# Informe de Consolidación — Dataset Maestro v2
### EnergiAI · NoCountry G9 LATAM — Clasificación de Eficiencia Energética

---

## 1. Procedencia de los datos

- **Fuente oficial:** XM S.A. E.S.P., operador del Sistema Interconectado Nacional (SIN) de Colombia.
- **Sección:** "Indicadores de pronósticos oficiales de demanda" —
  https://www.xm.com.co/consumo/informes-demanda/indicadores-de-pronosticos-oficiales-de-demanda
- **Carpeta cruda procesada:** `./Indicadores`, subcarpetas mensuales `AAAA-MM`.
- **Rango efectivamente procesado:** `2024-02` a `2026-06` (29 meses consecutivos, sin huecos).
- **Archivos usados:** `MC-SIN-OFI-DR-<mes>.xlsx`, hoja `real` (demanda real horaria, columnas `P1..P24`). `MC-SIN` es el mercado que agrega la demanda de **todo el Sistema Interconectado Nacional**, por lo que representa la curva de Colombia como país, no una sola región.
- **Archivos ignorados deliberadamente:** los 43 mercados comerciales regionales (`MC-Antioquia`, `MC-Cali`, `MC-Choco`, etc. — usados solo en la auditoría de calidad de la Fase 1, no en la calibración final) y los reportes `Informe_Indicadores_*.xlsx/.pptx` (no contienen la hoja `real`).

## 2. Metodología: calibración + síntesis, no XM directo

Los archivos de XM contienen **demanda real del sistema eléctrico** (MWh agregados por mercado comercializador), **no consumo de hogares individuales**. Usar estos datos como tabla de entrenamiento directa sería incorrecto: mezclaría carga industrial, comercial y residencial, y no tiene ninguna de las columnas que exige el contrato de la API (`cantidad_equipos`, `tipo_inmueble`, etc.).

Por eso XM se usa como **fuente de calibración**, no como tabla de hechos:

1. Se extrae de la hoja `real` de `MC-SIN` la **curva horaria promedio normalizada** (forma del día eléctrico típico de Colombia) y la **estacionalidad mensual** (variación de magnitud por mes calendario).
2. Sobre esa curva y esa estacionalidad **reales y verificadas**, se generan hogares residenciales **sintéticos** con distribuciones estadísticas realistas y reglas de clasificación justificadas.

Este enfoque cumple la directriz del reto (datos simulados que representen perfiles, con criterios documentados) y ancla la síntesis a un comportamiento eléctrico colombiano real y trazable, en vez de a supuestos arbitrarios.

## 3. Curva horaria real y cómo se usó

Calibrada sobre 881 días válidos de `MC-SIN` (2024-02 a 2026-06), tras limpieza de datos (ver §4):

| Hora | % demanda | | Hora | % demanda |
|---|---|---|---|---|
| 01h | 3.79% | | 13h | 4.44% |
| 02h | 3.66% | | 14h | 4.48% |
| 03h | 3.57% | | 15h | 4.53% |
| 04h | **3.51% (valle)** | | 16h | 4.54% |
| 05h | 3.55% | | 17h | 4.50% |
| 06h | 3.66% | | 18h | 4.44% |
| 07h | 3.70% | | 19h | 4.67% |
| 08h | 3.87% | | **20h** | **4.74% (pico)** |
| 09h | 4.06% | | 21h | 4.65% |
| 10h | 4.18% | | 22h | 4.47% |
| 11h | 4.32% | | 23h | 4.23% |
| 12h | 4.44% | | 24h | 3.98% |

**Pico a las 20:00h, valle a las 04:00h** — validado contra el rango esperado (19-20h) y contra un cross-check independiente promediando los 44 mercados por separado (mismo pico, misma hora).

**Uso en la síntesis:**
- La curva ancla la hora del pico (`uso_horario_pico`) usada en la Fase 2.
- **Nota metodológica importante:** la curva de `MC-SIN` diluye el pico residencial con carga industrial y comercial de 24h, por lo que su participación en horas pico (19-21h) es de solo ~1.1x el promedio horario (14.1% del día en 3 de 24 horas, vs 12.5% si fuera plano). A nivel de un hogar individual el pico nocturno es mucho más marcado (iluminación, cocina, TV, ducha eléctrica). Por eso se aplicó un **factor de amplificación residencial de 3.5x**, documentado en el código (`dataset_maestro_v2.py`, función `generate_households`), para pasar de "participación en el agregado nacional" a "probabilidad de uso pico a nivel de hogar". Esta es una decisión de diseño explícita, no un ajuste oculto.
- La estacionalidad mensual (ver tabla abajo) se usa como **ruido estacional controlado**: cada hogar sintético se asocia internamente a un mes calendario (sin guardarlo como columna, ya que el esquema del contrato no lo incluye) para inyectar en `consumo_kwh` la variabilidad estacional real de Colombia.

