# Contrato Interno — Backend ↔ ML Service

## Proyecto

**EnergiAI**
Hackathon ONE G9 LATAM | Alura + Oracle + NoCountry

**Estado:** Vigente — documentado a partir de la implementación real (2026-08-05, ver ADR-001)
**Responsable:** Bernardo Adolfo Gómez Montoya — Software / Solution Architect

---

## Objetivo

`architecture/contracts/API_CONTRACT_V1.md` define el contrato **Frontend↔Backend**, pero nunca definió el contrato **Backend↔ML Service** — riesgo R-03 de `planning/04-Gestion-de-Riesgos-Arquitectonicos.md`. Este documento cierra ese vacío, describiendo el contrato tal como quedó implementado en `backend/src/main/java/com/energiai/client/MlClient.java` y `ml-service/inference.py`, no como una propuesta nueva.

---

## Endpoints expuestos por el ML Service

### `GET /health`

Estado del servicio y si el modelo está cargado en memoria. Implementado en `ml-service/inference.py`.

### `POST /predict`

Recibe las 5 features del contrato Frontend↔Backend (reenviadas tal cual desde `AnalisisRequestDTO`) y devuelve categoría + probabilidad.

**Request** (idéntico al payload de `AnalisisRequestDTO`, ver `API_CONTRACT_V1.md`):

```json
{
  "consumo_kwh": 420,
  "uso_horario_pico": true,
  "cantidad_equipos": 10,
  "tipo_inmueble": "Casa",
  "horas_alto_consumo": 8
}
```

**Response** (`MlClient.PredictResponse`):

```json
{
  "categoria": "Ineficiente",
  "probabilidad": 0.81
}
```

El ML Service **no** calcula `costo_estimado_mensual` ni `recomendaciones` — esos campos los agrega el Backend (`AnalisisEnergeticoService`) antes de responder al Frontend. Ver `architecture/03-Arquitectura-Empresarial-EnergiAI.md` DA-06 para el estado de la lógica de recomendaciones.

---

## Configuración de red

- Variable de entorno del Backend: `ML_SERVICE_URL` (`MlClient.java`, default `http://localhost:8000`).
- En `docker-compose.yml`: `ML_SERVICE_URL=http://ml-service:8000` (comunicación por nombre de servicio en la red interna `energiai-net`, no por puerto de host).
- El backend arranca solo cuando el ML service reporta `service_healthy` (`docker-compose.yml`, `depends_on`).

---

## Manejo de fallos

`AnalisisEnergeticoService.procesarAnalisis()` envuelve la llamada a `mlClient.predecir()` en un `try/catch`: si el ML service no responde, el backend **no propaga el error 500 al frontend** — responde con un valor de contingencia fijo (`categoria = "Ineficiente"`, `probabilidad = 0.81`) y registra un `log.warn`. Esto es una decisión de resiliencia de demo, análoga a la del mock de frontend (ver `docs/architecture/MOTOR_RECOMENDACIONES_v1.md`), pero **no está documentada en ningún otro lugar** — se deja registrada aquí para que no se pierda como conocimiento tácito. Riesgo: un fallo real del ML service en producción/demo puede pasar desapercibido, porque el usuario ve una respuesta "normal" en vez de un error visible.

---

## Consistencia train/serve

`ml-service/train.py` y `ml-service/inference.py` comparten el mismo `CATEGORICAL_FEATURES = ["tipo_inmueble"]` con `OneHotEncoder(handle_unknown='ignore')`, y ambos corren en el mismo entorno (el modelo se entrena dentro del build de `ml-service/Dockerfile`, en el mismo contenedor que luego lo sirve) — por lo que hoy **no hay riesgo de *training-serving skew*** por versiones de librerías distintas. El riesgo vigente es otro: `tipo_inmueble` solo soporta 2 categorías reales (`Casa`, `Pequeño establecimiento`), ver corrección aplicada en `API_CONTRACT_V1.md` el 2026-08-05.

---

## Documentos relacionados

- `architecture/contracts/API_CONTRACT_V1.md` — contrato Frontend↔Backend
- `architecture/decisions/ADR-001-contrato-integracion-v1.md`
- `backend/src/main/java/com/energiai/client/MlClient.java`
- `ml-service/inference.py`
- `docker-compose.yml`
