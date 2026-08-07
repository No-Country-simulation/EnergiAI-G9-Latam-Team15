# Acta de Reunión 007 — Proyecto EnergiAI (G9-LATAM Team 15)

**Fecha:** lunes 3 de agosto de 2026
**Hora:** 11:30 a.m. (hora Colombia/Perú)
**Modalidad:** Virtual (Discord)
**Simulación:** NoCountry — Hackathon ONE G9-LATAM (Oracle / Alura)
**Elaborada por:** Bernardo Gómez — Solution / Software Architect

---

## 1. Asistentes

Asistieron los **7 integrantes activos** del equipo:

| Integrante | Rol |
|---|---|
| Bernardo Gómez | Solution / Software Architect |
| Elvis Trinidad | Backend Developer |
| Carlos Fabián Mesa | Backend Developer |
| Harrinson Villabona | Data Scientist |
| Alonso Carbajal | Full Stack Developer |
| Magno Cristian Coronel | Data Analyst |
| Luis Ángel Chávez Mejía | Product Owner |

**Ausente** Anayely Reyes (Data Engineer) no continuó en la simulación. El equipo se reorganiza y avanza con los 7 integrantes activos.

---

## 2. Objetivo de la reunión

Revisar el estado real del proyecto, reconocer los avances de cada integrante, alinear los últimos pasos hacia el despliegue en OCI, y confirmar las decisiones de producto bajo la dirección del Product Owner.

---

## 3. Estado del proyecto (avances revisados)

Se constató que **la mayor parte del trabajo crítico ya está superada**. Estado verificado en el repositorio (rama `develop`):

- ✅ **Modelo ML:** RandomForest entrenado y validado (~92% accuracy, StratifiedKFold), sobre el **dataset híbrido real** (fuentes XM + GoiEner). Reproducible.
- ✅ **Servicio de inferencia (ml-service):** API FastAPI con `/predict` y `/health`, funcionando.
- ✅ **Backend (Spring Boot, Java 21):** integrado al modelo real — la respuesta ya proviene del ML, no de un mock.
- ✅ **Frontend:** conectado al backend real, dockerizado; **demo completa corriendo end-to-end** (frontend → backend → modelo).
- ✅ **Gobernanza del repo:** trabajo unificado en `develop`, `main` limpia, historial ordenado (Git Flow respetado).
- ✅ **OCI:** las 3 imágenes (frontend, backend, ml-service) ya subidas al registry (OCIR); despliegue del Container Instance en curso.

---

## 4. Temas tratados y decisiones

**4.1 Diseño / Figma.**
Se ratificó la necesidad de consolidar el diseño en Figma. **Alonso Carbajal queda definitivamente a cargo del diseño/Figma**, en coordinación con el frontend que ya lidera.

**4.2 Despliegue en OCI y plan de contingencia.**
El despliegue objetivo es **OCI** (Container Instances), aprovechando la infraestructura ya preparada. Se acuerda dejar **Vercel como Plan B** para el frontend en caso de que el despliegue en OCI se complique.

**4.3 Tipos de inmueble (alcance del modelo).**
Se discutió que el modelo hoy clasifica sobre **"Casa" y "Pequeño establecimiento"** (las categorías presentes en la muestra real con la que se entrenó). Se evaluó qué hacer con otros tipos (apartamento / pequeño negocio):
- **Decisión para el MVP:** mantener las dos categorías que el modelo ya maneja de forma confiable, para que la demo sea sólida.
- **Mejora futura (Fase 2):** ampliar la cobertura re-entrenando el modelo con una muestra que incluya más tipos de inmueble reales.

**4.4 Feature de cantidad de equipos.**
Se destacó que la variable **cantidad de equipos** quedó muy bien integrada y aporta de forma clara a la clasificación. Se reconoce como uno de los puntos fuertes del modelo actual.

**4.5 Dirección de producto (PO).**
El equipo acuerda **seguir las pautas del Product Owner** (Luis Ángel) para avanzar de forma ordenada hacia el cierre, priorizando el MVP funcional y desplegado.

---

## 5. Reconocimientos

El equipo reconoce que **lo logrado a hoy es fruto del aporte de todos**:
- **Harrinson** — el modelo baseline y la metodología del dataset híbrido.
- **Elvis y Carlos** — la construcción del backend y sus endpoints.
- **Alonso** — el frontend funcional y ahora el diseño en Figma.
- **Cristian (Magno)** — el análisis de datos y las reglas de recomendación (base GoiEner).
- **Luis Ángel** — la dirección de producto y el alcance del MVP.
- **Bernardo** — la arquitectura, la integración de las piezas y el despliegue.

Cada quien puso su granito de arena para llegar a tener el producto funcionando de punta a punta.

---

## 6. Compromisos y próximos pasos

| # | Tarea | Responsable | Estado |
|---|---|---|---|
| 1 | Finalizar despliegue en OCI (Container Instance) + URL pública | Bernardo (Arquitectura) | En curso |
| 2 | Consolidar diseño en Figma | Alonso | En curso |
| 3 | Apuntar el frontend al backend desplegado (`VITE_API_URL`) | Alonso + Arquitectura | Al desplegar |
| 4 | Mantener Vercel listo como Plan B del frontend | Arquitectura | Contingencia |
| 5 | Evidencias del despliegue para NoCountry | Todos | Continuo |

---

## 7. Próxima reunión

**Martes 4 de agosto de 2026, 11:30 a.m.** — Seguimiento del despliegue en OCI y definición de cierre del MVP.

---

*Acta elaborada como registro oficial del proyecto. Se recomienda subirla a `meetings/` en el repositorio (GitHub) como evidencia para NoCountry.*
