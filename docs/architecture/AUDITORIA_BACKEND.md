# Auditoría Técnica — Backend

**Módulo:** `backend/`
**Fecha:** 2026-07-31
**Tecnología declarada:** Spring Boot (Java) — según `README.md`, `architecture/03-Arquitectura-Empresarial-EnergiAI.md` y `backend/README.md`.

---

## 1. Estado actual (evidencia)

```text
backend/
├── README.md
└── src/
    ├── main/
    │   ├── java/          <- solo .gitkeep
    │   └── resources/     <- solo .gitkeep
    └── test/
        └── java/          <- solo .gitkeep
```

- **No existe `pom.xml` ni `build.gradle`/`build.gradle.kts`.** No hay proyecto Maven/Gradle inicializado. No se puede compilar ni ejecutar `backend/` en su estado actual.
- **No existe una sola clase Java** en el repositorio (`find` dirigido a `.java` no arroja resultados).
- **No existe `application.yml` ni `application.properties`.**
- `backend/README.md` documenta responsabilidad y estructura *esperada*, pero es documentación de intención, no de estado.

**Conclusión:** el backend no está "en progreso" en términos de código versionado — está en blanco. Cualquier avance mencionado como "🟡 En ejecución" en `meetings/ActaReunion-006-ENERGIAI.md` (Tareas #4 y #5 del backlog) no está reflejado en `develop` a la fecha de esta auditoría. Si existe trabajo local no pusheado, debe integrarse cuanto antes para que esta auditoría deje de aplicar.

---

## 2. Verificación de endpoints requeridos por `API_CONTRACT_V1`

| Endpoint | Especificado en contrato | Implementado | Evidencia |
|---|---|---|---|
| `POST /api/v1/analisis-energetico` | ✅ Sí (`architecture/contracts/API_CONTRACT_V1.md`) | ❌ No | Sin código fuente Java en el repositorio |
| `GET /health` | Requerido por Backlog Sprint 2, Tarea #9 (no está en `API_CONTRACT_V1`, es requisito operativo) | ❌ No | Sin código fuente Java en el repositorio |
| Manejo de error 400 (payload inválido) | ✅ Sí (contrato define `status/code/message`) | ❌ No | — |
| Manejo de error 500 (error interno) | ✅ Sí (contrato define `status/code/message`) | ❌ No | — |

---

## 3. Gap frente a la arquitectura empresarial declarada

`architecture/03-Arquitectura-Empresarial-EnergiAI.md` (§5.2) describe el backend como orquestador central con:

- API REST `/users`, `/consumptions`, `/classifications`, `/recommendations` — **no implementada** (y de alcance mayor al MVP acordado en el backlog, que solo exige `/api/v1/analisis-energetico` y `/health`; recomendación: no construir estos 4 recursos adicionales hasta después del despliegue OCI, para no desviar el foco del Sprint 2).
- Validación de payloads — **no implementada.**
- Persistencia de historico — **no implementada** (Tarea #11 del backlog, prioridad alta pero no crítica).
- Integración con servicio ML por REST — **no implementada** (depende de que el servicio ML exista, ver `docs/architecture/AUDITORIA_ML.md`).
- Publicación de OpenAPI/Swagger — **no implementada.** `planning/01-Roles.md` asigna Swagger como responsabilidad explícita de Backend Developers.

---

## 4. Riesgo de desalineación de contrato (frontend ↔ backend)

`frontend/src/services/apiService.js:79` construye la llamada como:

```js
fetch(`${API_URL}/analisis-energetico`, { method: "POST", ... })
```

Mientras que `API_CONTRACT_V1.md` especifica la ruta completa:

```http
POST /api/v1/analisis-energetico
```

Si el backend se implementa exponiendo exactamente `/api/v1/analisis-energetico` (lo correcto según contrato) y `VITE_API_URL` apunta a la raíz del servicio (p. ej. `http://backend:8080`), la petición del frontend resolverá a `http://backend:8080/analisis-energetico`, que **no existirá**, y la app caerá silenciosamente al mock (ver `AUDITORIA_PROYECTO_v1.md` §3.3). Esto puede pasar desapercibido en demo porque el fallback es funcional, pero significa que la integración real nunca se estaría probando.

**Acción recomendada:** decidir en una única fuente de verdad — o el backend expone la ruta sin prefijo (y se actualiza `API_CONTRACT_V1.md`), o se corrige `apiService.js` para incluir `/api/v1`. Se recomienda esto último, por ser el contrato ya congelado y socializado.

---

## 5. Qué se necesita para llegar a un backend desplegable (mínimo viable)

1. Inicializar proyecto Spring Boot (Spring Initializr o manual): `pom.xml` con dependencias `spring-boot-starter-web`, `spring-boot-starter-validation`, `spring-boot-starter-actuator` (este último resuelve `GET /health` de forma nativa vía `/actuator/health`, evaluar si se expone como `/health` directo o se documenta la ruta de Actuator).
2. Estructura de paquetes mínima: `controller`, `service`, `dto`, `client` (para el cliente HTTP hacia ML service), `exception` (manejador global `@ControllerAdvice` para los errores 400/500 del contrato).
3. `application.yml` con perfiles `local` / `oci` y variables externalizadas (`ML_SERVICE_URL`, `SERVER_PORT`, etc.) — sin credenciales hardcodeadas.
4. Implementar `POST /api/v1/analisis-energetico`:
   - DTO de entrada validado según §"Definición de Campos" del contrato (`consumo_kwh`, `uso_horario_pico`, `cantidad_equipos`, `tipo_inmueble` con enum restringido, `horas_alto_consumo`).
   - Llamada HTTP síncrona al servicio ML (`RestTemplate`/`WebClient`).
   - Respuesta mapeada exactamente al esquema del contrato (`categoria`, `probabilidad`, `costo_estimado_mensual`, `recomendaciones`).
5. Implementar `GET /health` devolviendo estado propio y, opcionalmente, verificación de alcance del servicio ML.
6. Tests unitarios mínimos en `src/test/java` (hoy vacío) para el controller y el manejo de errores.
7. `Dockerfile` multi-stage (build Maven + runtime JRE liviano) — inexistente hoy, requisito directo para OCI Container Instances.

---

## 6. Veredicto

**Estado:** 🔴 Bloqueante crítico para la Tarea #10 del Backlog Sprint 2.
**Esfuerzo estimado para MVP desplegable:** endpoint único + health + Dockerfile es alcanzable en 1-2 días de un desarrollador backend dedicado, **una vez que el servicio ML tenga al menos un `POST /predict` funcional** (aunque sea con modelo baseline). No hay razón técnica para no empezar el backend en paralelo con stub del servicio ML.
