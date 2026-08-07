# Auditoría del Motor de Recomendaciones — v1

**Fecha:** 2026-07-31
**Ubicación actual del código auditado:** `frontend/src/services/apiService.js` (funciones `generarRecomendaciones()` y `generarMockResponse()`)

---

## ADENDA — 2026-08-05

**La decisión pendiente en §4 ya se tomó formalmente** — ver `architecture/decisions/ADR-002-motor-recomendaciones-backend.md` y DA-06 en `architecture/03-Arquitectura-Empresarial-EnergiAI.md`: se adopta la **Opción A** (motor en el Backend), tal como recomendaba este documento.

**La implementación sigue pendiente.** `AnalisisEnergeticoService.java` (backend real, ya desplegado) retorna 3 recomendaciones fijas hardcodeadas — no las 8 reglas condicionadas descritas en la §2 de este documento. El hallazgo central de esta auditoría (la única lógica de recomendaciones real vive en el mock de frontend) **sigue siendo cierto hoy**, con el agravante de que ahora también hay un backend real en producción que no la implementa. Trabajo asignado a Cristian Coronel y Harrinson Villabona en `meetings/ActaReunion-008-ENERGIAI.md` §6.

El resto de este documento se conserva sin modificar como registro histórico de la auditoría del 2026-07-31.

---

## ADENDA — 2026-08-06: Implementación cerrada

