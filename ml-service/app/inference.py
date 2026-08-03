#!/usr/bin/env python3
"""
inference.py
══════════════════════════════════════════════════════════════════
Servicio de Inferencia — Clasificación de Eficiencia Energética
Dataset de entrenamiento : dataset_hibrido_v3.csv
Modelo                   : RandomForestClassifier v2.0
══════════════════════════════════════════════════════════════════

Uso rápido
──────────
    from inference import predict_single, predict_batch

    # Clasificar un inmueble individual
    resultado = predict_single({
        "consumo_kwh":        120.5,
        "uso_horario_pico":   False,
        "cantidad_equipos":   3,
        "tipo_inmueble":      "Casa",
        "horas_alto_consumo": 2
    })
    print(resultado["categoria"])        # → "Eficiente"
    print(resultado["probabilidades"])   # → {"Eficiente": 0.91, ...}

    # Clasificar un lote desde un DataFrame
    import pandas as pd
    df = pd.read_csv("nuevos_inmuebles.csv")
    df_pred = predict_batch(df)
    print(df_pred[["categoria_pred", "prob_Eficiente"]])

Artefactos requeridos (misma carpeta que este archivo)
──────────
    modelo_eficiencia_energetica.pkl   → Pipeline sklearn (preprocesador + RF)
    label_encoder.pkl                  → LabelEncoder para decodificar clases
══════════════════════════════════════════════════════════════════
"""

import os
import joblib
import pandas as pd


# ── Rutas de artefactos (relativas a este archivo) ────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "modelo_eficiencia_energetica.pkl")
LE_PATH    = os.path.join(BASE_DIR, "label_encoder.pkl")

# Campos que el modelo espera recibir (en orden)
EXPECTED_FEATURES = [
    "consumo_kwh",
    "uso_horario_pico",
    "cantidad_equipos",
    "tipo_inmueble",
    "horas_alto_consumo",
]

# Singleton: se cargan una única vez por proceso
_pipeline = None
_le       = None


# ── Carga de artefactos ───────────────────────────────────────
def _load_artifacts() -> None:
    """
    Carga el pipeline y el label encoder en memoria (patrón Singleton).
    No hace nada si ya están cargados.
    """
    global _pipeline, _le
    if _pipeline is None:
        if not os.path.isfile(MODEL_PATH):
            raise FileNotFoundError(
                f"No se encontró el modelo en: {MODEL_PATH}\n"
                "Asegúrese de que 'inference.py' esté en la misma carpeta que los .pkl"
            )
        _pipeline = joblib.load(MODEL_PATH)

    if _le is None:
        if not os.path.isfile(LE_PATH):
            raise FileNotFoundError(f"No se encontró el LabelEncoder en: {LE_PATH}")
        _le = joblib.load(LE_PATH)


def _validate_and_cast(raw: dict) -> dict:
    """
    Valida que estén todos los campos y aplica cast de tipos seguros.

    Parámetros
    ----------
    raw : dict con los datos crudos del inmueble

    Retorna
    -------
    dict con tipos correctos para el pipeline

    Lanza
    -----
    ValueError si faltan campos requeridos
    """
    missing = [f for f in EXPECTED_FEATURES if f not in raw]
    if missing:
        raise ValueError(
            f"Campos requeridos ausentes: {missing}\n"
            f"Campos esperados: {EXPECTED_FEATURES}"
        )
    return {
        "consumo_kwh"        : float(raw["consumo_kwh"]),
        "uso_horario_pico"   : int(bool(raw["uso_horario_pico"])),
        "cantidad_equipos"   : int(raw["cantidad_equipos"]),
        "tipo_inmueble"      : str(raw["tipo_inmueble"]),
        "horas_alto_consumo" : int(raw["horas_alto_consumo"]),
    }


# ══════════════════════════════════════════════════════════════
# API PÚBLICA
# ══════════════════════════════════════════════════════════════

def predict_single(input_dict: dict) -> dict:
    """
    Clasifica un único inmueble y devuelve la categoría con probabilidades.

    Parámetros
    ----------
    input_dict : dict
        consumo_kwh        (float) — consumo en kWh
        uso_horario_pico   (bool)  — True si usa electricidad en horario pico
        cantidad_equipos   (int)   — número de equipos eléctricos
        tipo_inmueble      (str)   — p.ej. 'Casa' o 'Pequeño establecimiento'
        horas_alto_consumo (int)   — horas de alto consumo al día

    Retorna
    -------
    dict:
        categoria      (str)  — 'Eficiente', 'Moderado' o 'Ineficiente'
        probabilidades (dict) — probabilidad por clase, suma 1.0
        input_validado (dict) — registro después de aplicar cast de tipos
    """
    _load_artifacts()
    record = _validate_and_cast(input_dict)

    X_in    = pd.DataFrame([record])
    y_enc   = _pipeline.predict(X_in)
    y_proba = _pipeline.predict_proba(X_in)

    categoria      = _le.inverse_transform(y_enc)[0]
    clases         = list(_le.classes_)
    probabilidades = {c: round(float(p), 4) for c, p in zip(clases, y_proba[0])}

    return {
        "categoria"     : categoria,
        "probabilidades": probabilidades,
        "input_validado": record,
    }


