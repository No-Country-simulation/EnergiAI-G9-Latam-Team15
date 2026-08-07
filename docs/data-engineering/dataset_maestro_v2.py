"""
dataset_maestro_v2.py
======================
Generador del dataset final para el reto de clasificacion de eficiencia energetica
(EnergiAI - NoCountry G9 LATAM).

Metodologia (resumen, ver INFORME_CONSOLIDACION_DATASET.md para el detalle):
  1. CALIBRACION: se lee la demanda real horaria de Colombia desde los archivos
     oficiales de XM S.A. E.S.P. (carpeta ./Indicadores, hoja "real" de cada
     archivo MC-<mercado>-OFI-DR-<mes>.xlsx). Se usa el mercado MC-SIN (agregado
     del Sistema Interconectado Nacional) para extraer:
       - la curva horaria promedio normalizada (forma del dia tipico en Colombia)
       - la estacionalidad mensual (variacion de magnitud por mes calendario)
     Antes de calibrar se limpian los datos: se deduplican filas repetidas
     (UCP, FECHA) y se descartan filas con valores atipicos extremos (errores
     de captura o cargas industriales intermitentes no representativas).
  2. SINTESIS: sobre esa calibracion real se generan ~10.000 hogares sinteticos
     con distribuciones realistas (lognormal para consumo, correlaciones
     controladas entre variables, reglas multicriterio para la categoria).

El script es parametrizable: procesa CUALQUIER conjunto de carpetas AAAA-MM
presentes en DATA_ROOT, no un numero fijo de meses. Es reproducible (semilla fija).

Uso:
    python dataset_maestro_v2.py
"""
from __future__ import annotations

import re
import statistics as st
from collections import defaultdict
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

# --------------------------------------------------------------------------
# Configuracion
# --------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_ROOT = SCRIPT_DIR / "Indicadores"
OUTPUT_CSV = SCRIPT_DIR / "dataset_maestro_v2.csv"

MONTH_DIR_PATTERN = re.compile(r"^\d{4}-\d{2}$")
MC_FILE_PATTERN = re.compile(r"^MC-.+-OFI-DR-.*\.xlsx$", re.IGNORECASE)
HOUR_COLS = [f"P{i}" for i in range(1, 25)]
OUTLIER_RATIO = 15.0  # fila descartada si max(P1..P24)/mediana(P1..P24) > este umbral

N_RECORDS = 10_000
SEED = 42
LABEL_NOISE_RATE = 0.09  # 9% de etiquetas re-asignadas aleatoriamente (problema aprendible, no trivial)

MESES_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


# --------------------------------------------------------------------------
# Fase de calibracion: lectura de XM
# --------------------------------------------------------------------------
def discover_month_dirs(data_root: Path) -> list[Path]:
    return sorted(p for p in data_root.iterdir() if p.is_dir() and MONTH_DIR_PATTERN.match(p.name))


def extract_sin_calibration(data_root: Path) -> dict:
    """Lee todos los archivos MC-SIN-OFI-DR-*.xlsx disponibles, limpia
    duplicados y outliers, y devuelve la curva horaria normalizada + la
    estacionalidad mensual calendario, junto con un log de calidad de datos.
    """
    month_dirs = discover_month_dirs(data_root)

    quality_log = {
        "month_dirs_found": len(month_dirs),
        "sin_files_found": 0,
        "sin_files_missing_or_corrupt": [],
        "rows_read_total": 0,
        "rows_duplicated_dropped": 0,
        "rows_outlier_dropped": [],
    }

    seen_dates = set()
    hourly_sum = np.zeros(24)
    hourly_days = 0
    monthly_total_by_calendar_month = defaultdict(list)

    for month_dir in month_dirs:
        candidates = list(month_dir.glob("MC-SIN-OFI-DR-*.xlsx"))
        if not candidates:
            quality_log["sin_files_missing_or_corrupt"].append(f"{month_dir.name}: sin archivo MC-SIN")
            continue
        f = candidates[0]
        quality_log["sin_files_found"] += 1

        try:
            wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
            ws = wb["real"]
            rows_iter = ws.iter_rows(values_only=True)
            header = next(rows_iter)
            col_index = {name: idx for idx, name in enumerate(header) if name}
            p_idx = [col_index[c] for c in HOUR_COLS]
            total_idx = col_index.get("Total")
        except Exception as e:
            quality_log["sin_files_missing_or_corrupt"].append(f"{f.relative_to(data_root)}: {e}")
            continue

        for row in rows_iter:
            quality_log["rows_read_total"] += 1
            fecha = row[2]
            dedup_key = ("MC-SIN", fecha)
            if dedup_key in seen_dates:
                quality_log["rows_duplicated_dropped"] += 1
                continue
            seen_dates.add(dedup_key)

            hv = [row[i] for i in p_idx]
            if any(v is None for v in hv):
                continue
            med = st.median(hv)
            mx = max(hv)
            if med <= 0 or (mx / med) > OUTLIER_RATIO:
                quality_log["rows_outlier_dropped"].append(
                    f"{f.relative_to(data_root)} | fecha={str(fecha)[:10]} | max={mx:.1f} | mediana={med:.1f}"
                )
                continue

            hourly_sum += np.array(hv)
            hourly_days += 1

            if total_idx is not None and row[total_idx] is not None:
                month_name = MESES_ES[fecha.month - 1]
                monthly_total_by_calendar_month[month_name].append(row[total_idx])
        wb.close()

    hourly_curve = hourly_sum / hourly_sum.sum()

    seasonality = {}
    for month_name in MESES_ES:
        vals = monthly_total_by_calendar_month.get(month_name, [])
        seasonality[month_name] = st.mean(vals) if vals else None
    overall_mean = st.mean([v for v in seasonality.values() if v is not None])
    seasonality_factor = {m: (v / overall_mean if v is not None else 1.0) for m, v in seasonality.items()}

    quality_log["hourly_curve"] = hourly_curve.tolist()
    quality_log["peak_hour"] = int(np.argmax(hourly_curve)) + 1
    quality_log["valley_hour"] = int(np.argmin(hourly_curve)) + 1
    quality_log["seasonality_factor"] = seasonality_factor
    quality_log["days_used_for_curve"] = hourly_days

    return quality_log


