# Auditoría Técnica — Servicio ML

**Módulo:** `ml-service/`
**Fecha:** 2026-07-31
**Tecnología declarada:** Python + Scikit-Learn — según `README.md`, `architecture/03-Arquitectura-Empresarial-EnergiAI.md` y `ml-service/README.md`.

---

## ADENDA — 2026-08-05

**Este hallazgo quedó parcialmente superado.** El servicio ML existe, se entrena y sirve inferencia, y está desplegado en OCI (verificado en demo end-to-end 2026-08-04, `meetings/ActaReunion-008-ENERGIAI.md`). Estado real actual:

- `ml-service/requirements.txt`, `train.py` e `inference.py` existen. `POST /predict` y `GET /health` implementados y funcionando — ver `architecture/contracts/CONTRATO_INTERNO_BACKEND_ML.md` (nuevo, documenta este contrato que antes no existía).
- **Sigue sin resolverse el hallazgo central de este documento (§2):** no hay un artefacto de modelo versionado de forma reproducible. El modelo se entrena *dentro del build de Docker* (`RUN python train.py` en `ml-service/Dockerfile`) — es reproducible en el sentido de que el build siempre lo regenera, pero el `.pkl` resultante nunca se serializa a `ml-service/models/` ni a Object Storage. Esa carpeta sigue vacía.
- `ml-service/notebooks/` y `ml-service/tests/` **siguen vacías** — no hay notebook de exploración ni tests del servicio.
- La estructura `ml-service/app/` descrita en `ml-service/README.md` **nunca se usó** — el código real vive suelto en `ml-service/` (`train.py`, `inference.py`).
- **Hallazgo nuevo detectado el 2026-08-05, no cubierto en la auditoría original:** el modelo solo soporta 2 categorías de `tipo_inmueble` (`Casa`, `Pequeño establecimiento`), mientras el contrato original definía 5. Corregido en `architecture/contracts/API_CONTRACT_V1.md` — ver `architecture/decisions/ADR-001-contrato-integracion-v1.md`.

El resto de este documento se conserva sin modificar como registro histórico de la auditoría del 2026-07-31.

---

## 1. Estado actual (evidencia)

```text
ml-service/
├── README.md
├── app/           <- solo .gitkeep
├── models/        <- solo .gitkeep
├── notebooks/     <- solo .gitkeep
└── tests/         <- solo .gitkeep
```

- **No existe `requirements.txt`** (ni `pyproject.toml`, ni `Pipfile`). No hay forma de instalar dependencias de este módulo hoy.
- **No existe código Python** en `app/` (ni servidor HTTP, ni lógica de inferencia).
- **No existe ningún notebook** en `notebooks/`, pese a que la metodología del dataset (score multicriterio, umbrales de clasificación, validación GroupKFold) ya está completamente especificada en `docs/data-engineering/INFORME_HIBRIDO_v3.md`. Esa metodología nunca fue traducida a un notebook o script de entrenamiento versionado del **modelo** (sí existen, en cambio, los scripts de construcción del **dataset**: `build_hibrido_final.py`, `dataset_maestro_v2.py`, ubicados en `docs/data-engineering/`, no en `ml-service/`).
- **No existe ningún artefacto de modelo serializado** en `models/` ni en ningún otro punto del repositorio (`.pkl`, `.joblib`, `.onnx` — búsqueda exhaustiva sin resultados).
- **No existen tests** en `tests/`.

**Conclusión:** el servicio ML no existe en ninguna forma ejecutable. Es la carpeta con mayor distancia entre lo documentado (metodología de clasificación validada con 91,7% de accuracy) y lo implementado (cero líneas de código de servicio).

---

## 2. La brecha entre "modelo validado" y "modelo servible"

Esto merece explicitarse porque es fácil de malinterpretar en las actas de seguimiento: **el 91,7% de accuracy reportado en `INFORME_HIBRIDO_v3.md` es el resultado de un experimento de validación (RandomForest + GroupKFold), documentado en prosa técnica dentro de un Markdown.** No es:

- Un notebook reproducible versionado en el repo.
- Un script de entrenamiento (`train.py`) versionado en el repo.
- Un modelo serializado (`.pkl`/`.joblib`) que un servicio pueda cargar con `pickle.load()` o `joblib.load()`.

