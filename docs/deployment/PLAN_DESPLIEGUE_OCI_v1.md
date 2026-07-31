# Plan de Despliegue OCI v1 — Primer Despliegue Técnico (Tarea #10, Sprint 2)

**Fecha:** 2026-07-31
**Alcance:** "al menos Backend + ML" desplegados en OCI, tal como define la Tarea #10 del Backlog Sprint 2, con evidencia funcional verificable.
**Precondición explícita:** este plan **no puede ejecutarse hoy**. Depende de que existan primero artefactos desplegables (ver `docs/architecture/AUDITORIA_BACKEND.md` y `docs/architecture/AUDITORIA_ML.md`). Su propósito es dejar la ruta lista para ejecutarse en cuanto esas dependencias se resuelvan, sin perder tiempo de diseño en ese momento.

---

## 1. Principio rector

`architecture/03-Arquitectura-Empresarial-EnergiAI.md` ya fija la decisión arquitectónica correcta para el MVP: **pragmatismo cloud, no completitud cloud.** Este plan no introduce servicios OCI nuevos ni desvía esa decisión; solo la secuencia en pasos ejecutables.

Objetivo del primer despliegue (no del despliegue final): demostrar que el flujo `Backend ↔ ML Service` funciona sobre infraestructura real de OCI, con evidencia reproducible. No es necesario en esta primera iteración: alta disponibilidad, autoscaling, base de datos gestionada, ni dominio propio.

---

## 2. Arquitectura de despliegue objetivo (primer despliegue)

```text
                    Internet
                        │
                        ▼
        ┌───────────────────────────────┐
        │   OCI Container Instance      │
        │   (Backend Spring Boot)       │
        │   puerto 8080, /health        │
        └───────────────┬───────────────┘
                        │  red privada / VCN
                        ▼
        ┌───────────────────────────────┐
        │   OCI Container Instance      │
        │   (ML Service Python)         │
        │   puerto 8000, /health        │
        │   modelo cargado en memoria   │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   OCI Object Storage          │
        │   (dataset + modelo .pkl)     │
        └───────────────────────────────┘
```

Frontend queda fuera del alcance estricto de la Tarea #10 (que exige "al menos Backend + ML"), pero se recomienda desplegarlo en paralelo como sitio estático (Object Storage con *static website hosting* o un Container Instance liviano con Nginx) para tener demo end-to-end lista — no es bloqueante para cerrar la Tarea #10.

**Justificación de Container Instances sobre Compute (VM) clásico:** menor fricción operativa para un equipo de hackathon (no hay que administrar SO, parches, ni SSH), arranque más rápido, y es la opción que la propia arquitectura (`architecture/03` §8.1) ya lista como preferida junto a Compute.

---

## 3. Servicios OCI requeridos (mínimo viable)

