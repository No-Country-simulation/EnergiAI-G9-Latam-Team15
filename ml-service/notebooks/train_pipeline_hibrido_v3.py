#!/usr/bin/env python3
"""
train_pipeline_hibrido_v3.py
══════════════════════════════════════════════════════════════════
Pipeline de entrenamiento · Eficiencia Energética — v2.0
Dataset : dataset_hibrido_v3.csv  (50 869 registros)

Estados de avance objetivo:
  [1] ✅ Modelo baseline entrenado
  [2] ✅ Métricas preliminares (5-Fold Stratified CV)
  [3] ✅ Modelo serializado (.pkl + metadata .json)
  [4] ✅ Servicio de inferencia disponible
══════════════════════════════════════════════════════════════════
Autor   : Data Scientist — Hackathon Eficiencia Energética
Fecha   : 2026-08-01
"""

# ── Librerías estándar ───────────────────────────────────────
import os
import sys
import json
import warnings
from datetime import datetime

# ── Científico / ML ──────────────────────────────────────────
import numpy  as np
import pandas as pd
import joblib

from sklearn.compose         import ColumnTransformer
from sklearn.ensemble        import RandomForestClassifier
from sklearn.metrics         import (accuracy_score, classification_report,
                                     confusion_matrix, f1_score)
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline        import Pipeline
from sklearn.preprocessing   import LabelEncoder, OrdinalEncoder

warnings.filterwarnings("ignore")


# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN GLOBAL
# ══════════════════════════════════════════════════════════════
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "dataset_hibrido_v3.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "modelos")
TARGET        = "categoria"
RANDOM_SEED   = 42
N_FOLDS       = 5
N_ESTIMATORS  = 200
ACCURACY_MIN  = 0.80

LINE  = "═" * 68
LINE2 = "─" * 68


def header(text: str) -> None:
    print(f"\n{LINE}\n  {text}\n{LINE}")


def subheader(text: str) -> None:
    print(f"\n  ── {text} {'─' * max(1, 60 - len(text))}")


# ══════════════════════════════════════════════════════════════
# PASO 1 · CARGA Y EXPLORACIÓN INICIAL (EDA)
# ══════════════════════════════════════════════════════════════
header("PASO 1 · CARGA Y EXPLORACIÓN DEL DATASET (EDA)")

# Carga robusta: utf-8-sig elimina BOM, strip limpia espacios residuales
df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]

print(f"""
   Archivo  : dataset_hibrido_v3.csv
   Shape    : {df.shape[0]:,} filas × {df.shape[1]} columnas
   Columnas : {list(df.columns)}
""")

# Primeras filas
print("  Muestra (5 primeras filas):")
print(df.head().to_string(index=True))

# Tipos y nulos
subheader("Tipos de datos y valores nulos")
print(f"  {'Columna':<24} {'Dtype':<12} {'Nulos':>7}")
print(f"  {LINE2}")
for col in df.columns:
    print(f"  {col:<24} {str(df[col].dtype):<12} {df[col].isnull().sum():>7}")

# Estadísticas descriptivas (numéricas)
subheader("Estadísticas descriptivas")
print(df.describe(percentiles=[0.25, 0.50, 0.75]).round(2).to_string())

# Distribución del target
subheader("Distribución del Target — 'categoria'")
total = len(df)
for cat, n in df[TARGET].value_counts().items():
    pct = n / total * 100
    bar = "█" * int(pct / 2)
    print(f"    {cat:<14}  {n:>7,}  ({pct:5.1f}%)  {bar}")

# Tipos de inmueble
subheader("Tipos de inmueble")
for tipo, n in df["tipo_inmueble"].value_counts().items():
    pct = n / total * 100
    print(f"    {tipo:<30}  {n:>7,}  ({pct:5.1f}%)")

# Regla determinista
subheader("Análisis de regla determinista  [uso_horario_pico → ¿siempre No-Eficiente?]")
pico_true = df[df["uso_horario_pico"] == True]
viols     = pico_true[pico_true[TARGET] == "Eficiente"]
pct_viol  = len(viols) / len(pico_true) * 100 if len(pico_true) > 0 else 0.0
print(f"    Registros pico=True             : {len(pico_true):,}")
print(f"    De esos → clasificados Eficiente: {len(viols):,}  ({pct_viol:.2f}%)")

