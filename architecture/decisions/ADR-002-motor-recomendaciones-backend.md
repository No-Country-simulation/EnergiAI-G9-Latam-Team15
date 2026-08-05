# ADR-002 — Ubicación del motor de recomendaciones: Backend, no Frontend ni ML Service

**Estado:** Aceptado (pendiente de implementación)
**Fecha de decisión:** 2026-08-05 (formalizando la recomendación de la auditoría del 2026-07-31)
**Decisor:** Bernardo Adolfo Gómez Montoya (Software / Solution Architect)

---

## Contexto

`docs/architecture/MOTOR_RECOMENDACIONES_v1.md` (auditoría técnica, 2026-07-31) detectó que la única lógica de generación de recomendaciones que existe en el repositorio vive dentro de `frontend/src/services/apiService.js`, en la función `generarRecomendaciones()` — parte del mock de fallback de contingencia, no de un componente designado para lógica de negocio. Esto contradice el flujo documentado en `API_CONTRACT_V1.md` (`Frontend → Backend → ML Service`, donde `recomendaciones` es parte de la respuesta del backend), y corre el riesgo de que la lógica se duplique de forma inconsistente si backend y frontend terminan generando reglas distintas.

Esa auditoría planteó tres opciones (A: mover al Backend, B: mover al ML Service, C: formalizar en el Frontend) y recomendó la Opción A.

## Decisión

El motor de reglas de recomendaciones vive en el **Backend** (`AnalisisEnergeticoService`), como parte de la implementación de `POST /api/v1/analisis-energetico`. Las 8 reglas actuales de `generarRecomendaciones()` (umbrales sobre `consumo_kwh`, `uso_horario_pico`, `horas_alto_consumo`) se portan de JavaScript a Java sin cambiar umbrales ni redactar textos nuevos, para no introducir regresión de UX.

**Justificación (ver DA-01):** el backend ya es el orquestador central del sistema; las reglas son deterministas y no dependen de ningún resultado probabilístico del modelo — es lógica de negocio tradicional, no lógica de ML. La Opción B (motor en el ML Service) queda como evolución legítima post-MVP, cuando se quiera basar las recomendaciones en *feature importance* real del modelo (`consumo_kwh` 46%, `horas_alto_consumo` 31% según `docs/data-engineering/INFORME_HIBRIDO_v3.md` §6).

El mock de `apiService.js` en el frontend **se mantiene**, pero exclusivamente como fallback de contingencia si el backend no responde — no como fuente de verdad.

## Estado de implementación (2026-08-05)

**No implementado.** `AnalisisEnergeticoService.java` hoy retorna 3 recomendaciones fijas hardcodeadas, no las 8 reglas condicionadas a la entrada. Esta ADR registra la decisión arquitectónica; la implementación queda como tarea pendiente, relacionada con el trabajo ya asignado a Cristian Coronel y Harrinson Villabona en `meetings/ActaReunion-008-ENERGIAI.md` §6 ("enriquecer recomendaciones con la data disponible") — portar las 8 reglas es el paso previo mínimo antes de enriquecerlas.

## Consecuencias

- Positivo: una sola fuente de verdad para las recomendaciones reales (backend), con el frontend limitado a fallback declarado.
- Pendiente de alinear: el texto de ejemplo en `API_CONTRACT_V1.md` no coincide literalmente con ninguna de las 8 reglas — se recomienda alinearlo cuando se complete la implementación en backend.
- Riesgo si no se implementa a tiempo: el sistema sigue mostrando recomendaciones genéricas idénticas para cualquier perfil de consumo, aunque la clasificación (`categoria`) sí varíe — inconsistencia notable de cara al jurado de NoCountry.

## Referencias

- `docs/architecture/MOTOR_RECOMENDACIONES_v1.md`
- `architecture/03-Arquitectura-Empresarial-EnergiAI.md` (DA-06)
- `backend/src/main/java/com/energiai/service/AnalisisEnergeticoService.java`
- `meetings/ActaReunion-008-ENERGIAI.md`