Portado a `AnalisisEnergeticoService.java` (PR #25, mergeado a `develop`). El hallazgo central de esta auditoría ya no aplica: el backend es ahora la fuente de verdad de `recomendaciones`.

**El motor implementado no es el de la §2 de este documento.** Cristian Coronel entregó un set de reglas actualizado (6 reglas, condicionadas a `categoria` del modelo + `uso_horario_pico`/`horas_alto_consumo`/`consumo_kwh`/`tipo_inmueble`), distinto de las 8 reglas basadas solo en umbrales crudos descritas abajo. Ver `architecture/decisions/ADR-002-motor-recomendaciones-backend.md` (adenda 2026-08-06) para el detalle y un ajuste de escala pendiente de confirmar con Cristian/Harrinson (no bloqueante).

Sigue pendiente la Acción #3 de §5: alinear el texto de ejemplo de `API_CONTRACT_V1.md` con el texto real que produce el backend — el ejemplo del contrato todavía no coincide con ninguna de las 6 frases reales.

---

## 1. Hallazgo principal

El "motor de recomendaciones" de EnergiAI **existe hoy y es funcional**, pero vive enteramente dentro del mock de fallback del frontend, no en el backend ni en el servicio ML como indica el flujo documentado en `API_CONTRACT_V1.md` (`Frontend → Backend → ML Service → Modelo IA`, con `recomendaciones` como parte de la respuesta del backend). Es decir: **la única lógica de negocio de recomendaciones que existe en todo el repositorio está en una capa que la arquitectura designa como temporal (mock de contingencia ante fallo de red).**

Esto no es necesariamente un error — como estrategia de resiliencia de demo está bien resuelto (ver `planning/04-Gestion-de-Riesgos-Arquitectonicos.md`, plan de contingencia #3: "congelar interfaz con stub controlado"). El riesgo es que **nadie ha definido todavía dónde debe vivir esta lógica en la arquitectura final**, y si no se decide explícitamente, corre el riesgo de duplicarse (una versión en frontend, otra distinta en backend o ML) sin que ninguna sea la fuente de verdad.

---

## 2. Especificación del motor actual (v1, extraído del código)

### Entradas

- `consumo_kwh` (number)
- `uso_horario_pico` (boolean)
- `horas_alto_consumo` (number)

Nota: `cantidad_equipos` y `tipo_inmueble` están en el contrato de request pero **no se usan** en la lógica de recomendaciones actual — solo en la clasificación de categoría (indirectamente, vía `consumo_kwh`) y no aparecen en `generarRecomendaciones()` en absoluto.

### Reglas (orden de evaluación, todas acumulativas — no son mutuamente excluyentes)

| # | Condición | Recomendación generada |
|---|---|---|
| 1 | `consumo_kwh > 300` | "Reduzca el consumo General: revisar electrodomésticos de alto consumo..." |
| 2 | `consumo_kwh > 300` | "Considere instalar paneles solares..." |
| 3 | `consumo_kwh > 150` | "Apague los equipos en modo stand-by..." (se dispara también cuando la regla 1 ya se disparó, porque `>300` implica `>150`) |
| 4 | `uso_horario_pico === true` | "Evite el uso de electrodomésticos de alto consumo en horario pico (18:00-22:00)..." |
| 5 | `uso_horario_pico === true` | "Solicite una tarifa horaria diferenciada..." |
| 6 | `horas_alto_consumo > 6` | "Reduce las horas de alto consumo..." |
| 7 | Siempre | "Mantenga los electrodomésticos con etiquetas de eficiencia energética A o superior." |
| 8 | `consumo_kwh < 150` | "Excelente nivel de consumo. Continúe con sus buenas prácticas..." |

### Clasificación de categoría (en `generarMockResponse`, no en `generarRecomendaciones`)

```text
consumo_kwh > 300        → "Ineficiente"
150 <= consumo_kwh <= 300 → "Moderado"
consumo_kwh < 150         → "Eficiente"
```

### Costo estimado

```text
costo_estimado_mensual = consumo_kwh × 0.75
```

Coincide exactamente con la fórmula de `API_CONTRACT_V1.md` §"Regla de Cálculo Financiero MVP" — es el único punto donde el mock y el contrato están explícitamente alineados por diseño.

### Probabilidad

`probabilidad: 0.85` — valor **fijo/hardcodeado**, no calculado. Esto es coherente con ser un mock, pero debe quedar explícito: ningún resultado del mock refleja confianza real de un modelo, siempre reporta 85%.

---

## 3. Comparación contra el ejemplo del contrato oficial

`API_CONTRACT_V1.md` incluye este ejemplo de respuesta:

```json
{
  "categoria": "Ineficiente",
  "probabilidad": 0.81,
  "costo_estimado_mensual": 315.00,
  "recomendaciones": [
    "Reducir el uso de equipos durante horarios pico",
    "Evaluar equipos con alto consumo energético",
    "Distribuir actividades de mayor consumo a lo largo del día"
  ]
}
```

**El texto de las recomendaciones de ejemplo en el contrato no coincide literalmente con ninguna de las 8 frases que produce el motor actual del frontend.** No es un error funcional (el contrato no obliga a un texto exacto, solo a la forma del campo `recomendaciones: array`), pero sí es una señal de que el contrato y la implementación del mock se escribieron sin verificación cruzada. Si el backend o el modelo ML terminan generando texto distinto al del frontend, y en algún punto ambos coexisten (p. ej. durante una migración), el usuario podría ver redacciones inconsistentes entre sesiones según si la llamada real tuvo éxito o cayó al mock.

---

## 4. Decisión arquitectónica pendiente

Esta auditoría no toma la decisión por el equipo, pero la deja planteada con las opciones reales:

| Opción | Ventaja | Desventaja |
|---|---|---|
| **A. Mover el motor de reglas al Backend (Spring Boot)** | Consistente con el rol de "orquestador central" que la arquitectura ya le asigna al backend (DA-01); las reglas son deterministas, no requieren ML, encajan mejor en lógica de negocio tradicional | Duplica trabajo si luego se decide que las recomendaciones deben derivarse del modelo ML (p. ej. según *feature importance*) |
| **B. Mover el motor de reglas al Servicio ML** | Las recomendaciones podrían evolucionar para basarse en las variables que el modelo ya identificó como más influyentes (`consumo_kwh` 46%, `horas_alto_consumo` 31%, según `INFORME_HIBRIDO_v3.md` §6) | Mezcla lógica de negocio simple con la capa de inferencia, contraviniendo el principio de desacoplamiento por dominio (arquitectura §3.1) |
| **C. Mantenerlo en frontend, pero formalizarlo (no como mock, sino como motor v1 real, con backend delegando en el futuro)** | Cero trabajo adicional en esta iteración; ya está probado (`frontend/tests/apiService.test.js`) | Contradice el flujo documentado en `API_CONTRACT_V1.md`, donde `recomendaciones` es responsabilidad del backend/ML, no del cliente |

**Recomendación de esta auditoría:** **Opción A** para el MVP del Sprint 2. Las reglas actuales son simples, deterministas y no dependen de ningún resultado probabilístico del modelo — son exactamente el tipo de lógica que el backend, como orquestador central, debería poseer. Portar `generarRecomendaciones()` de JavaScript a Java es un trabajo directo (mismas 8 reglas, mismos umbrales) y puede hacerse en paralelo a la implementación del endpoint principal (Tarea #4), sin bloquear ni ser bloqueado por el servicio ML. La Opción B queda como evolución legítima post-MVP, una vez el modelo esté en producción y se quiera enriquecer las recomendaciones con explicabilidad basada en *feature importance*.

---

## 5. Acciones concretas recomendadas

1. Portar las 8 reglas de `generarRecomendaciones()` al backend como parte de la implementación de `POST /api/v1/analisis-energetico` (Tarea #4) — mismos umbrales, mismo texto, para no introducir regresión de UX.
2. Mantener `generarMockResponse()` en el frontend **únicamente como fallback de contingencia** (ya cumple ese rol correctamente), pero documentar explícitamente en el código (comentario breve) que es un duplicado intencional del motor real del backend, para que no diverja sin que alguien lo note.
3. Alinear el texto de ejemplo de `API_CONTRACT_V1.md` con el texto real que el backend termine produciendo, una vez portado — hoy el contrato tiene un ejemplo ilustrativo que no es el texto real de ningún lado del sistema.
4. Decidir explícitamente, en la próxima acta de seguimiento, cuál de las opciones A/B/C se adopta, y registrarlo como decisión arquitectónica (DA-06) en `architecture/03-Arquitectura-Empresarial-EnergiAI.md`.
