# Estado Operativo — Sprint 2 (Continuidad 48 horas)

**Fecha de corte:** viernes 2026-07-31, tarde
**Ventana de continuidad cubierta:** viernes 2026-07-31 → lunes 2026-08-03
**Propósito:** que el proyecto pueda avanzar sin bloqueos aunque uno o más integrantes no respondan durante el fin de semana. Este documento asume que **Bernardo (Software/Solution Architect) es quien sostiene la continuidad operativa** si algún responsable nominal no está disponible.
**No modifica código.** Es un documento de gestión y gobernanza.

> Lectura previa recomendada: `docs/governance/RESUMEN_EJECUTIVO_AUDITORIA_SPRINT2.md` y `docs/deployment/OCI_READINESS_REPORT.md` (auditoría técnica de base, 2026-07-31, sin cambios desde entonces — verificado en esta sesión).

---

## 1. Resumen operativo

El repositorio no cambió desde la auditoría técnica de esta misma fecha: `backend/`, `ml-service/` e `infra/` siguen sin código versionado (solo `.gitkeep`/`README.md`). Eso significa que **todo el trabajo crítico del fin de semana está por hacer**, no por terminar de integrar. La prioridad no es "pulir" — es "hacer existir" el backend, el modelo serializado y el servicio ML, en ese orden de urgencia, y dejar decisiones de contingencia ya tomadas para no perder tiempo de ejecución discutiéndolas el domingo bajo presión.

---

## 2. Matriz RAG por área

| Área | Estado | Justificación | Acción si no es 🟢 |
|---|---|---|---|
| **Dataset** | 🟢 Verde | `dataset_hibrido_v3.csv` validado, documentado, sin cambios desde la última auditoría | Ninguna — no tocar, es la única pieza terminada de punta a punta |
| **Frontend** | 🟢 Verde | Componentes completos, tests pasando, funcional de forma autosuficiente vía mock | Ninguna — solo pendiente de corregir la ruta de `apiService.js` cuando el backend exista |
| **Documentación / Gobernanza** | 🟢 Verde | Recién reorganizada (`docs/architecture/`, `docs/deployment/`, `docs/governance/`), auditoría completa disponible | Mantener actualizada tras el fin de semana (Tarea Lunes, §6) |
| **Backend** | 🔴 Rojo | Cero código versionado; sin `pom.xml`; endpoint y health inexistentes | Ver `docs/deployment/PLAN_CONTINGENCIA_OCI.md` Escenario 2 |
| **ML Service** | 🔴 Rojo | Cero código versionado; modelo no serializado pese a metodología ya validada | Ver `docs/deployment/PLAN_CONTINGENCIA_OCI.md` Escenario 1 — es la ruta más larga y el mayor riesgo del fin de semana |
| **Infraestructura / OCI** | 🔴 Rojo | Sin `Dockerfile`, sin IaC, sin confirmación de tenancy/cuenta OCI en el repositorio | Ver `docs/deployment/PLAN_CONTINGENCIA_OCI.md` Escenario 4 — **verificar cuenta OCI hoy viernes, no el domingo** |
| **Integración Backend ↔ ML** | 🔴 Rojo | Depende de que ambos existan; no evaluable todavía | Consecuencia directa de los dos anteriores |
| **Integración Frontend ↔ Backend** | 🟡 Amarillo | Frontend listo para conectar, pero hay mismatch de ruta documentado (`/analisis-energetico` vs `/api/v1/analisis-energetico`) y depende de que el backend exista | Corregir la ruta apenas el backend esté desplegable; mientras tanto el mock sostiene la demo |
| **Disponibilidad del equipo** | 🟡 Amarillo | Ver §5 — 4 de 8 roles activos en la última reunión (2026-07-30); Product Owner y Data Scientist ausentes | Confirmar disponibilidad real hoy mismo (mensaje directo, no esperar próxima acta) |

**Lectura de la matriz:** 3 áreas en rojo (Backend, ML, Infra/OCI) son exactamente las que bloquean el despliegue OCI — coincide con `docs/deployment/OCI_READINESS_REPORT.md`. Ninguna sorpresa nueva; lo que cambia hoy es que hay una ventana de 48-72h concreta para resolverlas antes del lunes.

---

## 3. Estado por componente (síntesis — detalle completo en las auditorías previas)

