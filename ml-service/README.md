# ML Service

Modulo de ciencia de datos e inferencia de EnergiAI.

## Responsabilidad

- cargar el modelo aprobado,
- ejecutar inferencia,
- mantener consistencia entre features de entrenamiento e inferencia,
- soportar evolucion del baseline y mejora del modelo.

## Estructura esperada

- `app/` servicio de inferencia
- `models/` artefactos serializados del modelo
- `notebooks/` exploracion y experimentacion controlada
- `tests/` pruebas del servicio y validaciones basicas
