# Gestion de Riesgos Arquitectonicos

**Fecha:** 2026-07-13  
**Objetivo:** Formalizar los riesgos tecnicos y operativos del MVP EnergiAI y definir acciones concretas de mitigacion.

## Matriz de riesgos

| ID | Riesgo | Categoria | Impacto | Probabilidad | Nivel | Mitigacion | Responsable sugerido |
|---|---|---|---:|---:|---|---|---|
| R-01 | Dataset insuficiente, sesgado o poco representativo | Datos | Alto | Alto | Critico | Validar dataset en semana 1, complementar con sintetico y definir criterios minimos de calidad | Data Scientist / Data Engineer |
| R-02 | Precision del modelo por debajo de lo esperado | ML | Alto | Medio | Alto | Establecer baseline temprano, medir F1 y ajustar variables relevantes | Data Scientist |
| R-03 | Contrato inestable entre Spring Boot y Python | Integracion | Alto | Medio | Alto | Congelar esquema JSON, documentar OpenAPI y ejecutar pruebas de integracion | Software Architect / Backend |
| R-04 | Despliegue OCI tardio o incompleto | Plataforma | Medio | Medio | Medio | Ejecutar PoC cloud en semana 2 y mantener checklist de despliegue | Software Architect / Infra |
| R-05 | Dependencia excesiva de personas clave | Equipo | Alto | Medio | Alto | Repartir conocimiento, documentar decisiones y evitar componentes opacos | Product Owner / Architect |
| R-06 | Scope creep durante el hackathon | Gestion | Alto | Alto | Critico | Proteger backlog MVP y mover extras a lista post-demo | Product Owner |
| R-07 | Baja observabilidad en ambiente demo | Operacion | Medio | Medio | Medio | Incorporar logs, health checks y comandos de verificacion | Backend / Infra |
| R-08 | Exposicion insegura de secretos o credenciales | Seguridad | Alto | Bajo | Medio | Usar variables de entorno y, si es posible, OCI Vault | Architect / Backend |

## Estrategia de tratamiento

### Riesgos criticos

- R-01 Dataset insuficiente
- R-06 Scope creep

Ambos deben ser tratados en la primera semana porque comprometen directamente la viabilidad del MVP.

### Riesgos altos

- R-02 Precision del modelo
- R-03 Contrato entre servicios
- R-05 Dependencia de personas clave

Deben revisarse al menos dos veces por semana en el seguimiento tecnico.

## Indicadores de alerta temprana

- No existe dataset aprobado al cierre de la semana 1.
- No hay flujo end-to-end funcionando al cierre de la semana 2.
- El modelo no supera el baseline acordado al cierre de la semana 3.
- OCI sigue pendiente al iniciar la semana 4.
- La demo depende de ejecuciones manuales no documentadas en la semana 5.

## Plan de contingencia

1. Si el modelo no alcanza calidad suficiente, usar baseline interpretable y reforzar valor con recomendaciones.
2. Si OCI presenta bloqueo operativo, mantener despliegue local reproducible y preparar narrativa tecnica con evidencia de integracion parcial.
3. Si falla la integracion backend-ML, congelar interfaz con stub controlado para sostener la demo.

## Gobierno recomendado

- Revision de riesgos dos veces por semana.
- Semaforo simple: verde, amarillo, rojo.
- Todo riesgo en rojo debe tener owner y fecha compromiso.
