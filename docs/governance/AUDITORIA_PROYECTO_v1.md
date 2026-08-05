# Auditoría Técnica del Proyecto EnergiAI — v1

**Rol:** Principal Solution Architect / Principal Cloud Architect OCI / Auditor Técnico Senior
**Fecha de auditoría:** 2026-07-31
**Rama auditada:** `develop` (working tree limpio, último commit `adee2f1`)
**Objetivo:** Determinar el estado real del repositorio frente a la Tarea #10 del Backlog Sprint 2 ("Primer despliegue técnico en OCI") y establecer qué bloquea ese despliegue hoy.

> Este documento es un **snapshot de auditoría**, no un plan de trabajo. El plan de acción está en `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md` y el checklist operativo en `docs/deployment/CHECKLIST_OCI.md`.

---

## ADENDA — 2026-08-05

Snapshot re-emitido: el sistema completo (Frontend + Backend + ML Service) está construido, integrado sin mock, y desplegado en OCI. Estado por dimensión, actualizado:

| Dimensión | Estado 2026-07-31 | Estado 2026-08-05 |
|---|---|---|
| Documentación / Arquitectura | ✅ Fuerte | ✅ Fuerte — + 2 ADR, contrato interno Backend↔ML, C4 N3, diagrama de secuencia |
| Dataset | ✅ Fuerte | ✅ Sin cambios |
| Frontend | 🟡 Funcional pero desacoplado | 🟢 Integrado con backend real, desplegado en OCI |
| Backend | 🔴 Inexistente | 🟢 Implementado, desplegado en OCI — sin tests aún |
| Servicio ML | 🔴 Inexistente | 🟢 Implementado, desplegado en OCI — modelo no versionado como artefacto independiente (se entrena en cada build), sin notebook ni tests |
| Infraestructura / OCI | 🔴 Inexistente | 🟢 3 imágenes en OCIR, stack corriendo — ver `infra/oci/README.md` (URL pública pendiente de documentar) |
| CI/CD | 🔴 Inexistente | 🔴 Sigue inexistente — `.github/workflows/` sigue vacío |

**Hallazgo nuevo (no cubierto el 2026-07-31):** mismatch entre `API_CONTRACT_V1.md` (`tipo_inmueble`, 5 valores) y el modelo real entrenado (2 valores) — corregido el 2026-08-05, ver `architecture/decisions/ADR-001-contrato-integracion-v1.md`.

**Deuda técnica que persiste sin cambios:** cero tests en backend y en ml-service; motor de recomendaciones decidido (ADR-002) pero no implementado; sin persistencia de histórico; sin CI/CD.

Detalle completo de qué se corrigió hoy y qué queda pendiente, con responsables sugeridos por rol, en `docs/local/revisiones/AUDITORIA_DOCUMENTAL_2026-08-05.md` (documento local, no versionado en GitHub).

El resto de este documento se conserva sin modificar como registro histórico de la auditoría del 2026-07-31.

---

## 1. Resumen ejecutivo

El proyecto tiene una **base documental y de datos sólida** (arquitectura, contrato de integración, gestión de riesgos, dataset real validado) pero **cero código ejecutable en backend y en el servicio ML**, y **cero artefactos de infraestructura**. El frontend es el único componente con implementación real, y opera de forma autosuficiente mediante un mock local que sustituye por completo al backend.

**Conclusión directa:** hoy no existe nada desplegable en OCI más allá de un sitio estático (el frontend). El backend y el servicio ML son carpetas vacías (`.gitkeep` únicamente); no hay imagen de contenedor, no hay `Dockerfile`, no hay definición de infraestructura OCI, no hay pipeline CI/CD. La Tarea #10 del backlog no es "desplegar algo que ya existe": es un bloque de trabajo que depende íntegramente de que primero existan las Tareas #4, #5 y #6.