if len(viols) == 0:
    print("     Regla DETERMINISTA confirmada (igual que dataset original)")
else:
    print(f"      Dataset híbrido: regla NO es determinista ({pct_viol:.1f}% de violaciones)")
    print("       → El modelo aprenderá el patrón completo desde los datos")

# Rangos por categoría
subheader("consumo_kwh por categoría (discriminador principal)")
print(df.groupby(TARGET)["consumo_kwh"].describe().round(2).to_string())

subheader("horas_alto_consumo por categoría")
print(df.groupby(TARGET)["horas_alto_consumo"].describe().round(2).to_string())

subheader("cantidad_equipos por categoría")
print(df.groupby(TARGET)["cantidad_equipos"].describe().round(2).to_string())


# ══════════════════════════════════════════════════════════════
# PASO 2 · PREPROCESAMIENTO
# ══════════════════════════════════════════════════════════════
header("PASO 2 · PREPROCESAMIENTO")

# Cast explícito: bool → int  (compatible con ColumnTransformer passthrough)
df["uso_horario_pico"] = df["uso_horario_pico"].astype(bool).astype(int)

# División features / target
FEATURES         = [c for c in df.columns if c != TARGET]
NUMERIC_COLS     = df[FEATURES].select_dtypes(include=["number"]).columns.tolist()
CATEGORICAL_COLS = df[FEATURES].select_dtypes(include=["object", "category"]).columns.tolist()

X = df[FEATURES].copy()
y = df[TARGET].copy()

# Label Encoding del target (preservamos el objeto para inversión posterior)
le    = LabelEncoder()
y_enc = le.fit_transform(y)

print(f"""
  Features numéricas   ({len(NUMERIC_COLS)}) : {NUMERIC_COLS}
  Features categóricas ({len(CATEGORICAL_COLS)}) : {CATEGORICAL_COLS}

  Codificación del target (LabelEncoder):""")
for cls, idx in zip(le.classes_, le.transform(le.classes_)):
    print(f"    {idx}  →  {cls}")

# ColumnTransformer: passthrough para numéricas, OrdinalEncoder para categóricas
# Nota: Random Forest no requiere escalado → passthrough es correcto
preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", NUMERIC_COLS),
        (
            "cat",
            OrdinalEncoder(
                handle_unknown="use_encoded_value",
                unknown_value=-1,
            ),
            CATEGORICAL_COLS,
        ),
    ],
    remainder="drop",
)

print(f"""
  ColumnTransformer configurado:
    └─ num ({len(NUMERIC_COLS)} feat) : passthrough
       Razón: RF mide importancia por impureza → escala no altera resultado
    └─ cat ({len(CATEGORICAL_COLS)} feat) : OrdinalEncoder
       handle_unknown='use_encoded_value' → robusto ante categorías nuevas""")


# ══════════════════════════════════════════════════════════════
# PASO 3 · ENTRENAMIENTO — MODELO BASELINE (RANDOM FOREST)
# ══════════════════════════════════════════════════════════════
header("PASO 3 · ENTRENAMIENTO — RANDOM FOREST BASELINE")

# Modelo: balanced compensa el desbalanceo de clases (Ineficiente ≈ 26%)
clf = RandomForestClassifier(
    n_estimators  = N_ESTIMATORS,
    max_depth     = None,
    class_weight  = "balanced",
    random_state  = RANDOM_SEED,
    n_jobs        = -1,
)

# Pipeline scikit-learn: encapsula preprocesamiento + clasificador
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier",   clf),
    ]
)

print(f"""
  Arquitectura del Pipeline:
    [1] preprocessor  →  ColumnTransformer (num + cat)
    [2] classifier    →  RandomForestClassifier
                         · n_estimators  : {N_ESTIMATORS}
                         · max_depth     : None  (árboles sin poda)
                         · class_weight  : balanced
                         · random_state  : {RANDOM_SEED}
""")

# ── 5-Fold Stratified Cross-Validation ───────────────────────
print(f"  ⏳ Ejecutando {N_FOLDS}-Fold Stratified CV  "
      f"(puede tomar ~30–60 s con 50K registros)...")