| Mes | Factor estacional |
|---|---|
| Enero | 0.984 | Julio | 0.999 |
| Febrero | 1.001 | Agosto | 0.996 |
| Marzo | 1.009 | Septiembre | 1.012 |
| Abril | 1.005 | Octubre | 0.998 |
| Mayo | 1.015 | Noviembre | 0.991 |
| Junio | 0.999 | Diciembre | 0.990 |

La variación es pequeña (±1.5%), consistente con el clima tropical colombiano (sin estaciones marcadas como en climas templados).

## 4. Hallazgos de calidad de datos (auditoría de Fase 1)

Se auditaron **los 1,322 archivos `MC-*-OFI-DR*.xlsx` de los 44 mercados** (no solo `MC-SIN`) para caracterizar la limpieza real de la fuente antes de decidir la calibración final. Hallazgos:

- **Estructura:** 100% de los archivos tienen la hoja `real` con la estructura esperada (`UCP, Varialble, FECHA, TIPO_DIA, P1..P24, Total, PO19-21`). 0 archivos corruptos al abrir, 0 hojas faltantes, 0 columnas `P25/P26/P27` (Colombia no tuvo cambios de horario en este rango), 0 valores nulos en `P1..P24`.
- **Errores de captura puntuales detectados:** `MC-Choco` (jul-2024, filas 15 y 18-jul) y `MC-Meta` (feb-2024, filas 6 y 7-feb) contienen celdas con valores físicamente imposibles (hasta 4.1×10¹⁴ y 4.3×10⁶ respectivamente, frente a un rango normal de decenas/cientos de MWh). Son errores aislados de captura en el archivo fuente de XM (el resto de cada fila es coherente), no error de lectura del script. **Estos dos mercados no forman parte de la calibración final** (que usa solo `MC-SIN`), pero se documentan porque motivaron el filtro de outliers aplicado también a `MC-SIN` como salvaguarda.
- **Cargas industriales intermitentes:** ~296 filas de mercados industriales pequeños (`Reficar`, `DrummondLoma`, `Ternium`, `Oxy`, `Drummond` — refinería y minería) muestran consumo casi nulo la mayor parte del día con picos puntuales de arranque de maquinaria. No es corrupción — es comportamiento real de carga industrial — pero no es representativo de hogares y quedó fuera del análisis de forma natural al usar solo `MC-SIN`.
- **Duplicación de filas:** `MC-SIN` de octubre 2025 contenía **56 filas para 31 días** (25 fechas duplicadas con valores idénticos, solo cambiaba la etiqueta `TIPO_DIA`). Se deduplicó por `(UCP, FECHA)`, quedándose con la primera ocurrencia.
- **Resultado en la calibración final (`MC-SIN`, 2024-02 a 2026-06):** 906 filas leídas → 25 duplicadas descartadas → **0 outliers** en `MC-SIN` específicamente (el mercado agregado nacional no mostró los errores puntuales vistos en mercados regionales pequeños) → 881 días válidos usados para la curva.

El filtro de outliers (`OUTLIER_RATIO = 15`, ratio máximo/mediana por fila) y la deduplicación por `(UCP, FECHA)` están implementados en `extract_sin_calibration()` dentro de `dataset_maestro_v2.py`, y se ejecutan automáticamente en cada corrida — no son una limpieza manual de un solo uso.

## 5. Criterios de clasificación (`categoria`)

`categoria` se asigna con un **score multicriterio** (no un umbral único, para que el problema sea realmente aprendible):

```
score = 0.35 · rank(kWh_por_equipo)        # más kWh por equipo → menos eficiente
      + 0.25 · rank(horas_alto_consumo/24) # más horas en franja de alto consumo → menos eficiente
      + 0.15 · uso_horario_pico (0/1)      # concentrar consumo en horario pico → menos eficiente
      + 0.25 · rank(consumo_kwh / mediana) # consumo muy por encima de la mediana → menos eficiente
```

(`rank(x)` = percentil 0-1 de `x` en el dataset; se usa percentil en vez de z-score para no dejar que un solo valor extremo domine el score, dado que `consumo_kwh` tiene cola alta).

- `score ≤ percentil 40` → **Eficiente**
- `percentil 40 < score ≤ percentil 75` → **Moderado**
- `score > percentil 75` → **Ineficiente**

Después se **reasigna aleatoriamente el 9% de las etiquetas** (`LABEL_NOISE_RATE = 0.09`) a una categoría al azar, simulando la incertidumbre real de etiquetado y evitando que el problema sea resoluble con una sola regla lineal.

## 6. Estadísticas del dataset final