def predict_batch(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clasifica un lote de inmuebles desde un DataFrame de pandas.

    Parámetros
    ----------
    df : pd.DataFrame
        Debe contener las columnas listadas en EXPECTED_FEATURES.
        Columnas adicionales se preservan sin modificar.

    Retorna
    -------
    pd.DataFrame — copia de `df` con columnas adicionales:
        categoria_pred     (str)   — clase predicha
        prob_Eficiente     (float) — probabilidad de ser Eficiente
        prob_Ineficiente   (float) — probabilidad de ser Ineficiente
        prob_Moderado      (float) — probabilidad de ser Moderado
    """
    _load_artifacts()

    # Validar columnas mínimas requeridas
    missing = [c for c in EXPECTED_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Columnas requeridas ausentes en el DataFrame: {missing}")

    X_in = df[EXPECTED_FEATURES].copy()
    X_in["uso_horario_pico"] = X_in["uso_horario_pico"].astype(bool).astype(int)

    y_enc   = _pipeline.predict(X_in)
    y_proba = _pipeline.predict_proba(X_in)
    clases  = list(_le.classes_)

    result                  = df.copy()
    result["categoria_pred"] = _le.inverse_transform(y_enc)
    for i, cls in enumerate(clases):
        result[f"prob_{cls}"] = y_proba[:, i].round(4)

    return result


# ══════════════════════════════════════════════════════════════
# DEMO (ejecutar directamente: python inference.py)
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":

    LINE = "─" * 58

    casos = [
        {
            "label"           : "Eficiente esperado",
            "consumo_kwh"     : 75.0,
            "uso_horario_pico": False,
            "cantidad_equipos": 2,
            "tipo_inmueble"   : "Apartamento",  # categoría no vista en entrenamiento
            "horas_alto_consumo": 1,
        },
        {
            "label"           : "Ineficiente esperado",
            "consumo_kwh"     : 850.0,
            "uso_horario_pico": True,
            "cantidad_equipos": 18,
            "tipo_inmueble"   : "Casa",
            "horas_alto_consumo": 350,
        },
        {
            "label"           : "Moderado esperado",
            "consumo_kwh"     : 210.0,
            "uso_horario_pico": False,
            "cantidad_equipos": 10,
            "tipo_inmueble"   : "Casa",
            "horas_alto_consumo": 190,
        },
        {
            "label"           : "Establecimiento pequeño",
            "consumo_kwh"     : 310.0,
            "uso_horario_pico": True,
            "cantidad_equipos": 14,
            "tipo_inmueble"   : "Pequeño establecimiento",
            "horas_alto_consumo": 220,
        },
    ]

    print("\n" + "=" * 58)
    print("  DEMO — Servicio de Inferencia (v2.0)")
    print("  Dataset entrenamiento: dataset_hibrido_v3.csv")
    print("=" * 58)

    for i, caso in enumerate(casos, 1):
        label  = caso.pop("label")
        result = predict_single(caso)
        caso["label"] = label  # restaurar para no mutar el dict

        print(f"\n  Caso {i}: {label}")
        print(f"  {LINE}")
        for feat in EXPECTED_FEATURES:
            print(f"    {feat:<22} : {caso[feat]}")
        print(f"  {LINE}")
        print(f"  → Clasificación     : {result['categoria']}")
        print(f"  → Probabilidades:")
        for cls, prob in sorted(result["probabilidades"].items(),
                                key=lambda x: x[1], reverse=True):
            bar = "█" * int(prob * 25)
            print(f"      {cls:<16} {prob:.4f}  {bar}")

    # Demo batch
    print(f"\n{'=' * 58}")
    print("  DEMO BATCH — predict_batch(DataFrame)")
    print(f"{'=' * 58}")
    batch_data = [
        {k: v for k, v in c.items() if k != "label"} for c in casos
    ]
    df_batch  = pd.DataFrame(batch_data)
    df_result = predict_batch(df_batch)
    cols_show = ["consumo_kwh", "uso_horario_pico",
                 "categoria_pred", "prob_Eficiente",
                 "prob_Ineficiente", "prob_Moderado"]
    print(f"\n{df_result[cols_show].to_string(index=False)}")
    print(f"\n{'=' * 58}")
    print("  ✅ Servicio de inferencia operativo")
    print(f"{'=' * 58}\n")