cv = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_SEED)

cv_results = cross_validate(
    pipeline, X, y_enc,
    cv              = cv,
    scoring         = {
        "accuracy"    : "accuracy",
        "f1_macro"    : "f1_macro",
        "f1_weighted" : "f1_weighted",
    },
    return_train_score = True,
    n_jobs             = -1,
)

subheader("MÉTRICAS PRELIMINARES (5-Fold Stratified CV)")
print(f"  {'Métrica':<16} {'Train Avg':>10} {'Train σ':>9} {'Val Avg':>10} {'Val σ':>9}")
print(f"  {LINE2}")

for key, label in [
    ("accuracy",    "Accuracy"),
    ("f1_macro",    "F1-Macro"),
    ("f1_weighted", "F1-Weighted"),
]:
    tr = cv_results[f"train_{key}"]
    vl = cv_results[f"test_{key}"]
    print(f"  {label:<16} {tr.mean():>10.4f} {tr.std():>9.4f} "
          f"{vl.mean():>10.4f} {vl.std():>9.4f}")

val_acc  = cv_results["test_accuracy"].mean()
val_f1   = cv_results["test_f1_macro"].mean()
val_f1w  = cv_results["test_f1_weighted"].mean()
val_acc_std = cv_results["test_accuracy"].std()

print(f"\n  Accuracy por fold : {list(cv_results['test_accuracy'].round(4))}")
print(f"\n   Accuracy media  (val) : {val_acc*100:.2f}% ± {val_acc_std*100:.2f}%")
print(f"   F1-Macro media  (val) : {val_f1:.4f}")
print(f"   F1-Weighted     (val) : {val_f1w:.4f}")

# Criterio de aceptación
print()
if val_acc < ACCURACY_MIN:
    print(f"   Accuracy ({val_acc:.2%}) < umbral mínimo ({ACCURACY_MIN:.0%})")
    print("     → Revisar hiperparámetros o features antes de serializar.")
    sys.exit(1)
else:
    print(f"  ✅ Criterio cumplido: {val_acc:.2%} ≥ {ACCURACY_MIN:.0%}")
    print("     → Proceder a entrenar modelo final y serializar.")

# ── Modelo final sobre corpus completo ───────────────────────
print("\n  ⏳ Entrenando modelo final sobre corpus completo...")
pipeline.fit(X, y_enc)
print("  ✅ Modelo final entrenado\n")

y_pred  = pipeline.predict(X)
in_acc  = accuracy_score(y_enc, y_pred)
in_f1   = f1_score(y_enc, y_pred, average="macro")

subheader("Reporte de clasificación completo (in-sample · referencia)")
print(classification_report(y_enc, y_pred, target_names=le.classes_, digits=4))

subheader("Matriz de Confusión (in-sample)")
cm    = confusion_matrix(y_enc, y_pred)
cm_df = pd.DataFrame(cm, index=le.classes_, columns=le.classes_)
print(cm_df.to_string())

# ── Importancia de features ───────────────────────────────────
subheader("Importancia de Features (Mean Decrease in Impurity)")
feat_names  = NUMERIC_COLS + CATEGORICAL_COLS
importances = pipeline.named_steps["classifier"].feature_importances_
imp_series  = pd.Series(importances, index=feat_names).sort_values(ascending=False)
max_imp     = imp_series.max()
for feat, imp in imp_series.items():
    bar = "█" * int(imp / max_imp * 35)
    print(f"    {feat:<24} {imp:.4f}  {bar}")


# ══════════════════════════════════════════════════════════════
# PASO 4 · SERIALIZACIÓN
# ══════════════════════════════════════════════════════════════
header("PASO 4 · SERIALIZACIÓN DE ARTEFACTOS")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Artefacto 1: Pipeline completo (preprocesador + modelo)
model_path = os.path.join(OUTPUT_DIR, "modelo_eficiencia_energetica.pkl")
joblib.dump(pipeline, model_path, compress=3)
model_kb = os.path.getsize(model_path) / 1024
print(f"\n   Pipeline serializado     → {model_path}")
print(f"                                ({model_kb:,.1f} KB, compress=3)")

