# Checklist Domingo de Despliegue — 2026-08-02

**Uso:** guion operativo del día de despliegue, en bloques horarios orientativos. Cada bloque tiene un punto de decisión go/no-go. Si un punto de decisión falla, aplicar el escenario correspondiente de `docs/deployment/PLAN_CONTINGENCIA_OCI.md` **de inmediato** — no acumular bloqueadores hasta el final del día.

**Precondición de entrada:** este checklist asume que el sábado (`docs/governance/ESTADO_OPERATIVO_SPRINT2.md` §6) se cerró con backend y ML funcionando **localmente**, con `Dockerfile` probado para ambos. Si eso no ocurrió, no empezar este checklist — resolver primero los Escenarios 1 y/o 2 de `PLAN_CONTINGENCIA_OCI.md`.

---

## Bloque 1 — Mañana: verificación y preparación (objetivo: listo para desplegar antes del mediodía)

- [ ] Confirmar que el modelo serializado existe (real o "baseline v0 de contingencia") — `ml-service/models/`
- [ ] Confirmar que backend y ML corren localmente y responden `/health`
- [ ] Confirmar `docker build` exitoso de ambas imágenes (si no se probó el sábado, hacerlo ahora antes de continuar)
- [ ] **Punto de decisión 1:** ¿hay acceso confirmado a la cuenta/tenancy OCI? → Si NO: aplicar Escenario 4.a de `PLAN_CONTINGENCIA_OCI.md` antes de seguir — no tiene sentido avanzar sin esto resuelto
- [ ] Compartment dedicado a EnergiAI creado o confirmado
- [ ] VCN con subredes creada o confirmada
- [ ] Políticas IAM mínimas (Container Instances + Object Storage + Registry) confirmadas
- [ ] Repositorios OCIR creados (`energiai-backend`, `energiai-ml-service`)
- [ ] `docker login` exitoso contra OCIR
- [ ] Imágenes de backend y ML pusheadas a OCIR

## Bloque 2 — Mediodía: despliegue

- [ ] Container Instance del ML service creada
- [ ] Estado `RUNNING` confirmado
- [ ] **Punto de decisión 2:** ¿`GET /health` del ML service responde 200 dentro de la VCN? → Si NO tras 2 intentos de diagnóstico razonables: aplicar Escenario 4.b (fallback a Compute) de `PLAN_CONTINGENCIA_OCI.md`
- [ ] Container Instance del backend creada, con `ML_SERVICE_URL` apuntando al servicio ML ya desplegado
- [ ] Estado `RUNNING` confirmado
- [ ] **Punto de decisión 3:** ¿`GET /health` del backend responde 200? → Si NO tras 2 intentos: aplicar Escenario 4.b

## Bloque 3 — Tarde: validación end-to-end y evidencia

- [ ] `POST /api/v1/analisis-energetico` contra el backend desplegado, con payload de ejemplo del contrato, devuelve una respuesta generada por el modelo real (no el mock del frontend)
- [ ] Capturar evidencia: comando `curl` completo con respuesta, timestamp, IP/URL usada
- [ ] Capturas de pantalla de la consola OCI (Container Instances en estado `RUNNING`, detalles de red)
- [ ] Habilitar OCI Logging para al menos uno de los dos servicios y capturar una entrada de log real
- [ ] **Punto de decisión 4:** ¿el frontend logra integrarse en vivo con el backend real? → Si NO: aplicar Escenario 3 de `PLAN_CONTINGENCIA_OCI.md` (demo con mock + evidencia de backend/ML por separado) — no es un bloqueador del cierre del día, es una decisión de cómo se presenta la demo

## Bloque 4 — Noche: cierre y documentación

- [ ] Documentar en `infra/oci/README.md` (o equivalente) los pasos reproducibles y configuración no sensible usada — sin credenciales
- [ ] Registrar en `docs/local/respaldos/` qué contingencias (si alguna) se activaron durante el día y por qué
- [ ] Trasladar evidencia recolectada a `docs/governance/ENTREGABLES_NOCOUNTRY.md`
- [ ] Actualizar el estado de la Tarea #10 en `planning/05-Backlog-Sprint2-ENERGIAI.md`
- [ ] Confirmar con el equipo (mensaje async está bien, no requiere reunión) el resultado del día antes del lunes

---

## Definición de éxito del día

El domingo se considera exitoso si, al cierre del Bloque 3, los tres primeros puntos de decisión (1, 2, 3) están en verde — es decir: backend y ML corriendo en OCI y respondiendo con datos reales end-to-end. El punto de decisión 4 (frontend en vivo) es deseable pero **no es condición de éxito del despliegue OCI en sí** — su fallback ya está autorizado sin que eso represente un incumplimiento de la Tarea #10.

## Qué hacer si el día completo falla (los 4 puntos de decisión en rojo)

No es un escenario contemplado como aceptable pero debe tener una salida ordenada:

1. No improvisar decisiones nuevas el domingo a última hora — usar exactamente lo ya autorizado en `PLAN_CONTINGENCIA_OCI.md`.
2. Documentar con honestidad el estado real alcanzado (parcial es mejor que inflado) para `ENTREGABLES_NOCOUNTRY.md`.
3. Mover el cierre de la Tarea #10 al lunes como prioridad P0 absoluta (ver `docs/governance/ESTADO_OPERATIVO_SPRINT2.md` §6, flujo del lunes), con el diagnóstico de qué falló ya hecho el domingo, para no repetir el diagnóstico el lunes.
