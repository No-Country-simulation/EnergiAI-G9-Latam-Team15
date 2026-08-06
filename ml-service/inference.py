"""
inference.py — Servicio de inferencia de EnergiAI (FastAPI)

Expone el modelo entrenado por train.py como una API REST:
  - GET  /health   -> estado del servicio y si el modelo está cargado
  - POST /predict  -> recibe las 5 features del contrato y devuelve categoría + probabilidad

Diseño: carga UN solo artefacto (el pipeline completo entrenado en train.py, que ya
predice los nombres de clase directamente). El pipeline incluye el preprocesamiento,
así que aquí se le pasan las features CRUDAS -> se elimina el training-serving skew.

Ejecutar:  uvicorn inference:app --reload --port 8000
Docs auto: http://localhost:8000/docs
"""

import json
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- Rutas de artefactos (generados por train.py) ---
MODELS_DIR = Path(__file__).resolve().parent / "models"
MODEL_PATH = MODELS_DIR / "model.pkl"
META_PATH = MODELS_DIR / "model_metadata.json"

# Orden EXACTO de features que espera el pipeline (igual que en train.py y el contrato)
FEATURES = ["consumo_kwh", "cantidad_equipos", "horas_alto_consumo", "uso_horario_pico", "tipo_inmueble"]

PESOS_SCORE = {"Eficiente": 100, "Moderado": 50, "Ineficiente": 0}

app = FastAPI(
    title="EnergiAI — Servicio de Inferencia",
    description="Clasifica el perfil de consumo energético en Eficiente / Moderado / Ineficiente.",
    version="1.0.0",
)

# CORS abierto para pruebas locales/demo. En producción se restringe al dominio del backend/front.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado del servicio: el modelo se carga UNA vez al arrancar, no por request.
_model = None
_metadata = {}


@app.on_event("startup")
def load_model() -> None:
    """Carga el modelo y los metadatos al iniciar el servicio."""
    global _model, _metadata
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    if META_PATH.exists():
        _metadata = json.loads(META_PATH.read_text(encoding="utf-8"))


# ---------- Esquemas (contrato de entrada/salida) ----------
class PerfilConsumo(BaseModel):
    """Entrada: las 5 features del API_CONTRACT_V1."""
    consumo_kwh: float = Field(..., gt=0, description="Consumo mensual en kWh")
    uso_horario_pico: bool = Field(..., description="¿Consume en horario pico?")
    cantidad_equipos: int = Field(..., gt=0, description="Número de equipos")
    tipo_inmueble: Literal["Casa", "Pequeño establecimiento"] = Field(..., description="Tipo de inmueble")
    horas_alto_consumo: int = Field(..., ge=0, description="Horas de alto consumo")

    model_config = {
        "json_schema_extra": {
            "example": {
                "consumo_kwh": 350.0,
                "uso_horario_pico": True,
                "cantidad_equipos": 12,
                "tipo_inmueble": "Casa",
                "horas_alto_consumo": 8,
            }
        }
    }


class RespuestaPrediccion(BaseModel):
    """Salida del servicio ML (categoría + confianza). El costo y las
    recomendaciones los añade el backend, no el modelo."""
    categoria: str
    probabilidad: float
    probabilidades: dict[str, float]
    score_eficiencia: float


# ---------- Endpoints ----------
@app.get("/health")
def health() -> dict:
    """Chequeo de salud: útil para OCI y para el backend antes de integrar."""
    return {
        "status": "ok",
        "model_loaded": _model is not None,
        "model_version": _metadata.get("framework", "desconocido"),
        "classes": _metadata.get("classes", []),
    }


@app.post("/predict", response_model=RespuestaPrediccion)
def predict(perfil: PerfilConsumo) -> RespuestaPrediccion:
    """Recibe un perfil de consumo y devuelve su categoría de eficiencia + probabilidad."""
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no cargado. Ejecuta primero: python train.py (genera models/model.pkl)",
        )

    # Construir el DataFrame en el ORDEN exacto que espera el pipeline
    fila = pd.DataFrame([{
        "consumo_kwh": perfil.consumo_kwh,
        "cantidad_equipos": perfil.cantidad_equipos,
        "horas_alto_consumo": perfil.horas_alto_consumo,
        "uso_horario_pico": perfil.uso_horario_pico,
        "tipo_inmueble": perfil.tipo_inmueble,
    }])[FEATURES]

    categoria = str(_model.predict(fila)[0])
    proba_arr = _model.predict_proba(fila)[0]
    clases = list(_model.classes_)
    probabilidades = {str(c): round(float(p), 4) for c, p in zip(clases, proba_arr)}
    probabilidad = round(float(max(proba_arr)), 4)

    score_eficiencia = round(
        sum(PESOS_SCORE.get(c, 0) * p for c, p in probabilidades.items()), 2
    )

    return RespuestaPrediccion(
        categoria=categoria,
        probabilidad=probabilidad,
        probabilidades=probabilidades,
        score_eficiencia=score_eficiencia,
    )
