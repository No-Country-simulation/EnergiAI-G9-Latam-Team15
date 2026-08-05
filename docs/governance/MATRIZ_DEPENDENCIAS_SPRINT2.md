# Matriz de Dependencias — Backlog Sprint 2

**Fecha:** 2026-07-31
**Fuente:** `planning/05-Backlog-Sprint2-ENERGIAI.md` (propuesta) contrastada con `meetings/ActaReunion-006-ENERGIAI.md` (estado reportado en la reunión del 2026-07-30) y con el estado real observado en el repositorio en esta auditoría.

> Nota metodológica: la columna "Estado real (repo)" refleja lo verificable en `develop` a 2026-07-31, no lo declarado en actas. Donde ambos difieren, se marca explícitamente — es la señal más importante de esta matriz.

---

## 1. Tabla de dependencias y estado

| # | Tarea | Depende de | Estado (Acta 006, 07-30) | Estado real (repo, 07-31) | Coincide |
|---|---|---|---|---|---|
| 1 | Dataset final (híbrido XM + GoiEner) | Decisión de equipo | ✅ Completada | ✅ `dataset_hibrido_v3.csv` presente, 50.869 filas, documentado | ✅ Sí |
| 2 | Entrenar modelo baseline + métricas | Tarea 1 | 🟡 En ejecución | 🔴 Sin script/notebook de entrenamiento versionado en `ml-service/` (solo el resultado narrado en `INFORME_HIBRIDO_v3.md`) | ⚠️ Parcial — el resultado está documentado pero no hay artefacto reproducible en el repo |
| 3 | Serializar modelo entrenado | Tarea 2 | 🔲 Pendiente | 🔴 No existe ningún archivo `.pkl`/`.joblib` en el repositorio | ✅ Coincide (ambos pendiente) |
| 4 | Endpoint `POST /api/v1/analisis-energetico` | — (ya en marcha) | 🟡 En ejecución | 🔴 `backend/src/main/java/` solo contiene `.gitkeep`, sin `pom.xml` | ⚠️ **No coincide** — el repo no refleja trabajo en curso; si existe, no está pusheado a `develop` |
| 5 | Servicio Python `POST /predict` | Tarea 3 | 🔲 Pendiente | 🔴 `ml-service/app/` solo contiene `.gitkeep` | ✅ Coincide |
| 6 | Backend ↔ ML real (reemplaza mock) | Tareas 4, 5 | 🔲 Pendiente | 🔴 No aplicable — ni backend ni ML existen | ✅ Coincide |
| 7 | Frontend ↔ Backend real | Tarea 6 | 🔲 Pendiente | 🔴 `apiService.js` sigue usando mock local como único camino funcional; además tiene mismatch de ruta con el contrato (ver `docs/architecture/AUDITORIA_BACKEND.md` §4) | ✅ Coincide, con hallazgo adicional |
| 8 | Validación de payloads y errores 400/500 | Tarea 4 | No reportado en acta 006 | 🔴 No implementable sin Tarea 4 | — |
| 9 | Endpoint `GET /health` | — | No reportado en acta 006 (mencionado como "continuidad de actividades") | 🔴 No existe | — |
| 10 | Primer despliegue técnico OCI | Tareas 4-6 | 🔲 Pendiente | 🔴 `infra/` completamente vacío, sin `Dockerfile` en ningún módulo | ✅ Coincide |
| 11 | Persistencia básica de resultados | Tarea 4 | No reportado | 🔴 No implementable sin Tarea 4 | — |
| 12 | OCI Object Storage para dataset/modelo | Tarea 10 | No reportado | 🔴 No implementable sin Tarea 10 | — |
| 13 | Logs estructurados + smoke test | Tarea 10 | No reportado | 🔴 No implementable sin Tarea 10 | — |
| 14 | Revisión UX frontend con datos reales | Tarea 7 | No reportado | 🔴 No implementable sin Tarea 7 | — |
| 15 | Consolidar y aprobar backlog | — | No reportado en acta 006 (el backlog seguía como "Propuesta" al 07-28; requiere confirmar si el PO lo aprobó formalmente) | ⚠️ Verificar con Product Owner | — |
| 16 | Redistribución del rol de Anayely (Data Engineer) | — | No reportado en acta 006 | ⚠️ Sin evidencia en el repo — decisión de gobernanza, no técnica | — |
| 17 | Sincronizar `develop` regularmente | — | ✅ Confirmado ("repositorio sincronizado", PR #5 integrado) | ✅ Working tree limpio, último commit `adee2f1` en `develop` | ✅ Sí |

---

## 2. Camino crítico hacia la Tarea #10

```text
Tarea 1 (dataset) ✅
   │
   ▼
Tarea 2 (entrenar baseline) 🟡 ── requiere artefacto reproducible, no solo informe
   │
   ▼
Tarea 3 (serializar modelo) 🔲 ── BLOQUEADA por Tarea 2 sin artefacto real
   │
   ▼
Tarea 5 (servicio ML /predict) 🔲 ── BLOQUEADA por Tarea 3
   │                                    ┌── Tarea 4 (endpoint backend) 🔴 puede avanzar en paralelo
   ▼                                    │      (no depende de ML, solo de sí misma)
Tarea 6 (Backend ↔ ML real) 🔲 ────────┘
   │
   ▼
Tarea 10 (despliegue OCI) 🔲 ── objetivo de esta auditoría
   │
   ▼
Tarea 7 (Frontend ↔ Backend real) 🔲
```

**Lectura del camino crítico:** la Tarea 10 no puede empezar en serio hasta que la Tarea 6 exista, y la Tarea 6 no puede existir hasta que las Tareas 4 y 5 existan **en paralelo**. De las dos, la Tarea 5 (ML) tiene la ruta más larga porque depende de la Tarea 3 (serializar), que depende de la Tarea 2 (entrenar), que hoy solo tiene un resultado narrado, no un artefacto. **La Tarea 4 (backend) es la que puede empezar hoy mismo sin ninguna dependencia externa** — es la acción de mayor apalancamiento inmediato.

---

## 3. Discrepancias entre lo reportado en actas y el estado del repositorio

Este es el hallazgo de gobernanza más relevante de esta matriz:

- Las Tareas #4 y #2 se reportaron como "🟡 En ejecución" en la reunión del 2026-07-30, pero **no hay evidencia en `develop`** de ese trabajo a 2026-07-31. Dos explicaciones posibles, a verificar con el equipo:
  1. El trabajo existe en ramas `feature/*` locales o remotas aún no fusionadas — en ese caso, **integrarlo antes de que esta auditoría quede obsoleta**.
  2. El estado "En ejecución" reflejaba intención/asignación, no avance de código — en ese caso, **ajustar el criterio de reporte en futuras actas** para distinguir "asignado" de "con código en `develop`", y así evitar que el backlog dé una falsa sensación de avance frente al riesgo R-04 (despliegue OCI tardío), que es justamente el que esta auditoría confirma como aún crítico.

Se recomienda que la próxima acta de seguimiento verifique explícitamente `git log`/PRs abiertos antes de reportar estado de tareas técnicas, siguiendo la misma disciplina que ya se aplicó para el estado del repositorio en la Tarea #17.

---

## 4. Relación con la matriz de riesgos vigente

| Riesgo (`planning/04`) | Estado a 2026-07-31 |
|---|---|
| R-04 Despliegue OCI tardío | 🔴 Activo y sin mitigar — 18 días desde su identificación (2026-07-13) sin ningún artefacto de infraestructura en el repo |
| R-02 Precisión del modelo por debajo de lo esperado | 🟢 Mitigado en el papel (91,7% accuracy documentado) pero 🔴 no verificable como artefacto — ver §1, Tarea 2 |
| R-03 Contrato inestable Backend-ML | 🟡 El contrato Frontend↔Backend está congelado, pero **no existe un contrato equivalente documentado para Backend↔ML** (nombre de endpoint, payload interno) — vacío a llenar antes de la Tarea 5 |
| R-05 Dependencia de personas clave | 🟡 Reforzado por la ausencia de Harrinson Villabona (Data Scientist, según `planning/01-Roles.md`) en la lista de participantes de la reunión más reciente (`meetings/ActaReunion-006-ENERGIAI.md`) — verificar continuidad de esa responsabilidad |
