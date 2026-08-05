# Despliegue OCI — EnergiAI

**Estado:** Desplegado (confirmado en `meetings/ActaReunion-008-ENERGIAI.md`, demo 2026-08-04).
**Responsable:** Bernardo Adolfo Gómez Montoya — Software / Solution Architect.
**Última actualización:** 2026-08-05.

> Este documento reemplaza el vacío señalado en `docs/deployment/CHECKLIST_OCI.md` (Fase 4: *"`infra/oci/README.md` (hoy inexistente)"*). Contiene lo verificable desde el repositorio; los campos marcados `[COMPLETAR]` requieren que Bernardo los rellene con los valores exactos de la consola OCI — no se inventaron para no dejar documentación incorrecta.

---

## 1. Registro de imágenes (OCI Container Registry — OCIR)

Confirmado — las 3 imágenes del stack están publicadas:

| Servicio | Imagen |
|---|---|
| Frontend | `bog.ocir.io/axvu1ir8dwvf/energiai-frontend:v2` |
| Backend | `bog.ocir.io/axvu1ir8dwvf/energiai-backend:v1` |
| ML Service | `bog.ocir.io/axvu1ir8dwvf/energiai-ml:v1` |

Región: Bogotá (`bog` en el hostname de OCIR).

> **Nota (2026-08-05):** el frontend quedó en `:v2` porque se reconstruyó después del fix de proxy Nginx / `VITE_API_URL` (commit `556f9ce`) — la `:v1` original no tenía esa corrección. Backend y ML Service no necesitaron rebuild y siguen en `:v1`.

## 2. Cómputo usado para el despliegue

**OCI Container Instances** (no VM Compute — los scripts locales `cazador_oci.py` sobre
`VM.Standard.A1.Flex` fueron un camino explorado en paralelo, pero el despliegue que
quedó funcionando es sobre Container Instance).

- Container Instance: estado `ACTIVE`, alojando los 3 contenedores del stack
  (`ml-service:v1`, `backend:v1`, `frontend:v2`) como grupo.
- Memoria: **8GB** — el intento inicial con 2GB fallaba por memoria insuficiente; se
  subió a 8GB y ahí quedó estable.
- `[COMPLETAR: Bernardo]` — OCID de la instancia, Availability Domain exacto y
  cantidad de OCPUs asignadas (no quedaron registrados en las notas de seguimiento).

## 3. Red

- VCN: `energiai-vcn` (10.0.0.0/16), región **Bogotá (BOG / sa-bogota-1)**, con
  subred pública + privada disponibles.
- `[COMPLETAR: Bernardo]` — confirmar en cuál subred quedó la Container Instance
  (pública, dado que expone `149.130.187.192` directamente) y las reglas exactas
  de Security List/NSG que permiten el tráfico entrante al frontend/backend.

## 4. Acceso público

**URL:** `http://149.130.187.192`

Verificado funcionando: formulario cargando, análisis respondiendo, historial
mostrando resultados reales (captura del 5-ago-2026, ~8:37am).

## 5. Variables de entorno usadas en el despliegue

Basado en `docker-compose.yml` (equivalentes deben configurarse en el entorno OCI):

| Variable | Servicio | Propósito |
|---|---|---|
| `ML_SERVICE_URL` | Backend | URL interna del ML Service (local: `http://ml-service:8000`) |
| `VITE_API_URL` | Frontend (build-time) | URL del backend; en producción se deja **vacía** para que `frontend/nginx.conf` haga proxy relativo (ver commit `556f9ce`, fix del bug `||` vs `??`) |

`[COMPLETAR: Bernardo]` — valores reales usados en OCI para `ML_SERVICE_URL` si difieren del nombre de servicio de docker-compose (en una VM con docker-compose serían iguales; en Container Instances separadas requeriría IP/hostname interno de OCI).

## 6. Reproducir el build y push localmente

```bash
# Desde la raíz del repo
docker build -f ml-service/Dockerfile -t bog.ocir.io/axvu1ir8dwvf/energiai-ml:v1 .
docker build -f backend/Dockerfile -t bog.ocir.io/axvu1ir8dwvf/energiai-backend:v1 ./backend
docker build -f frontend/Dockerfile -t bog.ocir.io/axvu1ir8dwvf/energiai-frontend:v2 ./frontend

# Login (usar auth token OCI, no la contraseña de la consola)
docker login bog.ocir.io -u '<tenancy-namespace>/<usuario>'

docker push bog.ocir.io/axvu1ir8dwvf/energiai-ml:v1
docker push bog.ocir.io/axvu1ir8dwvf/energiai-backend:v1
docker push bog.ocir.io/axvu1ir8dwvf/energiai-frontend:v2
```

## 7. Evidencia pendiente

Según `docs/deployment/CHECKLIST_OCI.md` Fase 4, falta trasladar a `docs/governance/ENTREGABLES_NOCOUNTRY.md`: capturas de la consola OCI, salida de `curl` contra el backend desplegado, y logs si OCI Logging llegó a habilitarse.

## Documentos relacionados

- `docs/deployment/PLAN_DESPLIEGUE_OCI_v1.md` — plan original
- `docs/deployment/CHECKLIST_OCI.md` — checklist operativo (ver adenda 2026-08-05 en ese archivo)
- `architecture/03-Arquitectura-Empresarial-EnergiAI.md` §8 — estrategia de integración OCI, actualizada 2026-08-05
