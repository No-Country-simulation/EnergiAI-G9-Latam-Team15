# Riesgos Operativos — Sprint 2 (Ventana 48-72h)

**Fecha:** 2026-07-31
**Alcance:** riesgos de **continuidad operativa** para la ventana viernes 2026-07-31 → lunes 2026-08-03. No reemplaza la matriz de riesgos arquitectónicos de `planning/04-Gestion-de-Riesgos-Arquitectonicos.md` (vigente para todo el proyecto) — la complementa con foco en "qué puede impedir que el fin de semana produzca un despliegue OCI real", con probabilidad y responsable evaluados sobre evidencia del repositorio, no sobre intención declarada.

**Criterio de probabilidad de incumplimiento:**
- **Alta** = hoy no existe ningún artefacto que respalde que la tarea se completará a tiempo.
- **Media** = existe intención/asignación declarada pero sin evidencia verificable de avance.
- **Baja** = existe evidencia de avance real (código, artefacto, o dependencia ya resuelta).

---

## 1. Matriz de riesgos operativos

| ID | Riesgo | Área | Probabilidad de incumplimiento | Impacto sobre OCI | Responsable | Mitigación |
|---|---|---|---|---|---|---|
| RO-01 | El modelo baseline no queda entrenado y serializado antes del domingo | ML | **Alta** — sin artefacto `.pkl`/`.joblib` en el repo a la fecha | Crítico — bloquea el servicio ML y, por extensión, el despliegue completo | Harrinson Villabona (Data Scientist) / Bernardo como respaldo | `PLAN_CONTINGENCIA_OCI.md` Escenario 1 |
| RO-02 | El backend no tiene endpoint funcional antes del domingo | Backend | **Alta** — sin `pom.xml` ni código a la fecha | Crítico — sin backend no hay nada que exponer públicamente | Carlos Fabian Mesa / Elvis Trinidad / Bernardo como respaldo | `PLAN_CONTINGENCIA_OCI.md` Escenario 2 |
| RO-03 | La cuenta/tenancy OCI no está confirmada o accesible | Infraestructura | **Media-Alta** — sin evidencia en el repositorio de que esté resuelto | Crítico — sin cuenta no hay despliegue posible, sin importar qué tan listo esté el código | Luis Angel Chavez Mejía (PO) / Bernardo | `PLAN_CONTINGENCIA_OCI.md` Escenario 4 — verificar HOY, no el domingo |
| RO-04 | El frontend no logra integrarse con el backend real a tiempo para la demo | Frontend / Integración | **Media** — el mismatch de ruta (`/analisis-energetico` vs `/api/v1/analisis-energetico`) ya está identificado pero no corregido | Bajo para OCI en sí (no bloquea el despliegue de backend/ML), Medio para la narrativa de demo | Alonso Carbajal | `PLAN_CONTINGENCIA_OCI.md` Escenario 3 — el mock sostiene la demo si es necesario |
| RO-05 | Miembros clave (PO, Data Scientist) no disponibles durante el fin de semana | Equipo | **Confirmada como riesgo activo** — ambos ausentes en la última reunión registrada (2026-07-30) | Alto indirecto — retrasa RO-01 y RO-03 si no hay quien las resuelva | Product Owner / equipo | Bernardo asume las tareas ejecutables sin ellos (ver `ESTADO_OPERATIVO_SPRINT2.md` §7); comunicación async explícita hoy mismo |
| RO-06 | Contrato interno Backend↔ML no está definido (nombre de endpoint, payload) | Integración | **Alta** — no existe ningún documento que lo fije, a diferencia del contrato Frontend↔Backend que sí está congelado | Alto — backend y ML pueden construirse de forma incompatible si trabajan en paralelo sin este acuerdo | Bernardo (Architect) | Definir y documentar antes de que ambos equipos avancen en paralelo — acción de hoy viernes |
| RO-07 | `Dockerfile` o build de imagen falla por primera vez el mismo domingo | Infraestructura | **Media** — nunca se ha probado, no hay Dockerfile hoy | Alto — un fallo de build el domingo consume tiempo que no sobra | Bernardo / quien construya cada servicio | Probar `docker build` en sábado, no en domingo (ver `ESTADO_OPERATIVO_SPRINT2.md`, flujo del sábado) |
| RO-08 | Scope creep de último momento (agregar funcionalidad no crítica) | Gestión | **Media** — riesgo estructural ya señalado en `planning/04` como R-06 | Medio — resta tiempo a lo que sí bloquea el despliegue | Todo el equipo | Congelar alcance el sábado por la noche (ver checklist); cualquier idea nueva va a backlog post-fin de semana |
| RO-09 | El modelo entrenado en contingencia (Escenario 1) tiene calidad notablemente menor a la reportada (91,7%) | ML | **Media** — depende de tiempo disponible para replicar correctamente el GroupKFold por hogar | Bajo para el despliegue en sí (igual es servible), Medio para la narrativa de calidad ante NoCountry | Quien ejecute el entrenamiento de contingencia | Documentar explícitamente como "baseline v0 de contingencia" si aplica, sin presentarlo como resultado final |

