# Plan de Contingencia — Despliegue OCI

**Fecha:** 2026-07-31
**Principio rector:** decidir ahora, no el domingo bajo presión. Cada escenario tiene un disparador (*trigger*) verificable, una acción concreta y un responsable de ejecutarla, para que activar la contingencia sea una decisión mecánica, no una discusión de última hora.
**No modifica código.** Este documento autoriza *de antemano* ciertas desviaciones tácticas del plan principal (`docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md`) si sus disparadores se cumplen; no las ejecuta.

---

## Cómo usar este documento

1. Revisar los disparadores en los checkpoints de `docs/governance/CHECKLIST_DOMINGO_DESPLIEGUE.md` (y del sábado, en `docs/governance/ESTADO_OPERATIVO_SPRINT2.md` §6).
2. Si un disparador se cumple, ejecutar la acción de contingencia correspondiente **sin esperar aprobación adicional** — ya está pre-autorizada por este documento.
3. Registrar en `docs/local/respaldos/` (zona privada, no versionada) qué contingencia se activó y por qué, para trasladarlo el lunes a la documentación oficial.

---

## Escenario 1 — ML no entrega modelo serializado

**Disparador:** sábado 2026-08-01, mediodía, sin un artefacto `.pkl`/`.joblib` real (no solo un informe de resultados) versionado o respaldado.

**Impacto si no se actúa:** el servicio ML no tiene nada que cargar; el despliegue completo se detiene en el punto más temprano posible.

**Acción de contingencia:**

1. Bernardo (o quien esté disponible con conocimiento básico de Python/scikit-learn) ejecuta directamente la metodología **ya documentada y validada** en `docs/data-engineering/INFORME_HIBRIDO_v3.md` §4 sobre `data/processed/dataset_hibrido_v3.csv`:
   - Score multicriterio ya definido (no requiere rediseño).
   - División **por hogar (`cups`)**, no por fila — para no repetir el error de validación ya identificado como circular en el análisis original de GoiEner.
   - Entrenar RandomForest (ya es el algoritmo validado con 91,7% de accuracy documentado).
   - Serializar con `joblib.dump()` en `ml-service/models/`.
2. Etiquetar explícitamente el resultado como **"baseline v0 de contingencia"** en el nombre del artefacto y en cualquier documentación asociada — no presentarlo como el modelo final optimizado si Harrinson retoma el trabajo después.
3. Si ni siquiera hay tiempo para esto el sábado: desplegar el servicio ML con un **stub determinista** que replique las reglas de clasificación ya usadas para etiquetar el dataset (mismo score multicriterio, sin modelo de ML real detrás). Es peor que un modelo real, pero cumple el contrato de respuesta y permite continuar con el resto del despliegue. Debe quedar documentado como decisión temporal, no como el servicio ML definitivo.

**Responsable de ejecutar:** quien esté disponible con conocimiento de Python; por defecto, Bernardo.

---

## Escenario 2 — Backend no integra a tiempo

**Disparador:** sábado 2026-08-01, mediodía, sin un endpoint `POST /api/v1/analisis-energetico` funcionando al menos localmente.

**Impacto si no se actúa:** no hay nada que exponer al frontend ni que desplegar como "Backend" en OCI, aunque el servicio ML sí esté listo.

**Acción de contingencia (en orden de preferencia):**