| Dimensión | Estado | Evidencia |
|---|---|---|
| Documentación / Arquitectura | ✅ Fuerte | `architecture/`, `docs/`, `planning/`, contrato API v1.0 |
| Dataset | ✅ Fuerte | `dataset_hibrido_v3.csv` (50.869 filas, real+derivado, validado GroupKFold) |
| Frontend | 🟡 Funcional pero desacoplado | Componentes reales, tests, pero corre 100% en modo mock |
| Backend | 🔴 Inexistente | `backend/src/**` solo contiene `.gitkeep` |
| Servicio ML | 🔴 Inexistente | `ml-service/**` solo contiene `.gitkeep`, sin modelo serializado |
| Infraestructura / OCI | 🔴 Inexistente | `infra/**` solo contiene `.gitkeep`, sin `Dockerfile`, sin IaC |
| CI/CD | 🔴 Inexistente | `.github/workflows/` solo contiene `.gitkeep` |

---

## 2. Alcance de la auditoría

Se revisaron exhaustivamente:

- `architecture/` (3 documentos + contrato de integración)
- `backend/` (estructura completa de directorios y archivos)
- `frontend/` (código fuente, tests, configuración de build)
- `ml-service/` (estructura completa de directorios y archivos)
- `infra/` (estructura completa de directorios y archivos)
- `planning/` (roles, riesgos, roadmap, backlog Sprint 2)
- `docs/` (índice, gobierno técnico, data engineering)
- `diagrams/`, `meetings/`, `README.md`, `ESTADO-PROYECTO.md`

Búsqueda dirigida en todo el repositorio (excluyendo `node_modules`) de artefactos de despliegue: `Dockerfile`, `docker-compose*`, `pom.xml`, `build.gradle`, `requirements.txt`, `application.yml/.properties`, archivos Terraform (`*.tf`), y modelos serializados (`*.pkl`, `*.joblib`, `*.onnx`). **Resultado: cero coincidencias.**

---

## 3. Hallazgos por componente

### 3.1 Arquitectura y documentación — ✅ Fuerte

- `architecture/03-Arquitectura-Empresarial-EnergiAI.md` define capas, componentes, decisiones arquitectónicas justificadas (DA-01 a DA-05) y una estrategia de integración OCI explícita (Compute/Container Instances, Object Storage, API Gateway, Vault, Logging/Monitoring).
- `architecture/contracts/API_CONTRACT_V1.md` congela el contrato JSON entre Frontend, Backend y ML Service, incluyendo el endpoint `POST /api/v1/analisis-energetico`, esquema de request/response, categorías de clasificación y fórmula de costo (`consumo_kwh × 0.75`).
- `planning/04-Gestion-de-Riesgos-Arquitectonicos.md` ya identificaba **R-04 "Despliegue OCI tardío"** como riesgo activo desde el 2026-07-13. Ese riesgo se materializó: sigue sin mitigar 18 días después.
- Gap documental heredado (ver `ESTADO-PROYECTO.md`, no versionado — excluido de Git localmente): no existe ADR formal del contrato de integración ni diagrama de secuencia versionado para el flujo de `POST /api/v1/analisis-energetico`. No es bloqueante para OCI, pero es deuda de trazabilidad.

### 3.2 Dataset — ✅ Fuerte

- Dataset vigente: `data/processed/dataset_hibrido_v3.csv` — 50.869 filas, 6 columnas (esquema exacto del contrato), 0 nulos, 0 duplicados.
- Combina consumo real medido (GoiEner Smart Meter Dataset v7, España) con metodología de calibración validada en la v2 (XM Colombia).
- Validación reportada: RandomForest, GroupKFold 5-fold agrupado por hogar, **91,7% ± 0,3% accuracy** vs. 38,4% baseline de clase mayoritaria.
- **Importante:** esta cifra de accuracy es un resultado de **experimento documentado en Markdown** (`docs/data-engineering/INFORME_HIBRIDO_v3.md`), no de un modelo serializado y reproducible en el repositorio. No hay notebook ni script de entrenamiento del modelo final versionado — solo los scripts de construcción del dataset (`build_hibrido_final.py`, `dataset_maestro_v2.py`). Ver `docs/architecture/AUDITORIA_ML.md` §2.
- Dataset antecedente `dataset_maestro_v2.csv` (10.000 filas, 100% sintético sobre curva horaria real de XM) se conserva como base metodológica pero no es la fuente vigente.

### 3.3 Frontend — 🟡 Funcional pero desacoplado