---

## 2. Riesgos con menor probabilidad (monitorear, no accionar de inmediato)

| ID | Riesgo | Probabilidad | Nota |
|---|---|---|---|
| RO-10 | El dataset o la metodología de clasificación necesitan retrabajo | **Baja** | Ya validado y documentado (`INFORME_HIBRIDO_v3.md`); sin cambios recientes |
| RO-11 | El frontend deja de funcionar o regresiona | **Baja** | Suite de tests existente, sin cambios planeados sobre `frontend/` este fin de semana |
| RO-12 | Se pierde trabajo por conflictos de Git durante el fin de semana | **Baja** | GitFlow respetado en la práctica reciente; mitigar solo si varias personas tocan `backend/`/`ml-service/` simultáneamente sin coordinar ramas |

---

## Hallazgo — 2026-08-01: `develop` y `main` desalineados

Verificado con `git log`: `origin/develop` está 7 commits adelante de
`origin/main` (dataset híbrido v3, frontend completo, documentación de
data-engineering, actas 005/006 — ~68.700 líneas de diferencia). No existe
en ningún documento del repositorio (backlog, plan de despliegue, actas)
una fecha o decisión explícita de cuándo se mergeará `develop` a `main`.

**Riesgo:** si NoCountry o el jurado evalúan el repositorio mirando `main`
(rama por defecto), verían una versión desactualizada del proyecto — sin
dataset, sin frontend, sin la documentación reciente.

**Acción recomendada:** confirmar con el Product Owner y el equipo cuándo
se planea el merge `develop` → `main` (¿al cierre de Sprint 2? ¿justo
antes de la demo final?). No es bloqueante para el despliegue OCI de este
fin de semana, pero sí debe resolverse antes de la entrega final.

**Responsable de escalar:** Bernardo Gómez Montoya (Architect).

---

## 3. Relación con la matriz de riesgos arquitectónicos vigente

`planning/04-Gestion-de-Riesgos-Arquitectonicos.md` ya identificaba R-04 (despliegue OCI tardío) como crítico desde el 2026-07-13. Esta matriz operativa es la traducción de ese riesgo, y de R-02/R-03/R-05, a una ventana de tiempo concreta (48-72h) con probabilidad evaluada sobre evidencia actual, no sobre el riesgo general del proyecto. Si al cierre del domingo (`docs/governance/CHECKLIST_DOMINGO_DESPLIEGUE.md`) alguno de estos riesgos se materializó, debe reflejarse también en la matriz original de `planning/04` el lunes.

---

## 4. Umbral de escalamiento

Cualquier riesgo marcado como **Alta** probabilidad que siga sin mitigar al **sábado a las 18:00** debe escalarse explícitamente (mensaje directo al responsable + aviso al Product Owner), no esperar al domingo para descubrir que no se resolvió. Este es el único punto de control duro de este documento — todo lo demás es seguimiento continuo.
