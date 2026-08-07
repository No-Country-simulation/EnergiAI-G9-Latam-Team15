# Acta de Reunión 008 — Proyecto EnergiAI (G9-LATAM Team 15)

**Fecha:** martes 4 de agosto de 2026
**Hora:** 11:30 a.m. (hora Colombia/Perú)
**Modalidad:** Virtual (Discord)
**Simulación:** NoCountry — Hackathon ONE G9-LATAM (Oracle / Alura)
**Elaborada por:** Bernardo Gómez — Solution / Software Architect

---

## 1. Asistentes

Equipo activo (7 integrantes): Bernardo Gómez (Architect), Elvis Trinidad y Carlos Fabián Mesa (Backend), Harrinson Villabona (Data Scientist), Alonso Carbajal (Full Stack), Magno Cristian Coronel (Data Analyst), Luis Ángel Chávez Mejía (Product Owner).

---

## 2. Objetivo de la reunión

Mostrar el **producto funcionando end-to-end** (demo en vivo), identificar mejoras de usabilidad y contenido, y repartir responsabilidades con fecha de entrega antes de la próxima reunión.

---

## 3. Desarrollo — demo del producto

Se presentó **EnergiAI corriendo de punta a punta** en el entorno local (frontend → backend → modelo ML), con el stack completo en Docker:
- Formulario de datos de consumo, clasificación (Eficiente / Moderado / Ineficiente) con % de confianza, costo mensual estimado y recomendaciones.
- Historial de análisis y gráfica de evolución.
- Respuesta proveniente del **modelo real** (no mock), verificada con distintos perfiles.
- Las 3 imágenes del stack (frontend, backend, ml-service) ya subidas al registry de OCI (OCIR).

El equipo constató que **la parte más difícil del proyecto ya está superada**: el sistema funciona integrado. Lo que sigue es pulir usabilidad y cerrar el despliegue público.

---

## 4. Hallazgos de mejora (usabilidad y contenido)

1. **Ortografía:** pequeños errores en el frontend y en los mensajes de ayuda (tooltips de los "?"). Deben corregirse para una presentación profesional.
2. **Gráfica de evolución:** el eje horizontal es poco legible (muestra solo "04-ago" repetido). Debe formatearse (fecha + hora / agrupación real) para que sea clara y demostrativa para el usuario.
3. **Historial de análisis:** se ve bien; se evaluará usarlo como fuente para mejorar la gráfica de evolución.
4. **Recomendaciones:** enriquecerlas usando la data disponible (hoy son 3 genéricas), para que sean más específicas por perfil.
5. **Elevar el uso de la IA:** explorar qué más puede predecir/recomendar el modelo con los datos que ya se tienen.

---

## 5. Decisiones y acuerdos

- **Continuar** el proyecto como se viene llevando, siguiendo las pautas del **Product Owner**.
- **Repartir las mejoras por responsabilidad**, con entrega **antes de la reunión del jueves**.
- **Regla de entrega:** todo cambio debe quedar en GitHub (rama + PR a `develop`) antes del jueves — lo que quede solo en local/Drive no cuenta para la demo.
- **Bernardo** continúa con el **despliegue en OCI** (Container Instance + URL pública), y re-despliega con las mejoras cuando estén en `develop`.

---

## 6. Reparto de responsabilidades (entrega antes del jueves)

| Responsable | Tarea |
|---|---|
| **Alonso** (Full Stack) | Corregir ortografía (frontend + tooltips "?"). Arreglar la legibilidad de la gráfica de evolución (eje X). |
| **Cristian** (Data Analyst) + **Harrinson** (Data Scientist) | Enriquecer recomendaciones con la data disponible. Explorar más valor de la IA (más predicciones/recomendaciones). |
| **Elvis + Carlos** (Backend) | Soporte a los cambios de recomendaciones si requieren ajuste en el backend. |
| **Luis Ángel** (PO) | Priorizar qué mejoras entran en la demo final vs. roadmap. |
| **Bernardo** (Architect) | Cerrar el despliegue en OCI (Container Instance + URL pública). |

---

## 7. Mejoras mayores (Fase 2 / roadmap — para el pitch, no para el jueves)

- Historial temporal del perfil (login + persistencia por evento).
- Modelo re-entrenable con más categorías de inmueble (apartamento, etc.) y con datos reales del uso.
- Motor de recomendaciones más completo.
- Contrato de datos formalizado entre frontend, backend y ML.

---

## 8. Próxima reunión

**Jueves 6 de agosto de 2026, 11:30 a.m.** — Revisión de las mejoras entregadas y estado del despliegue en OCI.

---

*Acta elaborada como registro oficial del proyecto. Ubicación: `meetings/ActaReunion-008-ENERGIAI.md`.*