- Componentes reales e integrados en `develop`: `FormularioConsumo`, `SemaforoEficiencia`, `HistorialAnalisis`, `TarjetaCosto`, `ListaRecomendaciones`, hook `useHistorial`, `apiService.js`.
- Suite de tests con Vitest + Testing Library cubriendo los 6 componentes y el servicio de API.
- Stack: React 18 + Vite + Tailwind + Recharts + jsPDF/html2canvas (export PDF).
- **Hallazgo crítico de integración:** `frontend/src/services/apiService.js` llama a `${API_URL}/analisis-energetico`, **sin el prefijo `/api/v1`** que exige `API_CONTRACT_V1.md` (`POST /api/v1/analisis-energetico`). Si el backend se implementa siguiendo el contrato al pie de la letra, esta llamada fallará por mismatch de ruta. Debe corregirse en cualquiera de los dos lados antes de la integración real (Tarea #7 del backlog).
- **Hallazgo arquitectónico:** el motor de recomendaciones (`generarRecomendaciones()`) vive completamente en el frontend como parte del mock de fallback, no en backend/ML como indica el flujo documentado en el contrato (Frontend → Backend → ML Service → Modelo IA). Detalle completo en `docs/architecture/MOTOR_RECOMENDACIONES_v1.md`.
- El `catch` de `analizarConsumo()` en `apiService.js` hace que **cualquier fallo de red o backend inexistente sea invisible para el usuario**: la app siempre "funciona" porque cae al mock. Esto es correcto como estrategia de demo-resiliente, pero oculta el hecho de que hoy el frontend nunca ha hablado con un backend real.

### 3.4 Backend — 🔴 Inexistente

Ver detalle completo en `docs/architecture/AUDITORIA_BACKEND.md`. Resumen: `backend/src/main/java/`, `backend/src/main/resources/` y `backend/src/test/java/` contienen únicamente `.gitkeep`. No existe `pom.xml` ni `build.gradle`, por lo que **no hay siquiera un proyecto Spring Boot inicializable**, más allá de la estructura de carpetas.

- `POST /api/v1/analisis-energetico`: **no existe.**
- `GET /health`: **no existe.**

### 3.5 Servicio ML — 🔴 Inexistente

Ver detalle completo en `docs/architecture/AUDITORIA_ML.md`. Resumen: `ml-service/app/`, `ml-service/models/`, `ml-service/notebooks/` y `ml-service/tests/` contienen únicamente `.gitkeep`. No existe `requirements.txt`, no existe código de servicio, no existe modelo serializado.

- Modelo serializado (`.pkl`/`.joblib`/`.onnx`): **no existe.**
- Servicio de inferencia (`POST /predict` o equivalente): **no existe.**

### 3.6 Infraestructura / OCI — 🔴 Inexistente

- `infra/docker/`, `infra/oci/`, `infra/scripts/`: solo `.gitkeep`.
- No hay `Dockerfile` para backend ni para ml-service (ni siquiera hay código que contenerizar).
- No hay definición de infraestructura como código (Terraform, Resource Manager de OCI, ni scripts OCI CLI).
- No hay evidencia en el repositorio de un *tenancy*, *compartment*, VCN, políticas IAM o *bucket* de Object Storage ya aprovisionados. Puede existir fuera del repo (consola OCI), pero no está documentado ni versionado — riesgo de conocimiento tácito no trazable (relacionado con R-05).

### 3.7 CI/CD y gobernanza técnica — 🔴 Inexistente / 🟡 Parcial

- `.github/workflows/` está vacío (`.gitkeep` únicamente): no hay build, test ni lint automatizados para ningún componente.
- GitFlow declarado (`main` / `develop` / `feature/*`) se está siguiendo correctamente en la práctica reciente (PR #4 y #5 mergeados a `develop` con revisión).
- No hay `.env.example` en ningún módulo pese a que ya existe una variable de entorno en uso (`VITE_API_URL` en frontend) y habrá al menos 2-3 más necesarias para backend↔ML↔OCI.

---

## 4. Qué impide específicamente el despliegue en OCI hoy

En orden de bloqueo (cada ítem bloquea a los siguientes):

1. **No hay código de backend que compilar/contenerizar** — falta hasta el `pom.xml`.
2. **No hay código de servicio ML que compilar/contenerizar** — falta hasta el `requirements.txt`.
3. **No hay modelo serializado** que el servicio ML pueda cargar en tiempo de ejecución.
4. **No hay `Dockerfile`** para ninguno de los dos servicios (consecuencia directa de 1 y 2).
5. **No hay definición de infraestructura OCI** (Compute/Container Instances, red, IAM, storage) ni como IaC ni como documentación operativa paso a paso.
6. **No hay gestión de variables de entorno/secretos** documentada para el entorno de despliegue (URLs internas de servicios, credenciales OCI, tarifa de referencia, etc.).
7. **No hay pipeline CI/CD** que automatice build → test → push de imagen → despliegue.
8. **Inconsistencia de contrato** entre frontend y `API_CONTRACT_V1` (ruta sin `/api/v1`) que debe resolverse antes de dar por cerrada la integración end-to-end, aunque no bloquea el despliegue de infraestructura en sí.

**Ninguno de estos puntos es un problema de OCI como plataforma.** OCI no es el cuello de botella: es el destino de un despliegue que todavía no tiene qué desplegar. El cuello de botella real son las Tareas #4, #5 y #6 del Backlog Sprint 2, de las que depende explícitamente la Tarea #10.

---

## 5. Priorización de acciones (impacto × urgencia)

| Prioridad | Acción | Impacto | Urgencia | Bloquea a |
|---|---|---|---|---|
| P0 | Inicializar proyecto Spring Boot real (`pom.xml`, estructura de paquetes, `application.yml`) | Alto | Crítica | Todo lo demás en backend |
| P0 | Inicializar proyecto de servicio ML (`requirements.txt`, framework de API — FastAPI/Flask) | Alto | Crítica | Todo lo demás en ML |
| P0 | Entrenar y **serializar** el modelo baseline sobre `dataset_hibrido_v3.csv` | Alto | Crítica | Servicio de inferencia real |
| P1 | Implementar `POST /api/v1/analisis-energetico` en backend (stub → real) | Alto | Alta | Integración end-to-end, Tarea #10 |
| P1 | Implementar `GET /health` en backend (y equivalente en ML service) | Medio | Alta | Verificación de despliegue OCI |
| P1 | Implementar `POST /predict` en servicio ML, cargando el modelo serializado | Alto | Alta | Backend ↔ ML |
| P1 | Corregir ruta en `apiService.js` (agregar `/api/v1`) o documentar excepción explícita | Medio | Alta | Integración Frontend ↔ Backend |
| P2 | Escribir `Dockerfile` para backend y ML service | Alto | Alta | Despliegue OCI |
| P2 | Definir y documentar arquitectura mínima de despliegue OCI (Compute/Container Instances) | Alto | Alta | Tarea #10 |
| P2 | Ejecutar primer despliegue técnico OCI (Backend + ML, aunque sea con datos de prueba) | Alto | Alta | Cierre de Tarea #10 |
| P3 | Documentar variables de entorno (`.env.example` por módulo) | Medio | Media | Reproducibilidad del despliegue |
| P3 | Configurar CI mínima (build + test en PR) | Medio | Media | Calidad sostenida |
| P3 | OCI Object Storage para dataset/modelo (Tarea #12) | Medio | Baja | Evolución post-MVP |

---

## 6. Documentos relacionados de esta auditoría

- `docs/architecture/AUDITORIA_BACKEND.md` — detalle del gap de backend.
- `docs/architecture/AUDITORIA_ML.md` — detalle del gap de ML e inferencia.
- `docs/architecture/MOTOR_RECOMENDACIONES_v1.md` — auditoría del motor de recomendaciones actual (frontend mock).
- `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md` — plan de despliegue propuesto.
- `docs/deployment/CHECKLIST_OCI.md` — checklist operativo de despliegue.
- `docs/deployment/OCI_READINESS_REPORT.md` — veredicto formal de disposición para desplegar en OCI.
- `docs/governance/MATRIZ_DEPENDENCIAS_SPRINT2.md` — dependencias entre tareas del backlog Sprint 2.
- `docs/governance/ENTREGABLES_NOCOUNTRY.md` — estado de entregables para NoCountry.
- `docs/governance/RESUMEN_EJECUTIVO_AUDITORIA_SPRINT2.md` — síntesis ejecutiva de esta auditoría.
