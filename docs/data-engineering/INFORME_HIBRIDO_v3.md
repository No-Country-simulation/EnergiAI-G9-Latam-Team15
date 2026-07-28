# Informe de Consolidación — Dataset Maestro v3 (Híbrido)

### EnergiAI · NoCountry G9 LATAM
**Construido por:** Bernardo Gómez Montoya, sobre el análisis de GoiEner
aportado por Magno Cristian Coronel Salazar.
**Fecha:** 2026-07-28

---

## 1. Qué es este dataset

Combina **consumo eléctrico real medido** (GoiEner Smart Meter Dataset v7,
España) con la **metodología de calibración y etiquetado balanceado**
desarrollada y validada en el Dataset Maestro v2 (XM Colombia). Reemplaza,
como propuesta, tanto al dataset puramente sintético (v2) como al análisis
inicial de GoiEner (que usaba percentiles puros y resultó circular).

- **Fuente de origen real:** GoiEner Smart Meter Dataset v7 (imputado),
  https://zenodo.org/records/14949245. Diccionario de campos:
  https://zenodo.org/records/7362094
- **Muestra base:** 1.000 puntos de suministro (cups), 963 con datos
  extraídos (37 sin archivo — reportado por el propio análisis de origen).
- **Filas base:** 53.168 combinaciones cups–mes (panel, ~55 meses por hogar).
- **Esquema de salida:** exactamente `API_CONTRACT_V1`
  (`consumo_kwh, uso_horario_pico, cantidad_equipos, tipo_inmueble,
  horas_alto_consumo, categoria`).

---

## 2. Qué es real y qué es sintético (declaración explícita)

| Variable | Origen | Detalle |
|---|---|---|
| `consumo_kwh` | **Real** | `consumo_kwh_mensual` de GoiEner, medido por smart meter |
| `horas_alto_consumo` | **Real** | Calculado por el análisis de origen sobre la serie horaria real |
| `uso_horario_pico` | **Derivado de dato real** | Umbral aplicado sobre `porcentaje_consumo_hora_pico` (real): >30% → `True`. Umbral consistente con el criterio ya usado en el análisis de origen |
| `cantidad_equipos` | **Sintético** | GoiEner no reporta esta variable en ningún archivo. Se sintetiza correlacionada con el consumo promedio de cada hogar (mismo método validado en la v2), estable por hogar en el tiempo |
| `tipo_inmueble` | **Sintético (basado en proporción real poblacional)** | El archivo `metadata.csv` de GoiEner (que trae `tarifa_atr` real) no fue adjuntado a esta construcción. Se asigna probabilísticamente por hogar usando la proporción real reportada sobre el metadata completo de GoiEner: 94,0% Casa / 6,0% Pequeño establecimiento. **Limitación reconocida**: no es el dato real por hogar, es una asignación consistente con la distribución poblacional real |
| `categoria` | **Re-derivada** | Ver §3 |

---

## 3. Limpieza y tratamiento aplicado

- **Outliers:** se eliminaron 1.165 filas (2,19%) con `consumo_kwh_mensual`
  > 2.000 kWh/mes (físicamente inverosímil para Casa/Pequeño
  establecimiento; máximo original era 25.869 kWh/mes).
- **Duplicados:** 1.134 filas exactas eliminadas tras ensamblar el esquema
  final (52.003 → 50.869).
- **Nulos:** 0 en todas las columnas del esquema final.

---

## 4. Metodología de clasificación (`categoria`)

Se descartó la clasificación original de GoiEner (percentiles puros de una
sola variable) porque, al auditarla, resultó **circular**: un modelo
entrenado con las mismas variables usadas para etiquetar reconstruía la
regla al 100% de precisión — no aprendía un patrón, repetía la fórmula.

Se aplicó en su lugar la metodología ya validada en la v2 — score
multicriterio + ruido de etiqueta controlado:

