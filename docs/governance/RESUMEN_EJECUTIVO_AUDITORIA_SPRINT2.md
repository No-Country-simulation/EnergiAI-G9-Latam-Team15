# Resumen Ejecutivo — Auditoría Técnica Sprint 2

**Fecha original:** 2026-07-31
**Audiencia:** Product Owner, equipo EnergiAI, jurado/evaluadores NoCountry
**Basado en:** auditoría técnica completa del repositorio (`docs/governance/AUDITORIA_PROYECTO_v1.md`, `docs/architecture/AUDITORIA_BACKEND.md`, `docs/architecture/AUDITORIA_ML.md`), contrastada con `meetings/ActaReunion-006-ENERGIAI.md`, `planning/05-Backlog-Sprint2-ENERGIAI.md` y `architecture/contracts/API_CONTRACT_V1.md`.

---

## ADENDA — 2026-08-05 — En una frase, actualizado

EnergiAI **completó el flujo end-to-end y ya está desplegado en OCI** (imágenes `:v1` en OCIR, integración real backend↔ML verificada en demo el 2026-08-04, ver `meetings/ActaReunion-008-ENERGIAI.md`). Los "hallazgos críticos" 1, 2 y 3 de este resumen (backend vacío, ML vacío, infraestructura vacía) **están resueltos**. Siguen abiertos: el hallazgo 6 (motor de recomendaciones sin dueño — ahora tiene dueño decidido por ADR-002 pero sin implementar), deuda de tests (backend y ML sin tests), y un hallazgo nuevo no cubierto en la auditoría original: `tipo_inmueble` del contrato no coincidía con las categorías reales del modelo (corregido en `API_CONTRACT_V1.md`). Detalle completo de qué se resolvió y qué sigue pendiente en `docs/local/revisiones/AUDITORIA_DOCUMENTAL_2026-08-05.md` (documento local, no versionado).

El resto de este documento se conserva sin modificar como registro histórico de la auditoría del 2026-07-31 — sección "En una frase" original a continuación.

## En una frase (registro histórico, 2026-07-31)

EnergiAI tiene **documentación, arquitectura y dataset de nivel sólido**, un **frontend funcional**, pero **cero código en backend y ML, y cero infraestructura**, lo que hace que el despliegue en OCI (Tarea #10) sea hoy inalcanzable — no por limitación de OCI, sino porque no existe todavía qué desplegar.

---

## Hallazgos críticos

1. **Backend vacío.** `backend/src/**` solo contiene marcadores `.gitkeep`. No hay `pom.xml`, no hay una sola clase Java, no hay `POST /api/v1/analisis-energetico`, no hay `GET /health`.
2. **Servicio ML vacío.** `ml-service/**` solo contiene marcadores `.gitkeep`. No hay `requirements.txt`, no hay servicio de inferencia, y **no hay modelo serializado** en ningún formato (`.pkl`/`.joblib`/`.onnx`), pese a que el dataset y su metodología de clasificación ya están validados y documentados.
3. **Infraestructura vacía.** `infra/**` solo contiene marcadores `.gitkeep`. No hay `Dockerfile`, no hay definición de infraestructura OCI, no hay pipeline CI/CD (`.github/workflows/` también vacío).
4. **Discrepancia acta vs. repositorio.** El acta del 2026-07-30 reporta las Tareas #2 (entrenar baseline) y #4 (endpoint backend) como "🟡 en ejecución", pero no hay evidencia de ese trabajo en `develop`. Debe confirmarse si existe en ramas no fusionadas o si el estado reportado reflejaba intención, no avance de código.
5. **Mismatch de contrato Frontend↔Backend.** `frontend/src/services/apiService.js` llama a `/analisis-energetico`, sin el prefijo `/api/v1` que exige el contrato oficial. Romperá la integración real si no se corrige antes de la Tarea #7.
6. **Motor de recomendaciones sin dueño arquitectónico.** La única lógica de recomendaciones que existe hoy vive en el mock de fallback del frontend, no en backend/ML como indica el flujo documentado del contrato. Ver `docs/architecture/MOTOR_RECOMENDACIONES_v1.md`.

## Lo que sí está fuerte

- **Dataset vigente** (`dataset_hibrido_v3.csv`): 50.869 filas, datos reales + metodología validada, 0 nulos, 0 duplicados, validación GroupKFold por hogar con 91,7% de accuracy documentado.
- **Arquitectura y contrato de integración**: bien definidos, congelados, con decisiones justificadas (`architecture/03-Arquitectura-Empresarial-EnergiAI.md`).
- **Frontend**: componentes completos, testeados, funcional de forma autosuficiente vía mock.
- **Gobernanza Git**: GitFlow respetado en la práctica reciente, `develop` sincronizada, sin conflictos pendientes.

## Estado por componente

| Componente | Estado | Bloqueante para OCI |
|---|---|---|
| Backend | 🔴 Sin código | Sí — crítico |
| ML Service | 🔴 Sin código, sin modelo serializado | Sí — crítico y ruta más larga |
| Infraestructura/OCI | 🔴 Sin ningún artefacto | Sí — consecuencia directa de los dos anteriores |
| Frontend | 🟡 Funcional pero desacoplado (mock) | No, pero opera sin integración real hoy |
| Dataset | ✅ Sólido | No |
| Documentación/Arquitectura | ✅ Sólida | No |

## Riesgos Sprint 2 más relevantes

- **R-04 (Despliegue OCI tardío)** — activo desde 2026-07-13, sin mitigar 18 días después. Es el riesgo que esta auditoría confirma como materializado.
- **R-03 (Contrato inestable Backend-ML)** — el contrato Frontend↔Backend está congelado, pero no existe un contrato equivalente documentado para Backend↔ML (nombre del endpoint interno, payload).
- **R-05 (Dependencia de personas clave)** — reforzado por la ausencia del Data Scientist asignado en la reunión de seguimiento más reciente.

## Recomendaciones prioritarias (orden de ejecución)

1. Iniciar **en paralelo** el proyecto Spring Boot (backend) y el proyecto Python (ML service) — ninguno depende del otro para arrancar.
2. Entrenar y **serializar** el modelo baseline sobre `dataset_hibrido_v3.csv` como artefacto versionado, no solo como resultado narrado.
3. Implementar `POST /api/v1/analisis-energetico` y `GET /health` en backend; `POST /predict` y `/health` en ML service.
4. Corregir el mismatch de ruta en `apiService.js`.
5. Escribir `Dockerfile` para ambos servicios y ejecutar el primer despliegue técnico en OCI Container Instances, siguiendo `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md` y `docs/deployment/CHECKLIST_OCI.md`.
6. Verificar el veredicto de disposición en `docs/deployment/OCI_READINESS_REPORT.md` antes de cada intento real de despliegue.

## Documentos de referencia completos

- `docs/governance/AUDITORIA_PROYECTO_v1.md`
- `docs/architecture/AUDITORIA_BACKEND.md`
- `docs/architecture/AUDITORIA_ML.md`
- `docs/deployment/OCI_READINESS_REPORT.md`
- `docs/governance/MATRIZ_DEPENDENCIAS_SPRINT2.md`
