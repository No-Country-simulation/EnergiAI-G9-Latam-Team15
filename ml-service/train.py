"""
train.py — Entrenamiento del modelo baseline de EnergiAI (Plan B de Arquitectura)

Implementa la metodología YA validada en INFORME_HIBRIDO_v3.md:
clasifica el consumo energético en {Eficiente, Moderado, Ineficiente} a partir
de las 5 features del API_CONTRACT_V1, usando RandomForest.

Salidas (en ml-service/models/):
  - model.pkl            -> pipeline completo (preprocesamiento + modelo), comprimido
  - model_metadata.json  -> features, clases, métricas, versión de sklearn, fecha

Diseño clave: se serializa el PIPELINE COMPLETO (no solo el modelo). Así, el
servicio de inferencia le pasa las features CRUDAS y el mismo objeto las codifica
igual que en entrenamiento -> se elimina el training-serving skew.
"""

import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# --- Rutas (robustas: relativas a la raíz del repo, sin importar desde dónde se corra) ---
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "processed" / "dataset_hibrido_v3.csv"
MODELS_DIR = REPO_ROOT / "ml-service" / "models"
MODEL_PATH = MODELS_DIR / "model.pkl"
META_PATH = MODELS_DIR / "model_metadata.json"

# --- Esquema del contrato (API_CONTRACT_V1): estas son las entradas del modelo ---
NUMERIC_FEATURES = ["consumo_kwh", "cantidad_equipos", "horas_alto_consumo"]
BOOL_FEATURES = ["uso_horario_pico"]
CATEGORICAL_FEATURES = ["tipo_inmueble"]  # {"Casa", "Pequeño establecimiento"}
FEATURES = NUMERIC_FEATURES + BOOL_FEATURES + CATEGORICAL_FEATURES
TARGET = "categoria"

RANDOM_STATE = 42


def build_pipeline() -> Pipeline:
    """Construye el pipeline: OneHot para tipo_inmueble + RandomForest.

    handle_unknown='ignore' evita que un tipo_inmueble no visto rompa la inferencia.
    El resto de features numéricas/booleanas pasan directo (RandomForest no requiere
    escalado). El bool se trata como número (0/1) automáticamente.
    """
    preprocess = ColumnTransformer(
        transformers=[("onehot", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES)],
        remainder="passthrough",  # deja pasar numéricas + bool sin tocar
    )
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced",  # robustez ante el leve desbalance de clases
    )
    return Pipeline([("preprocess", preprocess), ("model", model)])


def main() -> None:
    print("=" * 60)
    print("ENTRENAMIENTO — Modelo baseline EnergiAI")
    print("=" * 60)

    # 1) Cargar el dataset ya construido y validado
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES].copy()
    y = df[TARGET].copy()
    print(f"Dataset: {DATA_PATH.name} | filas={len(df)} | features={FEATURES}")
    print(f"Distribución de clases: {dict(y.value_counts())}")

    # 2) Validación honesta con StratifiedKFold (5-fold)
    #    Nota: la validación de investigación fue GroupKFold por hogar (cups),
    #    pero el dataset servido no incluye 'cups'. Como en producción el modelo
    #    puntúa filas independientes (una solicitud = un hogar), StratifiedKFold
    #    es la validación correcta para el modelo servido.
    pipe = build_pipeline()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy", n_jobs=-1)
    print(f"\nAccuracy (StratifiedKFold 5-fold): {cv_scores.mean():.3f} +/- {cv_scores.std():.3f}")

    # 3) Reporte por clase sobre un hold-out (para matriz de confusión legible)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )
    pipe.fit(X_tr, y_tr)
    y_pred = pipe.predict(X_te)
    print("\nReporte de clasificación (hold-out 20%):")
    print(classification_report(y_te, y_pred, digits=3))
    print("Matriz de confusión (filas=real, cols=predicho):")
    labels = sorted(y.unique())
    print(pd.DataFrame(confusion_matrix(y_te, y_pred, labels=labels), index=labels, columns=labels))

    # 4) Entrenar el modelo FINAL con TODOS los datos (más datos = mejor modelo)
    final_pipe = build_pipeline()
    final_pipe.fit(X, y)

    # 5) Serializar el PIPELINE completo, comprimido (resuelve el problema de peso)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_pipe, MODEL_PATH, compress=3)
    size_mb = MODEL_PATH.stat().st_size / (1024 * 1024)
    print(f"\nModelo guardado: {MODEL_PATH}  ({size_mb:.1f} MB)")

    # 6) Metadatos: lo que el servicio necesita para validar consistencia
    metadata = {
        "model_type": "RandomForestClassifier",
        "framework": f"scikit-learn {sklearn.__version__}",
        "python": platform.python_version(),
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "features": FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "target": TARGET,
        "classes": sorted(y.unique().tolist()),
        "cv_accuracy_mean": round(float(cv_scores.mean()), 4),
        "cv_accuracy_std": round(float(cv_scores.std()), 4),
        "n_rows": int(len(df)),
        "note": "Pipeline completo (OneHot + RF). Pasar features crudas; el pipeline codifica.",
    }
    META_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Metadatos guardados: {META_PATH}")

    # 7) Smoke test: recargar el .pkl y predecir un payload con forma del contrato
    _smoke_test()


def _smoke_test() -> None:
    """Recarga el modelo serializado y predice un ejemplo del contrato.
    Prueba que el artefacto guardado carga y predice (verificación end-to-end)."""
    print("\n" + "-" * 60)
    print("SMOKE TEST — recargar model.pkl y predecir un ejemplo")
    loaded = joblib.load(MODEL_PATH)
    sample = pd.DataFrame([{
        "consumo_kwh": 350.0,
        "cantidad_equipos": 12,
        "horas_alto_consumo": 8,
        "uso_horario_pico": True,
        "tipo_inmueble": "Casa",
    }])[FEATURES]
    pred = loaded.predict(sample)[0]
    proba = float(np.max(loaded.predict_proba(sample)))
    print(f"Entrada: {sample.to_dict(orient='records')[0]}")
    print(f"Predicción: categoria={pred!r} | probabilidad={proba:.2f}")
    print("OK: el modelo carga y predice correctamente.")


if __name__ == "__main__":
    main()
