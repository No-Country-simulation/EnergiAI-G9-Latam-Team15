"""
build_hibrido_final.py
=======================
Dataset Maestro v3 (HIBRIDO): consumo real de GoiEner + metodologia de
etiquetado balanceada validada en la v2 (XM Colombia).
Ver INFORME_HIBRIDO_v3.md para el detalle metodologico completo.

Uso: python build_hibrido_final.py
Requiere: monthly_features.csv en el mismo directorio (o ajustar ruta).
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

SEED = 42
CAP_KWH_MES = 2000.0
UMBRAL_PICO = 0.30
LABEL_NOISE_RATE = 0.09
P_CASA = 265214 / (265214 + 16918)  # proporcion real reportada sobre metadata completo de GoiEner

INPUT_PATH = "monthly_features.csv"
OUTPUT_PATH = "dataset_hibrido_v3.csv"


def main():
    rng = np.random.default_rng(SEED)
    mf = pd.read_csv(INPUT_PATH)
    print(f"Filas originales: {len(mf)} | cups unicos: {mf.cups.nunique()}")

    # 1) Outliers
    antes = len(mf)
    mf = mf[mf["consumo_kwh_mensual"] <= CAP_KWH_MES].copy()
    print(f"Outliers removidos (>{CAP_KWH_MES} kWh/mes): {antes - len(mf)} ({(antes-len(mf))/antes*100:.2f}%)")

    # 2) uso_horario_pico (derivado de dato real)
    mf["uso_horario_pico"] = mf["porcentaje_consumo_hora_pico"] > UMBRAL_PICO

    # 3) cantidad_equipos (sintetico, correlacionado, estable por hogar)
    cups_mean = mf.groupby("cups")["consumo_kwh_mensual"].transform("mean")
    pctile = cups_mean.rank(pct=True)
    base = 3 + 14 * pctile
    noise = pd.Series(rng.normal(0, 1.8, len(mf)), index=mf.index)
    mf["cantidad_equipos"] = np.clip(np.round(base + noise), 2, 22).astype(int)
    mf["cantidad_equipos"] = mf.groupby("cups")["cantidad_equipos"].transform("first")

    # 4) tipo_inmueble (sintetico, proporcion poblacional real, estable por hogar)
    cups_unicos = mf["cups"].unique()
    tipo_map = pd.Series(
        rng.choice(["Casa", "Pequeño establecimiento"], size=len(cups_unicos), p=[P_CASA, 1 - P_CASA]),
        index=cups_unicos,
    )
    mf["tipo_inmueble"] = mf["cups"].map(tipo_map)

    # 5) categoria (re-derivada, multicriterio + ruido -- metodologia v2)
    consumo = mf["consumo_kwh_mensual"]
    equipos = mf["cantidad_equipos"]
    horas = mf["horas_alto_consumo"]
    pico_flag = mf["uso_horario_pico"].astype(int)

    kwh_por_equipo = consumo / equipos
    frac_horas = (horas / horas.max()).clip(0, 1)
    consumo_rel = consumo / consumo.median()

    score = (
        0.35 * kwh_por_equipo.rank(pct=True)
        + 0.25 * frac_horas.rank(pct=True)
        + 0.15 * pico_flag
        + 0.25 * consumo_rel.rank(pct=True)
    )
    q40, q75 = score.quantile([0.40, 0.75])
    categoria = np.where(score <= q40, "Eficiente", np.where(score <= q75, "Moderado", "Ineficiente"))

    noise_mask = rng.random(len(mf)) < LABEL_NOISE_RATE
    noisy = rng.choice(["Eficiente", "Moderado", "Ineficiente"], size=noise_mask.sum())
    categoria = categoria.astype(object)
    categoria[noise_mask] = noisy

    # 6) Ensamblar esquema final (API_CONTRACT_V1)
    df = pd.DataFrame({
        "consumo_kwh": consumo.round(1),
        "uso_horario_pico": mf["uso_horario_pico"],
        "cantidad_equipos": mf["cantidad_equipos"],
        "tipo_inmueble": mf["tipo_inmueble"],
        "horas_alto_consumo": horas,
        "categoria": categoria,
    })
    df["_cups"] = mf["cups"].values  # solo para verificacion, se descarta al guardar

    before = len(df)
    df = df.drop_duplicates(subset=[c for c in df.columns if c != "_cups"]).reset_index(drop=True)
    print(f"Duplicados removidos: {before - len(df)}")
    print(f"Filas finales: {len(df)}")

    # 7) Verificacion honesta: GroupKFold por hogar (evita fuga de datos del panel)
    X = df.drop(columns=["categoria", "_cups"]).copy()
    X["tipo_inmueble"] = LabelEncoder().fit_transform(X["tipo_inmueble"])
    X["uso_horario_pico"] = X["uso_horario_pico"].astype(int)
    y = df["categoria"]
    groups = df["_cups"]

    clf = RandomForestClassifier(n_estimators=150, random_state=SEED, min_samples_leaf=5)
    scores = cross_val_score(clf, X, y, cv=GroupKFold(n_splits=5), groups=groups, scoring="accuracy")
    print(f"\nRandomForest accuracy (GroupKFold por hogar, 5-fold): {scores.mean():.3f} +/- {scores.std():.3f}")
    print(f"Baseline (clase mayoritaria): {y.value_counts(normalize=True).max():.3f}")

    print("\nBalance de clases:")
    print((y.value_counts(normalize=True) * 100).round(1))

    df.drop(columns=["_cups"]).to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\nGuardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