| Servicio OCI | Uso | Prioridad |
|---|---|---|
| **Container Instances** | Ejecutar backend y ML service contenerizados | P0 |
| **Container Registry (OCIR)** | Almacenar las imágenes Docker antes de desplegarlas | P0 |
| **VCN (Virtual Cloud Network)** | Red privada entre backend y ML service, exposición controlada del backend | P0 |
| **Object Storage** | Repositorio de dataset y modelo serializado (Tarea #12) | P1 |
| **IAM / Policies** | Permisos mínimos para que Container Instances lean de Object Storage | P1 |
| **Logging** | Trazabilidad básica de ejecución (Tarea #13) | P1 |
| **Vault** | Gestión de secretos si se requieren credenciales (p. ej. si se añade BD) | P2 — no crítico si no hay BD en este primer despliegue |
| **API Gateway** | Exposición controlada del backend | P3 — explícitamente pospuesto en `architecture/03` §8.1 ("en evolución posterior") |
| **Autonomous Database** | Persistencia de histórico (Tarea #11) | P3 — no crítico para el primer despliegue técnico |

---

## 4. Secuencia operativa (orden de ejecución)

Esta secuencia respeta las dependencias reales del backlog (ver `docs/governance/MATRIZ_DEPENDENCIAS_SPRINT2.md`) — no se puede saltar pasos.

### Fase 0 — Prerrequisitos de código (fuera de OCI)

1. Backend: `pom.xml` + endpoint `POST /api/v1/analisis-energetico` + `GET /health` (Tarea #4, #9).
2. ML Service: `requirements.txt` + modelo serializado + endpoint de inferencia + `/health` (Tareas #2, #3, #5).
3. Backend ↔ ML Service integrados localmente (`docker-compose` local recomendado como paso intermedio antes de OCI) (Tarea #6).
4. `Dockerfile` para ambos servicios, validado con build local (`docker build` exitoso).

### Fase 1 — Preparación de cuenta y proyecto OCI

5. Confirmar *tenancy* OCI activo para el equipo (verificar si ya existe cupo del hackathon Oracle+Alura+NoCountry — no hay evidencia en el repo de que esto esté resuelto; **verificar con Product Owner antes de continuar**).
6. Crear/confirmar *compartment* dedicado al proyecto EnergiAI.
7. Crear VCN con al menos una subred pública (backend) y una privada o restringida (ML service).
8. Crear políticas IAM mínimas (grupo dedicado al equipo, permisos de Container Instances + Object Storage + Registry).

### Fase 2 — Registro de imágenes

9. Crear repositorio en OCI Container Registry (OCIR) para `energiai-backend` y `energiai-ml-service`.
10. Autenticación local (`docker login` con *auth token* OCI).
11. Build + push de ambas imágenes.

### Fase 3 — Despliegue

12. Crear Container Instance para el servicio ML (desplegar primero — el backend depende de que exista para validar su integración).
13. Verificar `GET /health` del ML service accesible dentro de la VCN.
14. Crear Container Instance para el backend, con variable de entorno `ML_SERVICE_URL` apuntando al ML service desplegado.
15. Verificar `GET /health` del backend accesible públicamente (o vía IP/puerto asignado).
16. Prueba funcional real: `POST /api/v1/analisis-energetico` contra el backend desplegado, con payload de ejemplo del contrato, verificando respuesta end-to-end (backend → ML → respuesta).

### Fase 4 — Evidencia

17. Capturar evidencia (screenshots, `curl` de salida, logs de OCI Logging) para `docs/governance/ENTREGABLES_NOCOUNTRY.md`.
18. Documentar en `infra/oci/` (hoy vacío) al menos: IPs/endpoints, comandos usados, y un `README.md` de reproducibilidad — no es necesario IaC completo (Terraform) para este primer despliegue, pero sí trazabilidad manual mínima.

---

## 5. Decisiones de simplificación explícitas para este primer despliegue

Consistentes con `architecture/03-Arquitectura-Empresarial-EnergiAI.md` §6.3:

- Sin base de datos gestionada todavía — persistencia de histórico (Tarea #11) puede ir en memoria o diferirse a una segunda iteración de despliegue.
- Sin API Gateway — exposición directa del backend vía Container Instance es aceptable para esta fase.
- Sin autoscaling ni alta disponibilidad.
- Sin dominio propio ni TLS gestionado — HTTP simple o IP directa es aceptable para evidencia técnica de hackathon (evaluar si el jurado de NoCountry requiere HTTPS; si es así, usar un *load balancer* OCI básico con certificado gestionado como paso adicional).
- Autenticación: ninguna en esta fase (consistente con "autenticación ligera o acceso controlado por entorno" del alcance MVP). No exponer datos sensibles reales — el dataset ya es agregado/anónimo.

---

## 6. Riesgos específicos de esta fase

| Riesgo | Mitigación |
|---|---|
| Cupo/cuota del *tenancy* OCI del hackathon insuficiente o no confirmado | Verificar disponibilidad de cuenta OCI **antes** de la Fase 1, con el Product Owner |
| Miembro único con acceso/conocimiento de la consola OCI (relacionado a R-05) | Documentar cada paso ejecutado en `infra/oci/README.md` a medida que se hace, no al final |
| Imagen Docker del ML service pesada por dependencias de `scikit-learn`/`pandas` | Usar imagen base `python:3.x-slim` y `--no-cache-dir` en `pip install` |
| Timeout de red entre Container Instances si la VCN no está bien configurada | Probar conectividad backend↔ML dentro de la misma VCN antes de exponer el backend públicamente |

---

## 7. Definición de "hecho" para la Tarea #10

La Tarea #10 se considera completada cuando:

- [ ] El backend responde `GET /health` con status 200 desde una URL/IP pública o accesible por el equipo.
- [ ] El ML service responde `GET /health` con status 200 (accesible al menos desde el backend).
- [ ] Una petición real `POST /api/v1/analisis-energetico` contra el backend desplegado devuelve una respuesta generada por el modelo real (no el mock del frontend).
- [ ] Existe evidencia capturada (logs, capturas, comandos) reutilizable para `docs/governance/ENTREGABLES_NOCOUNTRY.md`.
