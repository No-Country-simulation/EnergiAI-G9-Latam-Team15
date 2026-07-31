# Estado de Entregables — NoCountry (Hackathon Oracle + Alura + NoCountry)

**Fecha:** 2026-07-31
**Fuente:** lista de recursos posibles mencionada en `meetings/ActaReunion-006-ENERGIAI.md` §7 ("Entregables NoCountry"), contrastada con evidencia real del repositorio.

> Este documento no inventa requisitos formales de NoCountry no mencionados en el repo — se limita a auditar, con evidencia, los ítems que el propio equipo ya identificó como entregables posibles en el acta 006. Si NoCountry exige entregables adicionales no documentados aquí, deben incorporarse en la próxima acta.

---

## 1. Estado por entregable

| Entregable | Estado | Evidencia | Acción pendiente |
|---|---|---|---|
| GitHub oficial | ✅ Listo | Repositorio activo, GitFlow en uso, PRs #1-#5 fusionados con revisión | Ninguna — mantener disciplina de PR |
| Documentación | ✅ Fuerte | `architecture/`, `docs/`, `planning/`, `README.md` completos y consistentes | Gap heredado ya cerrado en esta reorganización (`docs/00-Indice-Arquitectura.md` actualizado) — ver `ESTADO-PROYECTO.md` |
| Arquitectura | ✅ Fuerte | 3 documentos de arquitectura + 2 diagramas C4 + contrato de integración v1.0 | Falta diagrama C4 Nivel 3 (Componentes) y diagrama de secuencia del flujo principal — no bloqueante, sí deseable antes de la demo final |
| Figma (si existe enlace) | ❓ Sin evidencia en el repo | No hay referencia a Figma en ningún documento auditado | Confirmar con el equipo si existe un enlace y, de ser así, documentarlo en `README.md` / `assets/` |
| Frontend desplegado | 🔴 No desplegado | `frontend/` es funcional localmente (`npm run dev`) pero no hay evidencia de despliegue (Vercel/Netlify/OCI estático) en el repo | Desplegar como sitio estático — bajo esfuerzo, no depende de backend/ML por el mock de fallback |
| Backend desplegado | 🔴 No desplegado — y no existe código que desplegar | Ver `docs/architecture/AUDITORIA_BACKEND.md` | Depende de Tareas #4, #9 y del Plan de Despliegue OCI |
| OCI (evidencia de uso) | 🔴 Sin evidencia | `infra/` vacío, sin capturas, logs ni configuración documentada | Depende de la ejecución de `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md` |
| Video demostrativo | ❓ Sin evidencia en el repo | No hay referencia en `assets/presentations/` (carpeta con solo `.gitkeep`) | Planificar grabación una vez el flujo end-to-end esté integrado (Tarea #7) — es el último entregable en la secuencia natural |

---

## 2. Assets de soporte (branding, diagramas exportados, screenshots, presentaciones)

Todas las subcarpetas de `assets/` contienen únicamente `.gitkeep`:

- `assets/branding/` — sin logos ni identidad visual versionados (el frontend sí tiene `frontend/public/logo_energiAI.png`, que podría promoverse aquí para consistencia).
- `assets/diagrams/` — sin exportaciones visuales (los diagramas C4 existen solo como Markdown/ASCII en `diagrams/`, no como imágenes exportadas).
- `assets/presentations/` — sin material de pitch.
- `assets/screenshots/` — sin capturas del producto, pese a que el frontend ya es funcional y podría capturarse hoy mismo.

**Acción de bajo esfuerzo y alto impacto para NoCountry:** generar capturas de pantalla del frontend funcional (formulario, semáforo, historial, recomendaciones) y depositarlas en `assets/screenshots/` — esto no depende de ningún bloqueo técnico backend/ML/OCI y mejora inmediatamente la evidencia demostrable del proyecto.

---

## 3. Priorización para cierre de entregables NoCountry

| Prioridad | Entregable | Por qué esta prioridad |
|---|---|---|
| P0 | Backend + ML desplegados en OCI | Es el entregable técnico más exigente y el que más tiempo de ejecución requiere; sin él, "OCI" y "Backend desplegado" quedan en rojo |
| P1 | Frontend desplegado | Bajo esfuerzo, alto impacto visual para el jurado; no depende de nada bloqueado |
| P1 | Screenshots del producto funcionando | Cero dependencias técnicas, se puede hacer hoy |
| P2 | Video demostrativo | Debe grabarse después de la integración real (Tarea #7), para no mostrar solo el mock |
| P2 | Diagrama C4 Nivel 3 + diagrama de secuencia | Refuerza la narrativa técnica ante el jurado, no bloquea nada |
| P3 | Confirmar/enlazar Figma | Bajo esfuerzo, pendiente de confirmación con el equipo, no crítico si el diseño ya está reflejado en el frontend implementado |

---

## 4. Riesgo de narrativa ante el jurado

Si la demo final se presenta antes de resolver los hallazgos de `AUDITORIA_BACKEND.md` y `AUDITORIA_ML.md`, el equipo dependerá exclusivamente del mock de `apiService.js` para mostrar el flujo — que es funcional pero **no demuestra integración real ni uso de OCI**, que son justamente los criterios que este set de documentos busca dejar resueltos a tiempo. El plan de contingencia ya está anticipado en `planning/04-Gestion-de-Riesgos-Arquitectonicos.md` ("si falla la integración backend-ML, congelar interfaz con stub controlado para sostener la demo") — es una salida válida solo si se declara explícitamente en la presentación, no si se presenta como integración real.