# Artefacto 2: LabelEncoder (para invertir predicciones numéricas → texto)
le_path = os.path.join(OUTPUT_DIR, "label_encoder.pkl")
joblib.dump(le, le_path)
le_kb = os.path.getsize(le_path) / 1024
print(f"   LabelEncoder serializado → {le_path}")
print(f"                                ({le_kb:.1f} KB)")

# Artefacto 3: Metadata JSON (trazabilidad para el Solution Architect)
metadata = {
    "version"  : "2.0",
    "dataset"  : "dataset_hibrido_v3.csv",
    "n_samples": int(df.shape[0]),
    "n_features": len(FEATURES),
    "features"  : FEATURES,
    "numeric_features"    : NUMERIC_COLS,
    "categorical_features": CATEGORICAL_COLS,
    "target" : TARGET,
    "classes": list(le.classes_),
    "model"  : "RandomForestClassifier",
    "hyperparameters": {
        "n_estimators": N_ESTIMATORS,
        "max_depth"   : None,
        "class_weight": "balanced",
        "random_state": RANDOM_SEED,
    },
    "cross_validation": {
        "strategy"    : "StratifiedKFold",
        "n_splits"    : N_FOLDS,
        "shuffle"     : True,
        "random_state": RANDOM_SEED,
    },
    "metrics_cv": {
        "accuracy_mean"    : round(float(val_acc), 4),
        "accuracy_std"     : round(float(val_acc_std), 4),
        "f1_macro_mean"    : round(float(val_f1), 4),
        "f1_macro_std"     : round(float(cv_results["test_f1_macro"].std()), 4),
        "f1_weighted_mean" : round(float(val_f1w), 4),
        "f1_weighted_std"  : round(float(cv_results["test_f1_weighted"].std()), 4),
    },
    "metrics_insample": {
        "accuracy": round(float(in_acc), 4),
        "f1_macro": round(float(in_f1), 4),
    },
    "feature_importances": {
        feat: round(float(imp), 4)
        for feat, imp in imp_series.items()
    },
    "nota_dataset": (
        "Dataset hibrido: la regla determinista uso_horario_pico=True "
        "NO se mantiene de forma absoluta. El modelo aprende patrones "
        "multivariados sin hard-coding de reglas de negocio."
    ),
    "criteria_met": bool(val_acc >= ACCURACY_MIN),
    "trained_on"  : datetime.now().isoformat(),
}

meta_path = os.path.join(OUTPUT_DIR, "model_metadata.json")
with open(meta_path, "w", encoding="utf-8") as fh:
    json.dump(metadata, fh, indent=2, ensure_ascii=False)
meta_kb = os.path.getsize(meta_path) / 1024
print(f"   Metadata JSON guardada   → {meta_path}")
print(f"                                ({meta_kb:.1f} KB)")

print(f"\n  Contenido de {OUTPUT_DIR}/:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    sz = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
    print(f"    {f:<45}  {sz:>8.1f} KB")


# ══════════════════════════════════════════════════════════════
# RESUMEN EJECUTIVO
# ══════════════════════════════════════════════════════════════
header("RESUMEN EJECUTIVO — ESTADOS DE AVANCE")
print(f"""
    [1] Modelo baseline entrenado
          └─ Algoritmo    : RandomForestClassifier
          └─ n_estimators : {N_ESTIMATORS} árboles  |  max_depth=None
          └─ class_weight : balanced  (compensa Ineficiente ≈ 26%)
          └─ Pipeline     : ColumnTransformer + RandomForest

    [2] Métricas preliminares  ({N_FOLDS}-Fold Stratified CV)
          └─ Accuracy   : {val_acc*100:.2f}% ± {val_acc_std*100:.2f}%
          └─ F1-Macro   : {val_f1:.4f}
          └─ F1-Weighted: {val_f1w:.4f}
          └─ Criterio ≥ 80%: CUMPLIDO ✅

    [3] Modelo serializado (.pkl + .json)
          └─ {model_path}
          └─ {le_path}
          └─ {meta_path}

    [4] Servicio de inferencia disponible
          └─ inference.py  (predict_single, predict_batch)
""")