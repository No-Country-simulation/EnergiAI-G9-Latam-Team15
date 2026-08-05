# ADR-001 — Contrato de integración JSON v1 entre Frontend, Backend y ML Service

**Estado:** Aceptado (implementado)
**Fecha de decisión:** 2026-07-21
**Fecha de formalización como ADR:** 2026-08-05
**Decisor:** Bernardo Adolfo Gómez Montoya (Software / Solution Architect)

---

## Contexto

EnergiAI separa el sistema en tres componentes independientes (React, Spring Boot, Python/Scikit-Learn — ver DA-01, DA-02 en `architecture/03-Arquitectura-Empresarial-EnergiAI.md`) que necesitan poder desarrollarse en paralelo sin bloquearse mutuamente. Para eso hace falta congelar, antes de empezar a construir, un formato único de intercambio entre Frontend y Backend.

## Decisión

Se define `architecture/contracts/API_CONTRACT_V1.md` como la especificación oficial y única del endpoint `POST /api/v1/analisis-energetico`: esquema de request (`consumo_kwh`, `uso_horario_pico`, `cantidad_equipos`, `tipo_inmueble`, `horas_alto_consumo`), esquema de response (`categoria`, `probabilidad`, `costo_estimado_mensual`, `recomendaciones`), categorías de clasificación (`Eficiente`/`Moderado`/`Ineficiente`) y códigos de error (400/500).

Este contrato cubre **únicamente Frontend↔Backend**. La comunicación interna Backend↔ML Service se documenta por separado en `architecture/contracts/CONTRATO_INTERNO_BACKEND_ML.md` (ADR-001 no la cubre, ver nota de consecuencias).

## Consecuencias

- Positivo: permitió que Frontend, Backend y ML Service se construyeran en ramas separadas y se integraran sin renegociar el formato sobre la marcha — confirmado en la demo end-to-end del 2026-08-04 (`meetings/ActaReunion-008-ENERGIAI.md`).
- Negativo / deuda detectada: el contrato define 5 valores posibles para `tipo_inmueble`, pero el modelo entrenado solo soporta 2 (`Casa`, `Pequeño establecimiento`) — ver corrección aplicada el 2026-08-05 en el propio `API_CONTRACT_V1.md` y registrada aquí para trazabilidad. La causa raíz fue no haber definido este ADR *antes* de escribir el contrato, sino después de que ya llevaba semanas en uso — de ahí que esta decisión se formalice ahora, retroactivamente.
- Pendiente: el Backend↔ML nunca tuvo un contrato equivalente versionado hasta el 2026-08-05 (ver ADR relacionado y `CONTRATO_INTERNO_BACKEND_ML.md`) — riesgo R-03 de `planning/04-Gestion-de-Riesgos-Arquitectonicos.md`, parcialmente mitigado con ese documento.

## Referencias

- `architecture/contracts/API_CONTRACT_V1.md`
- `architecture/contracts/CONTRATO_INTERNO_BACKEND_ML.md`
- `docs/architecture/AUDITORIA_BACKEND.md` §4 (mismatch de ruta detectado y corregido)
