# Acta de Reunión 006 – EnergiAI

**Fecha:** 30 de julio de 2026
**Hora:** 11:30 a.m. (Colombia / Perú)
**Medio:** Discord – Reunión relámpago de seguimiento Sprint 2

## Objetivo

Revisar el estado actual del proyecto al inicio de Sprint 2, validar la integración de los entregables recientemente incorporados al repositorio oficial y coordinar las actividades prioritarias para continuar la construcción del MVP EnergiAI.

## Participantes

- Bernardo Adolfo Gómez Montoya – Software / Solution Architect
- Alonso Carbajal – Full Stack Developer
- Magno Cristian Coronel Salazar – Data Analyst
- Elvis Leniker Trinidad Caldas – Backend Developer


---

## Temas Tratados

### 1. Estado del Repositorio

Se realizó verificación de la rama `develop` y del estado del repositorio. Se confirmó:

- ✅ PR #5 integrado exitosamente en `develop`.
- ✅ Sin conflictos pendientes.
- ✅ Repositorio sincronizado.
- ✅ Working tree limpio.
- ✅ Línea base oficial de Sprint 2 actualizada.

### 2. Consolidación del Dataset Maestro

Se revisó el resultado de la integración realizada a partir de:

- Dataset Maestro v2 (XM Colombia).
- Dataset GoiEner (España).

Se confirmó que la propuesta oficial adoptada por el equipo corresponde al **Dataset Maestro v3 Híbrido (XM + GoiEner)**.

**Características:**

| Atributo | Valor |
|---|---|
| Registros | 50.869 |
| Valores nulos | 0 |
| Duplicados | 0 |
| Compatibilidad | API_CONTRACT_V1 |
| Validación | GroupKFold documentada |
| Accuracy aproximado | 91,7% |
| Informe técnico | Disponible para consulta |

### 3. Relación con Backlog Sprint 2

Se verifica el estado de avance frente al backlog aprobado por Product Owner.

| # | Tarea | Estado | Responsable |
|---|---|---|---|
| 1 | Definir y construir dataset final (Híbrido XM + GoiEner) | ✅ Completada | — |
| 2 | Entrenar modelo baseline | 🟡 En ejecución | Data Scientist |
| 3 | Serializar modelo entrenado | 🔲 Pendiente | — |
| 4 | Implementar endpoint `POST /api/v1/analisis-energetico` | 🟡 En ejecución | Backend Team |
| 5 | Servicio ML `POST /predict` | 🔲 Pendiente | — |
| 6 | Integración Backend ↔ ML | 🔲 Pendiente | — |
| 7 | Integración Frontend ↔ Backend | 🔲 Pendiente | — |
| 10 | Primer despliegue técnico OCI | 🔲 Pendiente | — |

**Resultado Tarea 1:**
- Dataset Maestro v3 Híbrido integrado en `develop`.
- Documentación incorporada.
- Evidencia técnica disponible.

### 4. Frontend

Se confirmó que los componentes desarrollados se encuentran integrados en la rama `develop`.

**Disponibles actualmente:**

- FormularioConsumo
- SemaforoEficiencia
- HistorialAnalisis
- TarjetaCosto
- ListaRecomendaciones
- API Service (mock)
- Suite inicial de pruebas

**Próximo paso:** Integración con Backend real.

### 5. Backend

Se confirmó continuidad de las actividades para:

- Endpoint principal de análisis energético.
- Validaciones.
- Manejo de errores.
- Endpoint Health Check.

### 6. OCI

Se identificó como prioridad del Sprint 2 iniciar el despliegue técnico mínimo requerido para el Hackathon.

**Objetivo:**

- Backend desplegado.
- Servicio ML desplegado.
- Evidencia funcional OCI.

### 7. Entregables NoCountry

Se recuerda la necesidad de consolidar evidencias y enlaces oficiales del proyecto.

**Posibles recursos:**

- GitHub oficial.
- Documentación.
- Arquitectura.
- Figma (si existe enlace disponible).
- Frontend desplegado.
- Backend desplegado.
- OCI.
- Video demostrativo.

---

## Acuerdos

- ✅ Se adopta oficialmente el Dataset Maestro v3 Híbrido como línea base para Sprint 2.
- ✅ Se considera completada la Tarea 1 del Backlog Sprint 2.
- ✅ El foco técnico del Sprint 2 se traslada a: Machine Learning, Backend, Integración y OCI.
- ✅ Se continuará utilizando GitFlow y revisión mediante Pull Requests para futuras integraciones.
- ✅ Se mantendrá la trazabilidad documental mediante actas y documentos técnicos.

---

## Estado General del Proyecto

| Área | Estado |
|---|---|
| Arquitectura | ✅ Consolidada |
| Documentación | ✅ Consolidada |
| Dataset | ✅ Consolidado e integrado |
| Frontend | 🟡 Integrado y pendiente de conexión real |
| Backend | 🟡 Desarrollo en marcha |
| Machine Learning | 🟡 Inicio de entrenamiento |
| OCI | 🔄 Pendiente despliegue inicial |
| Gobernanza | ✅ Repositorio sincronizado y actualizado |

---

## Próximos Pasos

1. Entrenar modelo baseline.
2. Serializar modelo entrenado.
3. Implementar endpoint principal Backend.
4. Crear servicio de inferencia ML.
5. Integrar Backend ↔ ML.
6. Integrar Frontend ↔ Backend.
7. Iniciar despliegue OCI.
8. Registrar evidencias para NoCountry.
9. Continuar seguimiento del Sprint 2.

---

## Conclusión

La reunión permitió validar que la rama `develop` refleja correctamente la línea base oficial del proyecto para Sprint 2. Con la integración del PR #5 se consolidan el Dataset Maestro v3 Híbrido, la documentación asociada y el backlog aprobado, permitiendo que el equipo concentre sus esfuerzos en la construcción e integración del MVP funcional EnergiAI.
