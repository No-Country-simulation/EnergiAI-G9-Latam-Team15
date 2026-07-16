# Roadmap Tecnico MVP - 5 Semanas

**Fecha:** 2026-07-13  
**Objetivo:** Ordenar la ejecucion tecnica del MVP EnergiAI con foco en entrega demostrable, control de riesgo y despliegue en OCI.

## Semana 1 - Fundaciones

### Objetivos

- Cerrar alcance MVP.
- Definir contratos entre frontend, backend y ML.
- Seleccionar dataset y criterios de calidad.

### Entregables

- Modelo de dominio inicial.
- OpenAPI preliminar.
- Dataset identificado y documentado.
- Estructura base de repositorio.

### Riesgos a controlar

- Ambiguedad funcional.
- Dataset no apto para clasificacion.

## Semana 2 - Vertical slice tecnico

### Objetivos

- Levantar skeleton de React, Spring Boot y Python.
- Ejecutar primer flujo de punta a punta.
- Validar despliegue inicial en OCI.

### Entregables

- Formulario basico en React.
- Endpoint backend operativo.
- Endpoint ML con respuesta mock o baseline.
- Primer despliegue tecnico cloud.

### Riesgos a controlar

- Problemas de conectividad entre servicios.
- Retraso en configuracion OCI.

## Semana 3 - Integracion funcional

### Objetivos

- Conectar inferencia real.
- Persistir historico.
- Consolidar resultado funcional del MVP.

### Entregables

- Flujo React -> Spring Boot -> Python -> DB.
- Primer modelo entrenado y medido.
- Almacenamiento de artefactos en OCI Object Storage.

### Riesgos a controlar

- Latencia del servicio ML.
- Errores de contrato entre backend y servicio analitico.

## Semana 4 - Calidad y experiencia

### Objetivos

- Mejorar UX.
- Afinar recomendaciones y calidad del modelo.
- Agregar observabilidad y manejo de errores.

### Entregables

- Dashboard mas claro para la demo.
- Recomendaciones explicativas.
- Logs estructurados y health checks.
- Smoke tests integrados.

### Riesgos a controlar

- Scope creep.
- Deuda tecnica oculta.

## Semana 5 - Estabilizacion y demo

### Objetivos

- Congelar alcance.
- Ejecutar pruebas finales.
- Preparar narrativa tecnica y funcional del hackathon.

### Entregables

- Version demo estable.
- Checklist de despliegue.
- Evidencias de precision y arquitectura.
- Documentacion final lista para presentacion.

### Riesgos a controlar

- Fallos de ultimo minuto.
- Dependencias manuales no documentadas.

## Checklist transversal

- [ ] Contratos API versionados
- [ ] Dataset trazable
- [ ] Modelo versionado
- [ ] Variables de entorno documentadas
- [ ] Evidencia de despliegue OCI
- [ ] Demo script probado