# --------------------------------------------------------------------------
# Fase de sintesis: hogares sinteticos
# --------------------------------------------------------------------------
def generate_households(n: int, calibration: dict, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    hourly_curve = np.array(calibration["hourly_curve"])
    seasonality_factor = calibration["seasonality_factor"]

    # --- tipo_inmueble ---
    tipo_inmueble = rng.choice(["Casa", "Departamento"], size=n, p=[0.55, 0.45])

    # --- consumo_kwh: lognormal calibrada a rango residencial colombiano tipico ---
    mu, sigma = np.log(185), 0.42
    consumo_base = rng.lognormal(mean=mu, sigma=sigma, size=n)
    tipo_factor = np.where(tipo_inmueble == "Casa", 1.08, 0.94)

    # jitter estacional: cada hogar se asocia a un mes calendario (sin guardarlo
    # en el dataset final) para inyectar la estacionalidad real de XM en la
    # dispersion del consumo, sin violar el esquema exacto de columnas.
    month_choices = rng.choice(MESES_ES, size=n)
    seasonal_factor = np.array([seasonality_factor[m] for m in month_choices])

    consumo_kwh = consumo_base * tipo_factor * seasonal_factor
    consumo_kwh = np.clip(consumo_kwh, 40, 1200)

    # percentil de consumo (0-1), usado para correlacionar el resto de variables
    consumo_pctile = pd.Series(consumo_kwh).rank(pct=True).to_numpy()

    # --- cantidad_equipos: correlacionado con consumo + ruido ---
    base_equipos = 3 + 14 * consumo_pctile
    cantidad_equipos = np.round(base_equipos + rng.normal(0, 1.8, n))
    cantidad_equipos = np.clip(cantidad_equipos, 2, 22).astype(int)

    # --- uso_horario_pico: probabilidad ligada a la curva horaria real de XM ---
    # La curva de XM (MC-SIN) diluye el pico residencial con carga industrial y
    # comercial 24h, por lo que su participacion en horas pico (19-21h) es solo
    # ~1.1x el promedio horario. A nivel de un hogar individual el pico nocturno
    # es mucho mas marcado (iluminacion, cocina, TV, ducha electrica), por lo
    # que se aplica un factor de amplificacion residencial documentado (3.5x).
    peak_share_sin = hourly_curve[18:21].mean()  # horas 19,20,21 (indices 18-20)
    residential_amplification = 3.5
    p_base = min(0.85, peak_share_sin * residential_amplification)
    p_peak = np.clip(p_base + 0.30 * (consumo_pctile - 0.5), 0.05, 0.95)
    uso_horario_pico = rng.random(n) < p_peak

    # --- horas_alto_consumo: correlacionado con consumo y con uso_horario_pico ---
    base_horas = 2 + 6 * consumo_pctile + np.where(uso_horario_pico, 2, 0)
    horas_alto_consumo = np.round(base_horas + rng.normal(0, 1.2, n))
    horas_alto_consumo = np.clip(horas_alto_consumo, 1, 14).astype(int)

    df = pd.DataFrame({
        "consumo_kwh": np.round(consumo_kwh, 1),
        "uso_horario_pico": uso_horario_pico,
        "cantidad_equipos": cantidad_equipos,
        "tipo_inmueble": tipo_inmueble,
        "horas_alto_consumo": horas_alto_consumo,
    })
    return df


def assign_categoria(df: pd.DataFrame, noise_rate: float, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 1)

    kwh_per_equipo = df["consumo_kwh"] / df["cantidad_equipos"]
    frac_horas_pico = df["horas_alto_consumo"] / 24.0
    consumo_relativo = df["consumo_kwh"] / df["consumo_kwh"].median()
    pico_flag = df["uso_horario_pico"].astype(int)

    # ranking percentil (0-1) por criterio: mas robusto a la asimetria (cola alta)
    # que un z-score, y evita que un solo outlier domine el score.
    r_kwh_equipo = kwh_per_equipo.rank(pct=True)
    r_horas_pico = frac_horas_pico.rank(pct=True)
    r_consumo_rel = consumo_relativo.rank(pct=True)

    score = (
        0.35 * r_kwh_equipo +      # mas kWh por equipo = menos eficiente
        0.25 * r_horas_pico +      # mas horas en franja de alto consumo = menos eficiente
        0.15 * pico_flag +         # concentrar consumo en horario pico = menos eficiente
        0.25 * r_consumo_rel       # consumo muy por encima de la mediana = menos eficiente
    )

    q40, q75 = score.quantile([0.40, 0.75])
    categoria = np.where(score <= q40, "Eficiente",
                 np.where(score <= q75, "Moderado", "Ineficiente"))

    # ruido de etiqueta controlado: ~9% de los registros se reasignan a una
    # categoria aleatoria para evitar un umbral trivial y forzar un problema
    # de clasificacion realmente aprendible (no separable con una sola regla).
    noise_mask = rng.random(len(df)) < noise_rate
    noisy_labels = rng.choice(["Eficiente", "Moderado", "Ineficiente"], size=noise_mask.sum())
    categoria = categoria.astype(object)
    categoria[noise_mask] = noisy_labels

    df["categoria"] = categoria
    return df


# --------------------------------------------------------------------------
# Orquestacion
# --------------------------------------------------------------------------
def main():
    print("=== FASE 2.1: Calibracion desde datos reales de XM (./Indicadores) ===")
    calibration = extract_sin_calibration(DATA_ROOT)
    print(f"Carpetas AAAA-MM encontradas: {calibration['month_dirs_found']}")
    print(f"Archivos MC-SIN leidos: {calibration['sin_files_found']}")
    print(f"Meses sin archivo MC-SIN / con error: {len(calibration['sin_files_missing_or_corrupt'])}")
    for m in calibration["sin_files_missing_or_corrupt"]:
        print(f"  - {m}")
    print(f"Filas leidas: {calibration['rows_read_total']}")
    print(f"Filas duplicadas (mismo FECHA) descartadas: {calibration['rows_duplicated_dropped']}")
    print(f"Filas con outliers descartadas: {len(calibration['rows_outlier_dropped'])}")
    for o in calibration["rows_outlier_dropped"]:
        print(f"  - {o}")
    print(f"Dias validos usados para la curva: {calibration['days_used_for_curve']}")
    print(f"Pico horario calibrado: P{calibration['peak_hour']} ({calibration['peak_hour']}:00h)")
    print(f"Valle horario calibrado: P{calibration['valley_hour']} ({calibration['valley_hour']}:00h)")
    print()

    print("=== FASE 2.2: Generacion de hogares sinteticos ===")
    df = generate_households(N_RECORDS, calibration, SEED)
    df = assign_categoria(df, LABEL_NOISE_RATE, SEED)

    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    dropped_dupes = before - len(df)
    # top-up si el dedup dejo el dataset por debajo de N_RECORDS (extremadamente
    # improbable con variables continuas, pero se deja como salvaguarda)
    extra_seed = SEED
    while len(df) < N_RECORDS:
        extra_seed += 1000
        extra = generate_households(N_RECORDS - len(df), calibration, extra_seed)
        extra = assign_categoria(extra, LABEL_NOISE_RATE, extra_seed)
        df = pd.concat([df, extra]).drop_duplicates().reset_index(drop=True)

    print(f"Registros generados: {before} | duplicados exactos eliminados: {dropped_dupes} | final: {len(df)}")
    print()
    print("Balance de clases (categoria):")
    print(df["categoria"].value_counts(normalize=True).round(3))
    print()
    print("Estadisticas de consumo_kwh:")
    print(df["consumo_kwh"].describe().round(1))
    print()
    print("Nulos por columna:")
    print(df.isnull().sum())

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"\nDataset guardado en: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
