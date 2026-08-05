# Contrato de Integración JSON v1.0

## Proyecto

**EnergiAI**  
Hackathon ONE G9 LATAM | Alura + Oracle + NoCountry

---

# Objetivo

Definir el formato oficial de intercambio de información entre los componentes del sistema:

- Frontend (React)
- Backend (Spring Boot)
- ML Service (Python)
- Modelo de Clasificación Energética

Este contrato permitirá que los equipos trabajen de forma independiente y paralela utilizando una única especificación de integración.

---

# Endpoint Principal

```http
POST /api/v1/analisis-energetico
```

---

# Request

## Ejemplo

```json
{
  "consumo_kwh": 420,
  "uso_horario_pico": true,
  "cantidad_equipos": 10,
  "tipo_inmueble": "Casa",
  "horas_alto_consumo": 8
}
```

## Definición de Campos

| Campo | Tipo | Descripción |
|---------|---------|---------|
| consumo_kwh | number | Consumo mensual de energía en kWh |
| uso_horario_pico | boolean | Indica si existe consumo frecuente en horario pico |
| cantidad_equipos | integer | Número total de equipos eléctricos |
| tipo_inmueble | string | Tipo de inmueble |
| horas_alto_consumo | integer | Horas diarias aproximadas de alto consumo |

## Valores Permitidos

### tipo_inmueble

**Vigente para el MVP (2026-08-05):**

```text
Casa
Pequeño establecimiento
```

> **Nota de alineación (2026-08-05):** esta lista reemplaza la versión original de este contrato (`Casa, Apartamento, Local, Oficina, Pequeño Negocio`), que nunca coincidió con las categorías reales sobre las que se entrenó el modelo (`ml-service/train.py`, `CATEGORICAL_FEATURES`). El encoder del modelo usa `handle_unknown='ignore'`, así que enviar un valor no soportado no provoca error, pero degrada la predicción de forma silenciosa (se codifica como si no perteneciera a ninguna categoría conocida). Decisión de alcance MVP registrada en `meetings/ActaReunion-007-ENERGIAI.md` §4.3: mantener solo las dos categorías con datos reales suficientes; ampliar cobertura es mejora de Fase 2 (requiere reentrenar el modelo con muestra que incluya los demás tipos).

---

# Response

## Ejemplo

```json
{
  "categoria": "Ineficiente",
  "probabilidad": 0.81,
  "costo_estimado_mensual": 315.00,
  "recomendaciones": [
    "Reducir el uso de equipos durante horarios pico",
    "Evaluar equipos con alto consumo energético",
    "Distribuir actividades de mayor consumo a lo largo del día"
  ]
}
```

## Definición de Campos

| Campo | Tipo | Descripción |
|---------|---------|---------|
| categoria | string | Clasificación energética generada por el modelo |
| probabilidad | number | Nivel de confianza de la clasificación |
| costo_estimado_mensual | number | Costo energético estimado |
| recomendaciones | array | Lista de recomendaciones personalizadas |

---

# Categorías de Clasificación

```text
Eficiente
Moderado
Ineficiente
```

---

# Regla de Cálculo Financiero MVP

Tarifa de referencia:

```text
0.75 USD/kWh
```

Fórmula:

```text
costo_estimado_mensual = consumo_kwh × 0.75
```

Ejemplo:

```text
420 × 0.75 = 315.00 USD
```

---

# Respuesta de Error

## Error 400 - Datos inválidos

```json
{
  "status": "error",
  "code": 400,
  "message": "consumo_kwh es obligatorio"
}
```

## Error 500 - Error interno

```json
{
  "status": "error",
  "code": 500,
  "message": "Error interno del servicio"
}
```

---

# Flujo de Integración

```text
┌─────────────────┐
│ Frontend React  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Backend API     │
│ Spring Boot     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ML Service      │
│ Python          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Modelo IA       │
│ Clasificación   │
└─────────────────┘
```

---

# Alcance MVP

El MVP deberá permitir:

- Analizar patrones de consumo energético.
- Clasificar perfiles energéticos.
- Generar recomendaciones.
- Calcular costo estimado mensual.
- Exponer resultados mediante API REST.
- Integrarse con servicios OCI.

---

# Estado del Documento

**Versión:** 1.0

**Estado:** Vigente — implementado y verificado end-to-end (demo 2026-08-04, `meetings/ActaReunion-008-ENERGIAI.md`)

**Responsable:**  
Bernardo Adolfo Gómez Montoya  
Software / Solution Architect

**Fecha:**  
21/07/2026

**Última revisión:** 2026-08-05 — corrección de `tipo_inmueble` para reflejar las categorías reales del modelo (ver sección "Valores Permitidos"). Ver ADR-001 en `architecture/decisions/ADR-001-contrato-integracion-v1.md` para el historial de esta decisión. El contrato Backend↔ML Service (interno, no cubierto por este documento) está en `architecture/contracts/CONTRATO_INTERNO_BACKEND_ML.md`.
