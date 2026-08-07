# ACTA DE REUNIÓN 005 – ENERGIAI

## Fecha
27 de julio de 2026

## Hora
11:30 a.m. (Colombia / Perú)

## Medio
Canal de voz + texto Discord – #general (reunión no grabada formalmente)

---

# Nota metodológica

> Esta acta se reconstruye **el 28 de julio**, un día después de la reunión,
> a partir del hilo de texto en #general y de lo reportado verbalmente por
> los asistentes, ya que la reunión fue breve y no se generó acta en el
> momento. Se documenta así para no perder trazabilidad, y queda sujeta a
> corrección por cualquier asistente que recuerde algo distinto.

---

# Objetivo de la reunión

Formalizar el cierre de Sprint 1 y la apertura de Sprint 2, y resolver la
duda pendiente sobre la fuente de datos final del proyecto (dataset XM
sintético vs. propuesta de Cristian).

---

# Asistentes

- Luis Angel Chavez Mejía – Product Owner
- Bernardo Adolfo Gómez Montoya – Software / Solution Architect
- Harrinson Villabona – Data Scientist
- Carlos Fabián Mesa Muñoz – Backend Developer
- Elvis Leniker Trinidad Caldas – Backend Developer
- Magno Cristian Coronel Salazar – Data Analyst
- Alonso Carbajal – Full Stack Developer

Asistió la totalidad del equipo activo (7 de 8 roles).

# Ausentes

- Anayely Reyes ("Amy" en Discord) – Data Engineer

---

# Temas tratados

1. Cierre formal de Sprint 1 (el cierre de facto había ocurrido el domingo
   26/07, se formalizó verbalmente en esta reunión).
2. Apertura formal de Sprint 2, según cronograma semanal del proyecto.
3. Revisión del estado del Dataset Maestro v2 (XM-calibrado, PR #5) — se
   valoró como un resultado sólido.
4. Discusión sobre si comparar el dataset XM contra la propuesta de GoiEner
   de Cristian antes de tomar la decisión final — se acordó esperar su
   análisis (entregado esa misma noche) para decidir con evidencia.
5. Backend (Carlos, Elvis) coordinó el arranque de los primeros endpoints
   de la API, aprovechando que el contrato (`API_CONTRACT_V1`) y las
   variables ya están definidos.
6. Se identificó que el backlog de Sprint 2 aún está en proceso de
   consolidación; el equipo acordó colaborar activamente en su elaboración
   para no perder tiempo antes de la próxima reunión.

---

# Avances logrados

✅ Cierre de Sprint 1 formalizado.

✅ Apertura de Sprint 2 formalizada.

✅ Backend inicia desarrollo de endpoints (Carlos y Elvis coordinando).

✅ Acuerdo de esperar el análisis de GoiEner (Cristian) para decisión de
dataset basada en evidencia, no en preferencia.

---

# Pendiente / gaps detectados

1. **Backlog de Sprint 2 aún en consolidación** — necesario para planificar
   tareas concretas; el equipo colabora en su elaboración.
2. **Decisión final de dataset no tomada** — pendiente de comparación
   técnica (ver documento de auditoría en #data-analyst, 28/07).
3. **PR #4 (Frontend)** comentado positivamente en la reunión, pero **sin
   review formal en GitHub** en el momento — corregido el 28/07.
4. **Reunión sin acta en vivo** — corregido con este documento reconstruido.


---

# Acuerdos

✅ Comparar objetivamente el dataset XM-sintético (v2) contra la propuesta
GoiEner antes de decidir la fuente final.

✅ Backend arranca desarrollo de endpoints en paralelo, sin esperar la
decisión de dataset (el contrato ya está congelado).

✅ Reunión de seguimiento tipo relámpago el **28/07 a las 11:30am**, abierta
a quienes puedan conectarse, para resolver dudas y afinar la agenda de
Sprint 2.

---

# Compromisos

| Responsable | Actividad |
|---|---|
| Bernardo Gómez Montoya | Auditar dataset GoiEner con el mismo rigor aplicado al propio; proponer integración híbrida si corresponde |
| Magno Cristian Coronel | Completar análisis de GoiEner (entregado la noche del 27/07) |
| Carlos Fabián Mesa / Elvis Trinidad | Iniciar implementación de endpoints backend sobre `API_CONTRACT_V1` |
| Bernardo Gómez Montoya | Revisar y formalizar (review + merge) el PR #4 de Frontend |
| Luis Angel Chavez Mejía / equipo | Consolidar backlog de Sprint 2, con apoyo del equipo |

---

# Próximos pasos

1. Cerrar la comparación técnica XM vs. GoiEner (evidencia en #data-analyst).
2. Definir dataset final: XM, GoiEner, o híbrido.
3. Consolidar backlog de Sprint 2 entre todos.
4. Reunión relámpago 28/07 11:30am: dudas, avance del dataset híbrido y
   afinación de tareas.

---

# Estado General del Proyecto (al cierre de este documento)

✅ Sprint 1 cerrado formalmente

✅ Sprint 2 abierto formalmente

✅ Dataset Maestro v2 (XM) construido, documentado, en PR #5

✅ Frontend completo, PR #4 revisado y aprobado formalmente (28/07)

🟡 Decisión final de dataset pendiente (evaluación híbrida en curso)

🟡 Backlog de Sprint 2 en consolidación, con apoyo colectivo del equipo

🟡 Backend en arranque temprano de endpoints

---

# Conclusión

La reunión del 27/07, aunque breve y sin registro formal en el momento,
contó con la participación de la totalidad del equipo activo y permitió
avanzar decisiones clave: cierre de Sprint 1, apertura de Sprint 2, y el
acuerdo de decidir la fuente de datos final con evidencia técnica en vez
de preferencia. Queda como prioridad para la reunión relámpago del 28/07
consolidar el backlog de Sprint 2 entre todos y despejar dudas puntuales.