Para que la Tarea #2 (entrenar baseline) y la Tarea #3 (serializar modelo) del Backlog Sprint 2 se den por completadas de forma verificable, el entregable tiene que ser un **artefacto versionado** (idealmente en `ml-service/models/` o en OCI Object Storage con referencia documentada, según Tarea #12), no solo un informe de resultados. Hoy, según el acta de la reunión más reciente (`meetings/ActaReunion-006-ENERGIAI.md`, 2026-07-30), la Tarea #2 está 🟡 en ejecución y la Tarea #3 sigue 🔲 pendiente — consistente con lo que se observa en el repositorio.

---

## 3. Verificación de servicio de inferencia

| Requisito | Especificado | Implementado |
|---|---|---|
| Endpoint de inferencia (`POST /predict` o equivalente, Tarea #5 del backlog) | ✅ Sí | ❌ No |
| Carga de modelo serializado aprobado | ✅ Sí (arquitectura §5.2, §8.3) | ❌ No (no hay modelo que cargar) |
| Normalización / feature engineering en inferencia consistente con entrenamiento | ✅ Sí (`ml-service/README.md`: "mantener consistencia entre features de entrenamiento e inferencia") | ❌ No verificable — no hay pipeline de entrenamiento versionado con el que comparar |
| Respuesta con clase, score y explicación resumida | ✅ Sí | ❌ No |
| Health check propio del servicio | Implícito por buenas prácticas de despliegue OCI (observabilidad, `architecture/03` §9) | ❌ No |

---

## 4. Riesgo de consistencia train/serve

El propio `ml-service/README.md` señala la responsabilidad de "mantener consistencia entre features de entrenamiento e inferencia" — un riesgo clásico de ML en producción (*training-serving skew*). Hoy este riesgo es **latente pero no activo**, porque no hay ni entrenamiento ni inferencia servibles. Sin embargo, debe anticiparse en el diseño del servicio:

- El esquema de features de `dataset_hibrido_v3.csv` (`consumo_kwh`, `uso_horario_pico`, `cantidad_equipos`, `tipo_inmueble`, `horas_alto_consumo`) coincide exactamente con `API_CONTRACT_V1`, lo cual es una buena señal: el contrato ya fue diseñado pensando en el dataset.
- Falta decidir y documentar cómo se codifica `tipo_inmueble` (categórica, 5 valores permitidos) de forma idéntica en el pipeline de entrenamiento y en el servicio de inferencia (p. ej. mismo `OneHotEncoder`/mapping serializado junto con el modelo, no reconstruido manualmente en cada lado).

---

## 5. Qué se necesita para llegar a un servicio ML desplegable (mínimo viable)

1. `requirements.txt` (o `pyproject.toml`) con: framework web ligero (FastAPI recomendado por tipado y `/docs` automático, o Flask si se prioriza simplicidad), `scikit-learn`, `pandas`, `joblib`, `uvicorn` (si FastAPI).
2. Un script/notebook de entrenamiento versionado en `ml-service/notebooks/` o `ml-service/app/train.py` que:
   - Cargue `data/processed/dataset_hibrido_v3.csv`.
   - Aplique la metodología ya documentada (score multicriterio + umbrales de `INFORME_HIBRIDO_v3.md` §4, ya está resuelta — no hay que rediseñarla, solo implementarla).
   - Divida por hogar (`cups`), no por fila, replicando el GroupKFold ya validado.
   - Serialice el modelo final (`joblib.dump`) junto con cualquier encoder/transformer necesario, en `ml-service/models/`.
3. Servicio de inferencia (`ml-service/app/main.py` o equivalente):
   - `POST /predict` (nombre exacto a decidir en conjunto con Backend, dado que hoy no está fijado en `API_CONTRACT_V1`, que solo define el contrato Frontend↔Backend, no Backend↔ML).
   - `GET /health` propio del servicio.
   - Carga del modelo en el arranque (no por request).
4. Tests mínimos en `ml-service/tests/` (hoy vacío): al menos un test de carga del modelo y un test de forma de la respuesta.
5. `Dockerfile` (Python slim base) — inexistente hoy, requisito directo para OCI Container Instances.

---

## 6. Veredicto

**Estado:** 🔴 Bloqueante crítico y **la ruta más larga** hacia la Tarea #10, porque a diferencia del backend (que puede empezar con un stub), el servicio ML depende de un artefacto de datos (modelo serializado) que todavía no existe en ningún formato reproducible. Es el componente que debe iniciarse primero, en paralelo con el backend, para no convertirse en el cuello de botella del Sprint 2.
