# Acta de Reunión 009 — Proyecto EnergiAI (G9-LATAM Team 15)

**Fecha:** 6 de agosto de 2026, 11:30am (Colombia)
**Modalidad:** Virtual (Discord)
**Simulación:** NoCountry — Hackathon ONE G9-LATAM (Oracle / Alura)
**Asistentes:** Harrinson, Alonso , Elvis, Bernardo
**Elaborada por:** Bernardo Gómez — Solution / Software Architect

---

## 1. Estado desde la última acta (008, 4-ago)

Desde la demo end-to-end del 4 de agosto, el 5 de agosto se dedicó por completo a documentación y gobernanza de repositorio (sin tocar código de ningún servicio), mientras se esperaban las correcciones del equipo. Se mergearon 4 PRs de documentación: #17 (arquitectura, contratos y diagramas actualizados a la realidad desplegada — 2 ADR, contrato interno Backend↔ML, C4 Nivel 3, diagrama de secuencia, adendas en las 9 auditorías de julio, `infra/oci/README.md` con datos reales del despliegue), #18 (README renovado con banner y badges), #20 (fix de nombre en la tabla de equipo), y un PR adicional que renombró `.github/README.md` → `.github/CONFIGURACION.md` para que GitHub vuelva a mostrar el banner en la portada del repo en vez de "GitHub Configuration". También se hizo limpieza de ramas (3 locales y 8 remotas ya fusionadas, incluida `revert-pr10-main`). El despliegue en OCI sigue **ACTIVO** sin cambios desde entonces (http://149.130.187.192).

## 2. Avance general estimado

~75-80% (técnico/infra prácticamente cerrado; notebook, motor de recomendaciones, video y ajustes del equipo son el tramo final concreto que falta).

## 3. Pendientes por responsable

| Quién | Qué se le pidió | Estado |
|---|---|---|
| Alonso | Ortografía frontend/tooltips, legibilidad eje X de la gráfica | 🟡 PR #22 abierto con el trabajo completo (ortografía, gráfica fecha-hora, PDF, historial con localStorage) — pendiente un ajuste menor en el selector de tipo_inmueble para alinear las opciones con las 2 categorías reales del modelo ("Casa" / "Pequeño establecimiento"). Seguimiento en curso, se mergea en cuanto quede listo. |
| Cristian + Harrinson | Enriquecer recomendaciones, explorar más valor del modelo | ✅ Cristian compartió reglas_recomendaciones.md (6 reglas + estimación de ahorro potencial 3%/5%/8%), portado al backend por Bernardo (PR #25) — cierra ADR-002. |
| Harrinson | Score de eficiencia 0-100 (predict_proba) en ml-service | ✅ Entregado en 2 PRs: score_eficiencia continuo en ml-service (PR #24) + suite de 27 tests del ml-service (PR #23, ml-service/tests/ estaba vacío). |
| Elvis + Carlos | Soporte backend si los cambios de recomendaciones lo requieren | No se requirió — Bernardo implementó directo el motor de recomendaciones y el cableado de score/prioridad. |
| Luis Ángel (PO) | Priorizar qué mejoras entran en la demo final | Sin confirmar aún al cierre de esta acta. |
| Bernardo | Redespliegue OCI cuando las mejoras estén en develop; score de priorización en backend | ✅ Score de priorización implementado y cableado (PR #26). Redespliegue OCI: en espera de integrar los últimos ajustes de frontend, para hacer un solo redespliegue final con todo junto en vez de varios parciales. |

## 4. Ruta crítica pendiente

1. ✅ Notebook de Ciencia de Datos — completado hoy (EDA, transformación, entrenamiento, evaluación, recomendaciones, serialización, + extra de detección de anomalías con IsolationForest). Pendiente: PR para subirlo a develop.
2. ✅ Motor de recomendaciones real en backend (ADR-002) — completado, ver PR #25.
3. 🔴 Redespliegue final en OCI con todas las mejoras integradas — sigue pendiente, bloqueado por el ajuste de Alonso en PR #22.
4. 🔴 Video demo — sin avance, sigue en 0%.
5. 🔴 Completar tareas 2, 3 y 4 de la plataforma NoCountry — sin avance.

## 5. Fechas de cierre acordadas

- Esta semana (Sprint 3): pulir todo lo de arriba.
- Semana del 10-16 ago, máximo viernes 14-ago: TODO listo (video, tareas NoCountry, redespliegue final).
- Semana del 17-27 ago: presentación/Demo Day, sin más cambios de código.

## 6. Acuerdos de esta reunión

- Priorizar la implementación de (a) score de eficiencia continuo y (c) score de priorización sobre (b) detección de anomalías; esta última se documenta en el notebook de Ciencia de Datos en vez de desplegarse en producción, para no arriesgar el redespliegue previo a la demo.
- Esperar el ajuste de Alonso (tipo_inmueble) antes de integrar todo el frontend y hacer el redespliegue final en OCI.
- Meta de cierre confirmada: viernes 14-ago con todo listo (video grabado, 4 tareas de NoCountry completas, redespliegue final en OCI).

## 7. Próxima reunión

Lunes 10 de agosto de 2026, 11:30am (Discord).

---

*Acta elaborada como registro oficial del proyecto. Ubicación: `meetings/ActaReunion-009-ENERGIAI.md`.*