1. **Preferida:** Bernardo u otro integrante disponible implementa un backend Spring Boot mínimo — solo el endpoint principal y `/health`, sin persistencia ni validaciones avanzadas (Tareas #8 y #11 del backlog quedan fuera de esta contingencia, se retoman después). Es menos trabajo de lo que parece: el contrato ya está congelado (`API_CONTRACT_V1.md`) y la lógica de recomendaciones ya existe portada desde `docs/architecture/MOTOR_RECOMENDACIONES_v1.md`.
2. **Fallback si no alcanza el tiempo:** exponer el endpoint directamente desde el servicio Python (FastAPI ya provee un framework de API), asumiendo temporalmente el rol de "backend" además del de "ML service". Esto es una **desviación explícita y temporal** de la arquitectura declarada (`architecture/03-Arquitectura-Empresarial-EnergiAI.md`, DA-01: Spring Boot como orquestador central) — debe documentarse como tal y revertirse en cuanto haya capacidad de backend Java real. Es preferible a no tener nada desplegable.
3. En cualquiera de los dos casos, la ruta expuesta debe ser exactamente `/api/v1/analisis-energetico` para no arrastrar el mismatch ya identificado con el frontend.

**Responsable de ejecutar:** Carlos Fabian Mesa / Elvis Trinidad; Bernardo como respaldo si no responden.

---

## Escenario 3 — Frontend no conecta con el backend real

**Disparador:** domingo 2026-08-02, tarde/noche, con backend y ML ya desplegados en OCI, pero la integración real desde `frontend/src/services/apiService.js` sigue fallando (CORS, mismatch de contrato, timeout, etc.).

**Impacto si no se actúa:** ninguno sobre el despliegue OCI en sí (backend y ML ya están arriba y son verificables por separado); sí afecta la demo visual de extremo a extremo.

**Acción de contingencia:**

1. **No forzar una corrección apurada bajo presión de tiempo.** El frontend ya tiene un fallback funcional y probado: el mock de `apiService.js` sigue mostrando la aplicación completa y coherente.
2. Para la demo/evidencia: mostrar la integración real por separado, con una petición `curl`/Postman en vivo contra el backend desplegado en OCI, dejando explícito que es la prueba de integración real — y usar el frontend con el mock para la experiencia visual completa. Esto es consistente con el plan de contingencia ya previsto en `planning/04-Gestion-de-Riesgos-Arquitectonicos.md` ("congelar interfaz con stub controlado para sostener la demo").
3. Registrar la causa raíz del fallo de integración (aunque no se resuelva ese fin de semana) para la próxima iteración — no descartar el diagnóstico solo porque se usó el fallback.

**Responsable de ejecutar:** Alonso Carbajal (Full Stack); decisión de "activar fallback para la demo" la toma Bernardo si no hay tiempo de resolverlo antes del cierre del domingo.

---

## Escenario 4 — OCI presenta problemas

Este escenario tiene varios niveles, del más simple al más grave. Evaluar en orden.

### 4.a — Cuenta/tenancy sin confirmar o sin acceso

**Disparador:** viernes 2026-07-31, si al final del día nadie ha confirmado acceso funcional a la consola OCI del hackathon.

**Acción:** esto es lo primero que debe resolverse, no lo último. Escalar de inmediato al Product Owner y, si aplica, al organizador del hackathon (Oracle/Alura/NoCountry) para confirmar el cupo. **No avanzar en Dockerfiles/IaC asumiendo que la cuenta existe** sin haberlo verificado — perder el sábado completo construyendo algo que no se puede desplegar el domingo es el peor escenario posible.

**Responsable:** Luis Angel Chavez Mejía (PO) / Bernardo.

### 4.b — Container Instances falla o no está disponible en la región asignada

**Disparador:** domingo, durante la Fase 3 de `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md`, sin lograr que la Container Instance quede en estado `RUNNING` tras dos intentos razonables de diagnóstico.

**Acción:** fallback a **OCI Compute** (VM simple) con Docker instalado manualmente — es la alternativa que la propia arquitectura ya contemplaba como equivalente (`architecture/03-Arquitectura-Empresarial-EnergiAI.md` §8.1: "Compute o Container Instances"). No requiere rediseño, solo un paso operativo distinto para correr las mismas imágenes.

**Responsable:** quien esté ejecutando el despliegue el domingo; por defecto, Bernardo.

### 4.c — OCI no es accesible/operable a tiempo, incluso con Compute

**Disparador:** domingo por la tarde, sin ningún servicio corriendo en OCI pese a haber intentado 4.a y 4.b.

**Acción (último recurso, con caveat explícito):** desplegar backend + ML en una plataforma alternativa gratuita (p. ej. Render, Railway, Fly.io) **únicamente como evidencia temporal de que la integración end-to-end funciona**, dejando documentado sin ambigüedad que esto **no sustituye el requisito de despliegue en OCI** del hackathon — es una prueba de continuidad técnica mientras se resuelve el acceso a OCI, no un reemplazo aceptado. Se debe seguir intentando OCI en paralelo o inmediatamente después, y este hecho debe comunicarse con transparencia al equipo y, si corresponde, al organizador del hackathon.

**Responsable:** Bernardo, con aviso inmediato al Product Owner — esta es la única acción de este documento que requiere comunicación explícita antes de ejecutarse, dado que toca el cumplimiento del requisito formal del hackathon.

---

## Tabla resumen de decisión rápida

| Escenario | Disparador (cuándo se activa) | Acción inmediata | Reversible después |
|---|---|---|---|
| 1. ML sin modelo | Sábado mediodía sin `.pkl`/`.joblib` | Entrenar/serializar baseline v0 ejecutado por Bernardo | Sí — se reemplaza cuando Harrinson entregue la versión definitiva |
| 2. Backend sin integrar | Sábado mediodía sin endpoint local funcional | Backend mínimo propio, o FastAPI como backend temporal | Sí — se revierte a Spring Boot cuando haya capacidad |
| 3. Frontend sin conectar | Domingo noche sin integración real funcionando | Demo con mock + evidencia de backend/ML por separado | Sí — se corrige en la siguiente iteración |
| 4.a Cuenta OCI no confirmada | Viernes noche sin acceso verificado | Escalar a PO/organizador de inmediato | N/A |
| 4.b Container Instances falla | Domingo, tras 2 intentos fallidos | Fallback a OCI Compute | Sí |
| 4.c OCI inoperable | Domingo tarde, sin nada desplegado en OCI | Evidencia temporal en plataforma alternativa + aviso explícito | Debe reemplazarse por OCI real apenas sea posible |