- **Filas:** 10,000 · **Columnas:** 6 (exactamente el contrato: `consumo_kwh, uso_horario_pico, cantidad_equipos, tipo_inmueble, horas_alto_consumo, categoria`)
- **Nulos:** 0 en todas las columnas.
- **Duplicados:** 0 filas exactas (se generó con margen y se depuró; ver `dataset_maestro_v2.py`).
- **Semilla fija:** `SEED = 42` → reproducible byte a byte.

**Balance de clases:**

| categoria | % |
|---|---|
| Eficiente | 38.8% |
| Moderado | 34.7% |
| Ineficiente | 26.5% |

Balance razonable (sin el desbalance extremo tipo 85/12/2).

**`consumo_kwh`** (lognormal, calibrado a rango residencial colombiano típico):

| | min | p25 | mediana | p75 | max | media |
|---|---|---|---|---|---|---|
| kWh/mes | 40.0 | 142.2 | 189.6 | 252.7 | 1006.4 | 207.8 |

**Coherencia de las correlaciones** (verificada, no solo asumida):

| categoria | consumo_kwh medio | cantidad_equipos medio | % con uso_horario_pico |
|---|---|---|---|
| Eficiente | 154.0 | 8.4 | 2.4% |
| Moderado | 200.8 | 9.8 | 9.6% |
| Ineficiente | 296.0 | 13.0 | 48.0% |

El gradiente es monótono y con solapamiento realista entre clases (no separable con una sola regla), gracias al ruido de etiqueta del 9%.

**`tipo_inmueble`:** Casa 55.2% / Departamento 44.8% (parámetro de diseño, ver §7).

## 7. Fuentes evaluadas y decisión de alcance

Para este dataset se evaluaron tres fuentes disponibles en el entorno del hackathon:

1. **XM Colombia (`./Indicadores`)** — elegida como única fuente de calibración. Es un registro oficial, granular (horario), con 29 meses continuos y trazabilidad completa (URL pública, estructura documentada, auditoría de calidad realizada).
2. **`dataElvis/` (Perú/Puno, OSINERGMIN)** — evaluada pero **no usada** en esta v2. Mezclar dos países en un mismo dataset de calibración habría introducido curvas de demanda y contextos regulatorios distintos sin una forma limpia de combinarlos. Queda como **vía de expansión futura** (ej. dataset multi-país o comparativo).
3. **Tarifas EPM Colombia (CSV públicos)** — **no se incorporan al dataset**, ya que no describen perfiles de consumo sino precios ($/kWh). Se mencionan aquí porque son la fuente pública prevista para que el **backend** estime el costo financiero del consumo clasificado (cálculo de $/kWh sobre `consumo_kwh`), fuera del alcance de este dataset de entrenamiento.

## 8. Limitaciones honestas

- **Es un dataset sintético-calibrado, no una medición directa de hogares.** No hay medidores inteligentes residenciales en la fuente; los hogares se generan estadísticamente sobre una curva y estacionalidad reales, con reglas de clasificación documentadas pero, en última instancia, diseñadas por criterio experto (no aprendidas de etiquetas reales de eficiencia).
- **Alcance temporal:** 29 meses (2024-02 a 2026-06) de un solo mercado agregado (`MC-SIN`). No se incluyen años anteriores a 2024 ni variaciones inter-anuales más allá de las tres iteraciones de cada mes calendario disponibles.
- **`uso_horario_pico` usa un factor de amplificación residencial (3.5x) que es una decisión de diseño justificada, no un valor medido** — no existe en la fuente XM una desagregación de demanda exclusivamente residencial por hogar.
- **`cantidad_equipos`, `tipo_inmueble` y las reglas de `categoria` no provienen de XM** (XM no tiene esa granularidad); son supuestos de dominio explícitos y documentados en el código, consistentes con literatura de consumo residencial colombiano.

## 9. Mejora futura (no bloqueante)

Ampliar el rango de meses procesados en corridas futuras (el script ya lo soporta sin cambios de código, al descubrir automáticamente cualquier carpeta `AAAA-MM` presente en `./Indicadores`) daría mayor robustez estadística a la estacionalidad, especialmente si se incorporan años adicionales o se cruza con la fuente de Perú para un modelo multi-país. Esto es una oportunidad de refinamiento, no un pendiente que bloquee el uso del dataset actual.

---

## Anexo: archivos entregados

| Archivo | Descripción |
|---|---|
| `dataset_maestro_v2.py` | Script generador completo, parametrizado (lee cualquier conjunto de carpetas `AAAA-MM`), reproducible (semilla fija), con limpieza de datos (dedup + filtro de outliers) integrada. |
| `dataset_maestro_v2.csv` | Dataset final, 10,000 filas, UTF-8-SIG, esquema exacto del contrato de la API. |
| `INFORME_CONSOLIDACION_DATASET.md` | Este informe. |
