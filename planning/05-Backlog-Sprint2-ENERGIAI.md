# Backlog Sprint 2 (Propuesta) — EnergiAI

### NoCountry G9 LATAM
**Propuesto por:** Bernardo Gómez Montoya — Software / Solution Architect
**Fecha:** 2026-07-28
**Estado:** Propuesta para revisión y aprobación del Product Owner

> Este backlog se construye sobre los objetivos ya definidos para Semana 2
> en `planning/03-Roadmap-Tecnico-5-Semanas.md` ("Vertical slice técnico"),
> ajustado al avance real del equipo a la fecha. Se somete a aprobación del
> PO; el equipo puede ajustar prioridades en la reunión.

---

## Objetivo de Sprint 2

Completar el flujo end-to-end del MVP: dato de consumo → clasificación →
recomendación → visualización, con un primer despliegue técnico en OCI.

---

## Estado heredado de Sprint 1 (contexto)

| Entregable | Estado |
|---|---|
| Contrato de integración (`API_CONTRACT_V1`) | ✅ Cerrado |
| Dataset Maestro v2 (XM Colombia) | ✅ Construido, PR #5 |
| Frontend (formulario, semáforo, historial, export PDF) | ✅ Completo, PR #4 aprobado y mergeado |
| Backend | 🟡 Iniciando |
| Modelo ML | 🔴 No iniciado (depende de dataset final) |
| Despliegue OCI | 🔴 No iniciado |

---

## Backlog propuesto

### 🔴 Prioridad crítica (bloquea el flujo end-to-end)

| # | Tarea | Rol sugerido | Depende de |
|---|---|---|---|
| 1 | Definir y construir dataset final (híbrido XM + GoiEner) | Data Engineering / Data Science, con apoyo de Data Analyst | Decisión en reunión de hoy |
| 2 | Entrenar modelo baseline (Regresión Logística o Random Forest) sobre dataset final + métricas (F1 macro, matriz de confusión) | Data Scientist | Tarea 1 |
| 3 | Serializar el modelo entrenado | Data Scientist | Tarea 2 |
| 4 | Implementar endpoint `POST /api/v1/analisis-energetico` en Spring Boot (según `API_CONTRACT_V1`) | Backend | — (ya en marcha) |
| 5 | Implementar servicio Python de inferencia (`POST /predict`), carga del modelo serializado | Backend / Data Scientist | Tarea 3 |
| 6 | Conectar Backend real ↔ Servicio ML (reemplaza mock) | Backend | Tareas 4, 5 |
| 7 | Reemplazar mock de `apiService.js` en frontend por la llamada real al Backend | Full Stack | Tarea 6 |

### 🟡 Prioridad alta (necesario para demo estable)

| # | Tarea | Rol sugerido | Depende de |
|---|---|---|---|
| 8 | Validación de payloads y manejo de errores en Backend (400/500 según contrato) | Backend | Tarea 4 |
| 9 | Endpoint `GET /health` | Backend | — |
| 10 | Primer despliegue técnico en OCI (Compute/Container Instance) — al menos Backend + ML | Arquitectura / Backend | Tareas 4-6 |
| 11 | Persistencia básica de resultados (histórico mínimo, según arquitectura MVP) | Backend | Tarea 4 |

### 🟢 Prioridad media (mejora, no bloquea)

| # | Tarea | Rol sugerido | Depende de |
|---|---|---|---|
| 12 | OCI Object Storage para dataset/modelo serializado | Arquitectura | Tarea 10 |
| 13 | Logs estructurados + smoke test básico | Backend / Arquitectura | Tarea 10 |
| 14 | Revisión de UX del frontend con datos reales (ajustes menores post-integración) | Full Stack | Tarea 7 |

### ⚪ Gobernanza / transversal

| # | Tarea | Rol sugerido |
|---|---|---|
| 15 | Consolidar y aprobar este backlog | Product Owner |
| 16 | Definir si Anayely (Data Engineer) se reincorpora con tarea concreta o se redistribuye el rol | Product Owner + equipo |
| 17 | Sincronizar rama `develop` regularmente para evitar el desvío que tuvimos en Sprint 1 | Arquitectura |

---

## Riesgos activos a vigilar (heredados de `planning/04-Gestion-de-Riesgos-Arquitectonicos.md`)

- **R-02** (precisión del modelo por debajo de lo esperado) — mitigar con baseline temprano (Tarea 2).
- **R-03** (contrato inestable Backend-ML) — ya congelado, vigilar que no cambie sin registrar el impacto.
- **R-04** (despliegue OCI tardío) — por eso se prioriza la Tarea 10 esta semana, no al final.
- **R-05** (dependencia de personas clave) — ver Tarea 16.

---

## Próximos pasos

1. Revisión y ajuste de este backlog en la reunión relámpago de hoy.
2. Aprobación formal del Product Owner.
3. Asignación definitiva de owners por tarea.
