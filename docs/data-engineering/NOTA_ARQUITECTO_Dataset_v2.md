# Nota de Arquitectura y Trazabilidad — Dataset Maestro v2

### EnergiAI · NoCountry G9 LATAM
**Autor:** Bernardo Gómez Montoya — Software / Solution Architect
**Fecha:** 2026-07-25 · **Contexto:** cierre de Sprint 1

> Este documento cubre dos cosas que **no** están en el informe técnico y evita
> repetirlo: (1) el registro de la decisión de arquitectura y su encuadre de rol,
> y (2) la trazabilidad legal de las fuentes de datos. El detalle metodológico
> (curva horaria, criterios de clasificación, estadísticas) vive en
> [`INFORME_CONSOLIDACION_DATASET.md`](INFORME_CONSOLIDACION_DATASET.md) y no se
> reproduce aquí.

---

## 1. Decisión de arquitectura y encuadre de rol

El **Dataset Maestro** figura en el backlog como dependencia crítica: sin él se
bloquean las actividades de Data Science y Machine Learning (ver mapa de
dependencias en `docs/02-Revision-Arquitectonica-y-Version-Optimizada.md` §2.5, y
riesgo **R-01** en `planning/04-Gestion-de-Riesgos-Arquitectonicos.md`).

Ante la no disponibilidad de los datos base al cierre de Sprint 1, desde
Arquitectura se ejecutó una **acción de mitigación**: consolidar una base de datos
apta, trazable y reproducible. Esta acción **no introduce alcance nuevo** (el
dataset ya estaba en el backlog) y es coherente con el plan de contingencia
documentado para R-01, así como con la mitigación registrada en el acta 004.

**Encuadre de rol (importante).** Esta consolidación es una **habilitación** para
que el equipo de datos arranque, no una sustitución de su rol:

- El **EDA, el entrenamiento y la evaluación del modelo** siguen siendo de Data
  Science (Harrinson Villabona).
- El **ownership del pipeline de datos** corresponde a Data Engineering
  (Anayely Reyes).
- El **esquema de columnas** se conserva del trabajo previo de Backend
  (Elvis Trinidad), alineado con `API_CONTRACT_V1`.

El dataset se entrega como **propuesta para revisión y aprobación del equipo** en
la reunión de cierre de Sprint 1. No se asume aprobación previa: se somete a
validación colectiva.

## 2. Evidencia de proceso (resumen)

El proceso siguió dos fases con control humano entre ellas; el detalle está en el
informe técnico. Los hitos verificables:

- Se auditaron 1.322 archivos Excel oficiales de XM (44 mercados × 29 meses).
- Se detectó y corrigió un error de cálculo de curva en la Fase 1 (normalización
  por mercado antes de promediar) — el pico resultante (20:00h) se validó por dos
  vías independientes.
- Se detectaron y trataron problemas de calidad en la fuente (errores de captura
  puntuales, duplicados) mediante limpieza integrada en el script (no manual).
- Se verificó el CSV final de forma independiente, incluyendo una prueba de
  aprendibilidad con un modelo de referencia.

Este documento, junto con el informe técnico y el script reproducible, constituye
la evidencia de trazabilidad del entregable.

## 3. Trazabilidad y licenciamiento de datos (blindaje legal)

### 3.1 Fuente principal — XM S.A. E.S.P. (Colombia)

- **Producto:** "Indicadores de pronósticos oficiales de demanda" (Acuerdo CNO 1303).
- **URL:** https://www.xm.com.co/consumo/informes-demanda/indicadores-de-pronosticos-oficiales-de-demanda
- **Naturaleza:** demanda eléctrica real horaria del sistema (información pública).
- **Rango usado:** 2024-02 a 2026-06 (29 meses).

**Condiciones de uso (verificadas):** la información publicada por XM en sus
portales públicos es de acceso **público, gratuito y de uso libre, sin licencia ni
restricciones** para análisis e investigación. Referencias:
- Términos legales del sitio: https://www.xm.com.co/legales/terminos-legales-del-sitio-web
- Términos de uso de Sinergox: https://sinergox.xm.com.co/Documentos/Terminos_Condiciones/Terminos_Legales_Uso_Sinergox.pdf

**Restricciones respetadas por el proyecto:**
1. **Sin uso comercial.** EnergiAI es un MVP académico de hackathon; no comercializa
   ni vende la información de XM.
2. **Sin vínculo con XM.** El uso de datos públicos no implica asociación,
   patrocinio ni relación laboral con XM. El proyecto es independiente.
3. **Sin redistribución del crudo.** El dataset **no republica** los archivos de
   XM; solo usa la forma estadística de su curva de demanda como calibración. Los
   archivos crudos de XM **no forman parte del repositorio**.

### 3.2 Fuentes evaluadas y no incorporadas

| Fuente | País | Estado | Motivo |
|---|---|---|---|
| XM – Indicadores de demanda | Colombia | **Usada** (calibración) | Oficial, pública, granular, trazable |
| OSINERGMIN / Electro Puno | Perú | Evaluada, no usada en v2 | Reservada como expansión multi-país futura |
| Tarifas EPM Colombia | Colombia | No en el dataset | Son precios ($/kWh), no perfiles de consumo. Previstas para la estimación financiera del backend |

### 3.3 Datos personales

El dataset **no contiene datos personales** (registros sintéticos de consumo
agregado). No aplica tratamiento bajo la Ley 1581 de 2012 (Colombia).

## 4. Naturaleza del dataset (declaración de honestidad)

`dataset_maestro_v2.csv` es un conjunto **sintético calibrado**: los hogares son
generados (no medidos), pero su calibración (curva horaria y estacionalidad)
proviene de datos reales de XM. Esto cumple la directriz del reto —que permite
datos simulados y exige justificar los criterios— y se declara explícitamente
como parte de la calidad del entregable, no como una omisión.

---

## 5. Handoff — Sprint 2

Dataset **listo para consumo** en `data/processed/dataset_maestro_v2.csv`.
Próximos responsables (sin bloqueos):
- **Data Science (Harrinson):** EDA + baseline + métricas + serialización.
- **Data Engineering (Anayely):** ownership del pipeline (`dataset_maestro_v2.py`,
  ya reproducible y parametrizado).
- **Backend:** esquema alineado con `API_CONTRACT_V1`, consumo directo.
