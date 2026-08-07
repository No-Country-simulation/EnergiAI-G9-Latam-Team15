# Indice Maestro de Documentacion Arquitectonica

**Fecha:** 2026-07-16
**Última actualización:** 2026-08-05 — proyecto ya desplegado en OCI; se agregan ADRs, contrato interno Backend↔ML, diagramas C4 Nivel 3/secuencia y actas 006-008.
**Objetivo:** Consolidar la documentacion principal de EnergiAI como referencia oficial para el equipo durante el Hackathon Oracle + Alura + NoCountry, garantizando trazabilidad, coherencia arquitectonica y alineacion entre las diferentes areas del proyecto.

---

## Documentos principales

### Arquitectura

- `architecture/01-Vision-General.md`
- `architecture/02-Arquitectura-Propuesta.md`
- `architecture/03-Arquitectura-Empresarial-EnergiAI.md`
- `architecture/contracts/API_CONTRACT_V1.md` — contrato Frontend↔Backend
- `architecture/contracts/CONTRATO_INTERNO_BACKEND_ML.md` — contrato Backend↔ML Service (nuevo, 2026-08-05)

### Decisiones arquitectónicas (ADR)

- `architecture/decisions/ADR-001-contrato-integracion-v1.md`
- `architecture/decisions/ADR-002-motor-recomendaciones-backend.md`

### Diagramas

- `diagrams/01-C4-Nivel-1-Contexto.md`
- `diagrams/02-C4-Nivel-2-Contenedores.md` — actualizado 2026-08-05 a la arquitectura real desplegada
- `diagrams/03-C4-Nivel-3-Componentes.md` — nuevo, componentes del Backend
- `diagrams/04-Diagrama-Secuencia-Analisis-Energetico.md` — nuevo, flujo end-to-end + camino de fallo

### Gobierno Tecnico y Arquitectura

- `docs/01-Estructura-Repositorio-y-GitFlow.md`
- `docs/02-Revision-Arquitectonica-y-Version-Optimizada.md`
- `docs/03-Guia-Maestra-Proyecto-EnergiAI.md`

### Auditoria Tecnica y Despliegue OCI (Sprint 2)

> Documentos diagnosticos (no normativos): evaluan el estado real del codigo frente a la especificacion de `architecture/` y `planning/`. Ver `docs/architecture/README.md` para la distincion con la carpeta `architecture/` de la raiz.

- `docs/governance/RESUMEN_EJECUTIVO_AUDITORIA_SPRINT2.md` — lectura recomendada primero (sintesis ejecutiva)
- `docs/governance/AUDITORIA_PROYECTO_v1.md`
- `docs/architecture/AUDITORIA_BACKEND.md`
- `docs/architecture/AUDITORIA_ML.md`
- `docs/architecture/MOTOR_RECOMENDACIONES_v1.md`
- `docs/deployment/OCI_READINESS_REPORT.md`
- `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md`
- `docs/deployment/CHECKLIST_OCI.md`
- `docs/governance/MATRIZ_DEPENDENCIAS_SPRINT2.md`
- `docs/governance/ENTREGABLES_NOCOUNTRY.md`

### Continuidad Operativa 48h y Despliegue del Fin de Semana (Sprint 2)

> Generados 2026-07-31 para sostener el proyecto sin bloqueos si algun integrante no participa durante el fin de semana de despliegue. Empezar por `ESTADO_OPERATIVO_SPRINT2.md`.

- `docs/governance/ESTADO_OPERATIVO_SPRINT2.md` — matriz RAG por area, dependencias criticas y flujo operativo Viernes-Lunes
- `docs/governance/RIESGOS_OPERATIVOS_SPRINT2.md` — riesgos de continuidad con probabilidad de incumplimiento e impacto sobre OCI
- `docs/deployment/PLAN_CONTINGENCIA_OCI.md` — que hacer si ML/Backend/Frontend/OCI fallan, decisiones pre-autorizadas por escenario
- `docs/governance/CHECKLIST_DOMINGO_DESPLIEGUE.md` — guion operativo del dia de despliegue, en bloques horarios

### Data Engineering

- `docs/data-engineering/Dataset_Research_Report_v1.md`
- `docs/data-engineering/Dataset_Strategy_v1.md`
- `docs/data-engineering/INFORME_CONSOLIDACION_DATASET.md`
- `docs/data-engineering/NOTA_ARQUITECTO_Dataset_v2.md`
- `docs/data-engineering/INFORME_HIBRIDO_v3.md`

### Actas y Seguimiento

- `meetings/ActaReunion-001-ENERGIAI.md`
- `meetings/ActaReunion-002-ENERGIAI.md`
- `meetings/ActaReunion-003-ENERGIAI.md`
- `meetings/ActaReunion-004-ENERGIAI.md`
- `meetings/ActaReunion-005-ENERGIAI.md`
- `meetings/ActaReunion-006-ENERGIAI.md`
- `meetings/ActaReunion-007-ENERGIAI.md` — demo end-to-end local + imágenes en OCIR
- `meetings/ActaReunion-008-ENERGIAI.md` — reparto de mejoras post-demo, despliegue OCI en curso

### Planeacion

- `planning/01-Roles.md`
- `planning/02-Riesgos.md`
- `planning/03-Roadmap-Tecnico-5-Semanas.md`
- `planning/04-Gestion-de-Riesgos-Arquitectonicos.md`
- `planning/05-Backlog-Sprint2-ENERGIAI.md`

---

## Orden sugerido de lectura

1. Vision general.
2. Arquitectura empresarial y alcance del MVP.
3. Guia Maestra del proyecto.
4. Revision arquitectonica y version optimizada.
5. Diagramas C4.
6. Estructura del repositorio y GitFlow.
7. Actas de reuniones y decisiones del Sprint 0.
8. Roadmap tecnico.
9. Riesgos y gestion arquitectonica.
10. Backlog Sprint 2 (`planning/05-Backlog-Sprint2-ENERGIAI.md`).
11. Auditoria tecnica Sprint 2 — empezar por `docs/governance/RESUMEN_EJECUTIVO_AUDITORIA_SPRINT2.md`, luego `docs/deployment/OCI_READINESS_REPORT.md`.

---

## Documentos rectores vigentes

Los documentos considerados fuente oficial de referencia para Sprint 1 son:

- `README.md`
- `docs/03-Guia-Maestra-Proyecto-EnergiAI.md`
- `architecture/03-Arquitectura-Empresarial-EnergiAI.md`
- `docs/01-Estructura-Repositorio-y-GitFlow.md`
- `planning/03-Roadmap-Tecnico-5-Semanas.md`
- `planning/04-Gestion-de-Riesgos-Arquitectonicos.md`

Documentos rectores adicionales para Sprint 2 (auditoria y despliegue OCI):

- `planning/05-Backlog-Sprint2-ENERGIAI.md`
- `docs/governance/RESUMEN_EJECUTIVO_AUDITORIA_SPRINT2.md`
- `docs/deployment/OCI_READINESS_REPORT.md`

---

## Alcance oficial del MVP

El MVP oficial de EnergiAI se enfoca en:

```text
Usuario Residencial
```