```
score = 0.35 · rank(kWh_por_equipo)
      + 0.25 · rank(horas_alto_consumo / máximo)
      + 0.15 · uso_horario_pico (0/1)
      + 0.25 · rank(consumo_kwh / mediana)

Eficiente:   score ≤ percentil 40
Moderado:    percentil 40 < score ≤ percentil 75
Ineficiente: score > percentil 75

+ 9% de las etiquetas reasignadas aleatoriamente (ruido controlado)
```

---

## 5. Estadísticas del dataset final

- **Filas:** 50.869 · **Columnas:** 6 (esquema exacto del contrato)
- **Nulos:** 0 · **Duplicados exactos:** 0
- **Balance de clases:** Eficiente 38,4% / Moderado 35,4% / Ineficiente 26,2%
  — casi idéntico al balance de la v2 (38,8/34,7/26,5), lo que valida que la
  metodología es consistente entre fuentes distintas.
- **Consumo (kWh/mes):** mediana 138,4, media 205,2, rango 0–1.997,5.
- **Gradiente coherente entre clases** (verificado, no solo asumido):

| categoria | consumo medio | equipos medio | horas alto consumo medio |
|---|---|---|---|
| Eficiente | 89,4 | 8,8 | 114,3 |
| Moderado | 194,2 | 10,4 | 191,2 |
| Ineficiente | 389,7 | 12,1 | 267,9 |

---

## 6. Validación de aprendibilidad (metodológicamente honesta)

Como el dataset es un **panel** (múltiples filas por el mismo hogar a lo
largo de los meses), una validación cruzada estándar (K-Fold por fila)
sobreestimaría el rendimiento, porque el mismo hogar podría aparecer en
entrenamiento y en prueba simultáneamente.

Se usó **GroupKFold agrupando por hogar (`cups`)**, garantizando que ningún
hogar aparezca en ambos conjuntos:

- **RandomForest, GroupKFold 5-fold: 91,7% ± 0,3% de accuracy**, contra
  38,4% de baseline (clase mayoritaria).
- Todas las variables aportan señal: `consumo_kwh` (46%), `horas_alto_consumo`
  (31%), `cantidad_equipos` (13%), `uso_horario_pico` (10%), `tipo_inmueble`
  (0,2% — esperado y honesto, ya que su asignación es poblacional, no
  correlacionada por diseño con el resto).

**Nota para quien entrene el modelo final:** dado que es un panel, se
recomienda seguir usando una división por hogar (no por fila) al entrenar
el modelo de producción, para evitar una estimación optimista del
desempeño real.

---

## 7. Limitaciones honestas

- `tipo_inmueble` y `cantidad_equipos` no son mediciones reales por hogar;
  están documentadas como síntesis razonada (ver §2).
- El origen geográfico es España, no Colombia/LATAM — mismo tipo de
  consideración que se documentó para las fuentes previas evaluadas.
- Es un panel de datos (un hogar aparece en muchas filas); cualquier
  evaluación de modelo debe respetar esa estructura (ver §6).
- La categoría es una construcción metodológica razonada y documentada,
  no una etiqueta verificada externamente — igual que en la v2.

---

## 8. Créditos

- **Fuente de datos real y extracción inicial:** Magno Cristian Coronel
  Salazar (Data Analyst), a partir de GoiEner Smart Meter Dataset v7.
- **Metodología de calibración, limpieza y etiquetado:** desarrollada
  originalmente para el Dataset Maestro v2 (XM Colombia) por Bernardo
  Gómez Montoya, reaplicada aquí sobre los datos reales de GoiEner.

---

## Anexo: archivos entregados

| Archivo | Descripción |
|---|---|
| `dataset_hibrido_v3.csv` | Dataset final, 50.869 filas, UTF-8-SIG, esquema exacto del contrato |
| `build_hibrido.py` | Script generador, comentado, reproducible (semilla fija 42) |
| `INFORME_HIBRIDO_v3.md` | Este informe |
