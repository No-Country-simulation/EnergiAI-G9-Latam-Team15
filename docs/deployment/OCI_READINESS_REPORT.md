# OCI Readiness Report — EnergiAI

**Fecha original:** 2026-07-31
**Pregunta central:** ¿Puede EnergiAI desplegar en OCI hoy?

## Veredicto actualizado — 2026-08-05

# SÍ — ya desplegado.

Este documento se auto-advertía: *"debe re-emitirse, no asumirse, cada vez que se cierren las Tareas #4, #5 o #6"*. Esas tareas se cerraron. Las 3 imágenes (`energiai-frontend`, `energiai-backend`, `energiai-ml`, tag `:v1`) están publicadas en OCIR y el stack corre en OCI, confirmado con integración real (no mock) en la demo del 2026-08-04 (`meetings/ActaReunion-008-ENERGIAI.md`). Detalle operativo en `infra/oci/README.md` (creado 2026-08-05 — algunos campos, como la URL pública exacta, siguen pendientes de que Bernardo los documente).

**Camino mínimo (§ "Camino mínimo hacia un SÍ" más abajo): completado** — backend y ML responden `/health`, y `POST /api/v1/analisis-energetico` devuelve una respuesta generada por el modelo real.

**Pendiente aún, no bloqueante para el veredicto SÍ:** OCI Object Storage para modelo/dataset, OCI Logging/Monitoring, Vault, persistencia de histórico — ver `architecture/03-Arquitectura-Empresarial-EnergiAI.md` §8 (actualizado 2026-08-05).

---

## Veredicto original — 2026-07-31 (histórico, superado)

# NO.

No por ninguna limitación de Oracle Cloud Infrastructure como plataforma, sino porque **no existe todavía ningún artefacto desplegable**: ni backend compilable, ni servicio ML ejecutable, ni modelo serializado, ni imagen de contenedor, ni definición de infraestructura. OCI es el destino de un despliegue que hoy no tiene qué desplegar.

---

## Qué falta, quién es responsable, qué tarea del backlog lo respalda

| Gap | Detalle | Responsable (rol, `planning/01-Roles.md`) | Tarea del Backlog Sprint 2 |
|---|---|---|---|
| Proyecto Spring Boot inicializado | Falta `pom.xml`, estructura de paquetes, `application.yml` | Backend Developers (Carlos Fabian Mesa, Elvis Trinidad) | Tarea #4 (implícita como prerrequisito) |
| Endpoint `POST /api/v1/analisis-energetico` | No implementado | Backend Developers | Tarea #4 |
| Endpoint `GET /health` (backend) | No implementado | Backend Developers | Tarea #9 |
| Validación de payloads y errores 400/500 | No implementada | Backend Developers | Tarea #8 |
| Modelo entrenado y **serializado** | Solo existe como resultado narrado en `docs/data-engineering/INFORME_HIBRIDO_v3.md`; no hay artefacto `.pkl`/`.joblib` en el repo | Data Scientist (Harrinson Villabona) | Tareas #2 y #3 |
| Proyecto Python del servicio ML inicializado | Falta `requirements.txt`, framework de API | Data Scientist / Backend de apoyo | Tarea #5 (prerrequisito) |
| Endpoint de inferencia (`/predict` o equivalente) | No implementado | Data Scientist | Tarea #5 |
| Health check del servicio ML | No implementado | Data Scientist | Tarea #5 (implícito, buenas prácticas de despliegue) |
| Integración Backend ↔ ML real | No implementada — depende de que ambos servicios existan | Backend + Data Scientist | Tarea #6 |
| `Dockerfile` para backend | No existe | Backend Developers / Arquitectura | Tarea #10 (prerrequisito) |
| `Dockerfile` para ML service | No existe | Data Scientist / Arquitectura | Tarea #10 (prerrequisito) |
| Definición de infraestructura OCI (VCN, Container Instances, IAM) | No existe ni como IaC ni como documentación operativa | Software Architect (Bernardo Gómez) / rol de Infra | Tarea #10 |
| Confirmación de tenancy/cuenta OCI del hackathon | Sin evidencia en el repositorio de que esté resuelto | Product Owner (Luis Angel Chavez Mejía) | Prerrequisito de Tarea #10, no listado explícitamente en el backlog — **recomendación de esta auditoría: añadirlo como sub-tarea de la Tarea #10** |
| Corrección de ruta `apiService.js` vs. contrato | `/analisis-energetico` en frontend vs. `/api/v1/analisis-energetico` en el contrato | Full Stack (Alonso Carbajal) / Backend | Tarea #7 |
| Pipeline CI/CD mínimo | `.github/workflows/` vacío | Arquitectura / equipo | No listado en el backlog Sprint 2 — recomendación post-Tarea #10 |

---

## Camino mínimo hacia un "SÍ"

No es necesario resolver todos los ítems de la tabla para obtener un primer "sí" parcial. El camino mínimo verificable es:

1. Backend expone `GET /health` en un contenedor corriendo en OCI. → requiere: proyecto Spring Boot + `Dockerfile` + Container Instance.
2. ML service expone `GET /health` en un contenedor corriendo en OCI, con un modelo baseline cargado (aunque sea el primero, no el óptimo). → requiere: proyecto Python + modelo serializado + `Dockerfile` + Container Instance.
3. Una petición real `POST /api/v1/analisis-energetico` contra el backend desplegado devuelve una respuesta generada por el modelo real.

Este es exactamente el criterio de "hecho" ya definido en `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md` §7 y operacionalizado en `docs/deployment/CHECKLIST_OCI.md`.

---

## Reevaluación

Este veredicto debe re-emitirse (no asumirse) cada vez que se cierren las Tareas #4, #5 o #6 del backlog. Un "NO" de hoy no debe copiarse a futuro sin volver a verificar `git log` y el contenido real de `backend/`, `ml-service/` e `infra/` — ver la advertencia de consistencia en `docs/governance/MATRIZ_DEPENDENCIAS_SPRINT2.md` §3 sobre la brecha ya observada entre lo reportado en actas y el estado real del repositorio.