| Componente | Auditoría de referencia | Hallazgo clave |
|---|---|---|
| Backend | `docs/architecture/AUDITORIA_BACKEND.md` | Sin `pom.xml`; ni el endpoint ni `/health` existen |
| ML Service | `docs/architecture/AUDITORIA_ML.md` | Sin `requirements.txt`; modelo solo documentado, no serializado |
| Motor de recomendaciones | `docs/architecture/MOTOR_RECOMENDACIONES_v1.md` | Vive en el mock del frontend; sin dueño arquitectónico decidido |
| Infraestructura OCI | `docs/deployment/OCI_READINESS_REPORT.md` | Veredicto: NO desplegable hoy; tabla de responsables por gap |
| Dependencias del backlog | `docs/governance/MATRIZ_DEPENDENCIAS_SPRINT2.md` | Camino crítico: Tarea 2 → 3 → 5 → 6 → 10 (ML es la ruta más larga) |

---

## 4. Dependencias críticas, responsables y plan si no responden

| Dependencia crítica | Responsable nominal (`planning/01-Roles.md`) | Qué hace Bernardo si no hay respuesta en 24h |
|---|---|---|
| Entrenar + serializar modelo baseline | Harrinson Villabona (Data Scientist) | Ejecutar él mismo la metodología ya documentada en `docs/data-engineering/INFORME_HIBRIDO_v3.md` §4 (score multicriterio, ya resuelta) sobre `dataset_hibrido_v3.csv`; no requiere rediseño, solo ejecución (ver Escenario 1 de `PLAN_CONTINGENCIA_OCI.md`) |
| Endpoint `POST /api/v1/analisis-energetico` + `/health` | Carlos Fabian Mesa / Elvis Trinidad (Backend) | Implementar un backend mínimo él mismo o evaluar el fallback de Escenario 2 (`PLAN_CONTINGENCIA_OCI.md`) |
| Confirmación de tenancy/cuenta OCI | Luis Angel Chavez Mejía (Product Owner) | Verificar acceso directamente en la consola OCI hoy viernes; si no hay cuenta, escalar de inmediato — es la dependencia con menor margen de tiempo |
| Redistribución del rol de Data Engineer (Tarea #16 del backlog) | Product Owner + equipo | No bloquea el fin de semana técnico; diferir a la reunión del lunes |
| Aprobación formal del Backlog Sprint 2 (Tarea #15) | Product Owner | No bloquea la ejecución técnica — el equipo ya está actuando sobre la propuesta; formalizar el lunes |

---

## 5. Disponibilidad del equipo (evidencia, no suposición)

Según `meetings/ActaReunion-006-ENERGIAI.md` (2026-07-30, la más reciente):

| Rol | Integrante | Presente en última reunión |
|---|---|---|
| Software Architect | Bernardo Adolfo Gómez Montoya | ✅ Sí |
| Full Stack | Alonso Carbajal | ✅ Sí |
| Data Analyst | Magno Cristian Coronel Salazar | ✅ Sí |
| Backend Developer | Elvis Leniker Trinidad Caldas | ✅ Sí |
| Backend Developer | Carlos Fabian Mesa | ❌ No registrado |
| Data Scientist | Harrinson Villabona | ❌ No registrado |
| Data Engineer | Anayely Reyes | ❌ No registrado (su continuidad en el rol ya está en discusión, Tarea #16 del backlog) |
| Product Owner | Luis Angel Chavez Mejía | ❌ No registrado |

**Lectura operativa:** de los dos responsables del bloque más crítico (ML: Harrinson; Backend: Carlos Fabian), solo Elvis (Backend) confirmó presencia reciente. Esto no significa que los ausentes no vayan a trabajar — pero para efectos de este plan de continuidad, **se asume que Bernardo debe estar en condiciones de avanzar el modelo baseline y el esqueleto de backend sin depender de que aparezcan**, usando los fallbacks de `docs/deployment/PLAN_CONTINGENCIA_OCI.md`.

---

## 6. Flujo operativo — Viernes a Lunes, con prioridades exactas

### Viernes 2026-07-31 (resto del día)

- **P0** — Bernardo: verificar acceso a la cuenta/tenancy OCI del hackathon. No esperar al domingo.
- **P0** — Bernardo + quien esté disponible: iniciar en paralelo el esqueleto del backend (`pom.xml`, estructura de paquetes) y el proyecto ML (`requirements.txt`, entrenamiento del baseline). Ninguno depende del otro para arrancar.
- **P1** — Bernardo: mensaje directo (no solo acta) a Harrinson, Carlos Fabian y Luis Angel confirmando disponibilidad real para el fin de semana.
- **P1** — Congelar el contrato interno Backend↔ML (nombre del endpoint, payload) — hoy no existe documentado, y sin él el servicio ML y el backend pueden construirse de forma incompatible.

### Sábado 2026-08-01

- **P0 (mañana)** — Modelo baseline entrenado y **serializado** (artefacto real, no solo métrica documentada). Si no ocurre para el mediodía, activar Escenario 1 de `PLAN_CONTINGENCIA_OCI.md`.
- **P0 (mañana)** — Backend con `POST /api/v1/analisis-energetico` y `GET /health` funcionando localmente. Si no ocurre para el mediodía, activar Escenario 2.
- **P0 (tarde)** — Integración local Backend ↔ ML probada (dos servicios corriendo, petición real de extremo a extremo, aunque sea en dos terminales o `docker-compose` local).
- **P1 (tarde)** — `Dockerfile` de ambos servicios construido y probado localmente (`docker build` + `docker run` + `curl /health`).
- **P2 (noche)** — Congelar alcance: nada nuevo se agrega después de este punto salvo que resuelva un bloqueador. Revisar `docs/governance/CHECKLIST_DOMINGO_DESPLIEGUE.md` antes de dormir para saber exactamente qué toca al día siguiente.

### Domingo 2026-08-02 — Día de despliegue

Ejecutar `docs/governance/CHECKLIST_DOMINGO_DESPLIEGUE.md` de punta a punta. Resumen de bloques:

- **Mañana:** cuenta OCI, VCN, OCIR, build y push de imágenes.
- **Mediodía:** despliegue de Container Instances (ML primero, backend después).
- **Tarde:** validación end-to-end real + captura de evidencia.
- **Noche:** decisión go/no-go sobre integración Frontend↔Backend real para la demo (ver Escenario 3 de `PLAN_CONTINGENCIA_OCI.md` si no se logra), cierre del día y actualización de estado.

### Lunes 2026-08-03

- **P0** — Reunión de cierre del fin de semana: ¿qué se logró, qué contingencia se activó, qué queda pendiente?
- **P0** — Actualizar `planning/05-Backlog-Sprint2-ENERGIAI.md` y `docs/governance/MATRIZ_DEPENDENCIAS_SPRINT2.md` con el estado real (no el proyectado).
- **P1** — Si se activó alguna contingencia, definir el plan de reemplazo por la versión definitiva (p. ej. si el backend del fin de semana fue un stub, planificar cuándo se reemplaza por la versión completa en Spring Boot).
- **P1** — Trasladar evidencia del despliegue a `docs/governance/ENTREGABLES_NOCOUNTRY.md`.
- **P2** — Redactar/actualizar acta de reunión formal siguiendo el formato de `meetings/ActaReunion-006-ENERGIAI.md`.

---

## 7. Qué puede hacer Bernardo solo, sin depender de terceros, en las próximas 48 horas

Esta sección existe porque el objetivo explícito de este documento es continuidad sin bloqueos. Lista de acciones que **no requieren esperar respuesta de nadie**:

1. Verificar y, si es necesario, gestionar el acceso a la cuenta OCI.
2. Inicializar el proyecto Spring Boot (`pom.xml`, estructura) — es trabajo de andamiaje, no requiere al Data Scientist.
3. Ejecutar la metodología de entrenamiento ya documentada en `docs/data-engineering/INFORME_HIBRIDO_v3.md` sobre el dataset, si Harrinson no está disponible — la metodología ya está resuelta y validada, solo falta ejecutarla y serializar el resultado.
4. Escribir los `Dockerfile` de ambos servicios en cuanto exista código mínimo que contenerizar.
5. Documentar la infraestructura OCI (VCN, Container Instances) siguiendo `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md`, que ya está completo.
6. Corregir el mismatch de ruta en `frontend/src/services/apiService.js` en cuanto el backend defina su ruta final.
7. Mantener actualizado este documento y `docs/governance/RIESGOS_OPERATIVOS_SPRINT2.md` a medida que cambie el estado real.

---

## 8. Documentos relacionados

- `docs/governance/RIESGOS_OPERATIVOS_SPRINT2.md`
- `docs/deployment/PLAN_CONTINGENCIA_OCI.md`
- `docs/governance/CHECKLIST_DOMINGO_DESPLIEGUE.md`
- `docs/deployment/OCI_READINESS_REPORT.md`
- `docs/governance/MATRIZ_DEPENDENCIAS_SPRINT2.md`
