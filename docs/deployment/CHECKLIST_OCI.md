# Checklist Operativo — Despliegue OCI (Tarea #10, Sprint 2)

**Fecha:** 2026-07-31
**Uso:** checklist de ejecución, complementario a `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md`. Marcar cada ítem solo con evidencia verificable (commit, screenshot, log o URL), no por percepción de avance.

---

## Fase 0 — Prerrequisitos de código

- [ ] `backend/pom.xml` existe y `mvn clean package` compila sin errores
- [ ] `POST /api/v1/analisis-energetico` implementado y probado localmente (`curl`/Postman)
- [ ] `GET /health` implementado en backend
- [ ] `ml-service/requirements.txt` existe y `pip install -r requirements.txt` funciona sin errores
- [ ] Modelo entrenado y **serializado** en `ml-service/models/` (o referenciado desde Object Storage)
- [ ] Endpoint de inferencia del ML service implementado y probado localmente
- [ ] `GET /health` implementado en ML service
- [ ] Backend y ML service integrados y probados localmente (docker-compose o ejecución directa en dos terminales)
- [ ] Ruta de `frontend/src/services/apiService.js` alineada con la ruta real expuesta por el backend (`/api/v1/analisis-energetico` vs `/analisis-energetico` — resolver la inconsistencia documentada en `docs/architecture/AUDITORIA_BACKEND.md` §4)
- [ ] `Dockerfile` de backend — build local exitoso (`docker build -t energiai-backend .`)
- [ ] `Dockerfile` de ml-service — build local exitoso (`docker build -t energiai-ml .`)
- [ ] Contenedores corren localmente y responden `/health` (`docker run` + `curl`)

## Fase 1 — Cuenta y proyecto OCI

- [ ] Tenancy OCI del equipo confirmado y accesible (verificar con Product Owner / patrocinador del hackathon)
- [ ] Compartment dedicado a EnergiAI creado
- [ ] Grupo IAM del equipo creado con políticas mínimas (Container Instances, Object Storage, Registry)
- [ ] VCN creada con subred(es) apropiadas
- [ ] Reglas de seguridad (Security Lists / NSGs) permiten tráfico backend↔ML y acceso externo al backend

## Fase 2 — Registro de imágenes

- [ ] Repositorio OCIR `energiai-backend` creado
- [ ] Repositorio OCIR `energiai-ml-service` creado
- [ ] Auth token OCI generado y `docker login` exitoso contra OCIR
- [ ] Imagen de backend pusheada a OCIR
- [ ] Imagen de ml-service pusheada a OCIR

## Fase 3 — Despliegue

- [ ] Container Instance del ML service creada y en estado `RUNNING`
- [ ] `GET /health` del ML service responde 200 dentro de la VCN
- [ ] Container Instance del backend creada y en estado `RUNNING`, con `ML_SERVICE_URL` configurada
- [ ] `GET /health` del backend responde 200 (público o accesible por el equipo)
- [ ] `POST /api/v1/analisis-energetico` contra el backend desplegado responde con datos generados por el modelo real (no el mock del frontend)
- [ ] (Opcional, no bloqueante) Frontend desplegado (Object Storage estático o Container Instance con Nginx) y apuntando al backend real vía `VITE_API_URL`

## Fase 4 — Observabilidad y evidencia

- [ ] OCI Logging habilitado para al menos uno de los dos servicios
- [ ] Evidencia capturada: URLs/IPs, comandos ejecutados, capturas de pantalla de la consola OCI
- [ ] `infra/oci/README.md` (hoy inexistente) documenta pasos reproducibles y valores de configuración no sensibles
- [ ] Variables de entorno y secretos documentados en `.env.example` por módulo (sin valores reales)
- [ ] Evidencia trasladada a `docs/governance/ENTREGABLES_NOCOUNTRY.md`

## Cierre de la Tarea #10

- [ ] Todos los ítems de Fase 3 marcados con evidencia
- [ ] Acta de reunión actualizada reflejando el cierre de la Tarea #10 (siguiendo el formato de `meetings/ActaReunion-006-ENERGIAI.md`)
- [ ] Backlog Sprint 2 (`planning/05-Backlog-Sprint2-ENERGIAI.md`) actualizado con el estado real
