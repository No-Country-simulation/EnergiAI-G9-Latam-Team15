# EnergiAI - Arquitectura Empresarial y MVP

**Fecha:** 2026-07-13  
**Rol:** Enterprise Software Architect Senior  
**Objetivo:** Definir la arquitectura objetivo y la arquitectura MVP de EnergiAI para clasificar usuarios por eficiencia energetica y habilitar una evolucion ordenada hacia una plataforma cloud-native sobre Oracle Cloud Infrastructure.

## 1. Resumen ejecutivo

EnergiAI es una solucion orientada al analisis de patrones de consumo energetico para clasificar usuarios en tres segmentos:

- Eficiente
- Moderado
- Ineficiente

La propuesta arquitectonica separa claramente la captura y exposicion del producto digital, el procesamiento analitico, el entrenamiento de modelos y la integracion cloud. Esto permite:

- Entregar un MVP funcional en 5 semanas.
- Reducir el riesgo de acoplamiento entre frontend, backend y ciencia de datos.
- Facilitar despliegues independientes por componente.
- Preparar una ruta de evolucion hacia una plataforma empresarial observable, segura y escalable.

## 2. Contexto de negocio y objetivos

### 2.1 Problema de negocio

Los usuarios residenciales y de pequenos comercios suelen carecer de interpretacion util de su consumo electrico. El dato existe, pero no se transforma en decisiones accionables.

### 2.2 Objetivos de negocio

- Clasificar usuarios segun su comportamiento energetico.
- Identificar patrones de uso y potenciales ineficiencias.
- Generar recomendaciones entendibles y accionables.
- Construir una solucion demostrable y escalable para el hackathon.

### 2.3 Objetivos tecnicos

- Exponer una API desacoplada para integracion con frontend.
- Separar inferencia ML del backend transaccional.
- Mantener trazabilidad de datasets, versiones de modelo y resultados.
- Desplegar una primera version operable en OCI.

## 3. Principios arquitectonicos

1. **Desacoplamiento por dominio**  
   El frontend, la capa transaccional y la capa analitica deben poder evolucionar de forma independiente.

2. **API-first**  
   Todas las integraciones entre componentes se formalizan mediante contratos HTTP/JSON versionados.

3. **MVP con ruta de escalado**  
   El diseno inicial prioriza velocidad de entrega sin bloquear una futura evolucion empresarial.

4. **Cloud pragmatica**  
   OCI se usa donde agrega valor real: hosting, almacenamiento, observabilidad y seguridad.

5. **Trazabilidad del dato y del modelo**  
   Cada resultado de clasificacion debe poder relacionarse con la entrada, la version del modelo y el timestamp de ejecucion.

## 4. Requerimientos arquitectonicos

### 4.1 Requerimientos funcionales

- Registrar o cargar datos de consumo energetico por usuario.
- Ejecutar clasificacion de eficiencia.
- Presentar resultados y recomendaciones en UI web.
- Consultar historico de evaluaciones.
- Gestionar dataset base para entrenamiento y calibracion.

### 4.2 Requerimientos no funcionales

- **Disponibilidad MVP:** media, con recuperacion operativa manual aceptable.
- **Escalabilidad:** horizontal en frontend y backend; elastica en inferencia ML a futuro.
- **Seguridad:** autenticacion basica para entorno demo y secreto centralizado.
- **Observabilidad:** logs estructurados y health checks.
- **Mantenibilidad:** repositorio monorepo con separacion por bounded context tecnico.

## 5. Arquitectura empresarial objetivo

### 5.1 Capas

#### Capa de experiencia

- Aplicacion web React.
- Visualizacion de clasificacion, indicadores y recomendaciones.

#### Capa de servicios digitales

- API Backend en Spring Boot.
- Orquestacion de solicitudes, validaciones, reglas de negocio y exposicion REST.

#### Capa analitica e inteligencia

- Servicio Python con Scikit-Learn para inferencia.
- Pipeline offline para entrenamiento, evaluacion y versionado de modelos.

#### Capa de datos

- Base relacional transaccional para usuarios, evaluaciones y metadatos.
- Object storage para datasets, artefactos de modelo y reportes.

#### Capa de plataforma

- OCI para despliegue, almacenamiento, secretos, red y observabilidad.

### 5.2 Componentes principales

#### Frontend React

- Dashboard de consumo.
- Formulario de simulacion o carga de datos.
- Vista de clasificacion y recomendaciones.
- Cliente HTTP hacia backend.

#### Backend Spring Boot

- API REST `/users`, `/consumptions`, `/classifications`, `/recommendations`.
- Validacion de payloads.
- Persistencia de historico.
- Integracion con servicio ML por REST.
- Publicacion de OpenAPI/Swagger.

#### Servicio ML Python

- Endpoint de inferencia.
- Carga de modelo entrenado.
- Normalizacion y feature engineering basico.
- Respuesta con clase, score y explicacion resumida.

#### Capa de datos

- Tabla de usuarios.
- Tabla de mediciones/consumos.
- Tabla de clasificaciones.
- Bucket para datasets y modelos serializados.

## 6. Arquitectura MVP para 5 semanas

### 6.1 Alcance MVP

El MVP debe incluir exclusivamente capacidades necesarias para demostrar valor:

- Ingreso de datos de consumo.
- Clasificacion automatica del usuario.
- Presentacion de resultado y recomendacion.
- Persistencia simple del resultado.
- Despliegue demo en OCI.

### 6.2 Arquitectura MVP propuesta

- **React** como SPA para experiencia demo.
- **Spring Boot** como backend central y facade del sistema.
- **Python Scikit-Learn** como microservicio de inferencia.
- **Base de datos relacional unica** para MVP.
- **OCI Object Storage** para datasets y modelos.
- **OCI Compute o Container Instances** para despliegue rapido.

### 6.3 Decisiones de simplificacion MVP

- Sin event streaming en primera fase.
- Sin IAM empresarial completo; autenticacion ligera o acceso controlado por entorno.
- Sin feature store dedicada.
- Entrenamiento inicialmente manual o semiautomatizado.
- Integracion sincrona backend -> ML para minimizar complejidad.

## 7. Decisiones arquitectonicas justificadas

### DA-01. Backend Spring Boot como orquestador central

**Decision:** Centralizar reglas de negocio, persistencia e integracion externa en Spring Boot.  
**Justificacion:** Permite contratos estables, reduce complejidad en frontend y desacopla la evolucion del modelo ML.

### DA-02. Servicio ML separado en Python

**Decision:** Exponer inferencia como servicio independiente.  
**Justificacion:** Scikit-Learn y el ecosistema Python aceleran el desarrollo analitico. Separarlo evita mezclar runtimes y facilita reemplazo futuro.

### DA-03. Integracion REST entre backend y ML

**Decision:** Usar HTTP/JSON en vez de librerias embebidas o colas para el MVP.  
**Justificacion:** Menor complejidad operativa, contratos claros y despliegue independiente.

### DA-04. Monorepo con dominios separados

**Decision:** Mantener frontend, backend, ML, infraestructura y documentacion en un mismo repositorio logico.  
**Justificacion:** En hackathon reduce friccion de coordinacion y acelera la trazabilidad del entregable.

### DA-05. OCI Object Storage como repositorio de artefactos

**Decision:** Guardar datasets, modelos y evidencias en Object Storage.  
**Justificacion:** Es simple, durable y nativo de OCI; evita soluciones ad hoc para artefactos.

## 8. Estrategia de integracion OCI

### 8.1 Servicios OCI recomendados

- **OCI Compute** o **Container Instances** para backend y ML.
- **OCI Object Storage** para datasets, modelos y reportes.
- **OCI API Gateway** en evolucion posterior para exposicion controlada.
- **OCI Vault** para secretos y credenciales.
- **OCI Logging / Monitoring** para observabilidad basica.
- **Autonomous Database** o base gestionada equivalente si el tiempo lo permite.

### 8.2 Arquitectura de despliegue OCI para MVP

1. Frontend desplegado como sitio estatico o servicio web ligero.
2. Backend Spring Boot desplegado en una instancia o contenedor.
3. Servicio ML desplegado por separado en otra instancia o contenedor.
4. Base de datos accesible por red privada o configuracion segura controlada.
5. Object Storage como repositorio comun de datasets y modelos.

### 8.3 Secuencia operativa recomendada

1. El equipo de datos entrena y publica el modelo.
2. El artefacto se almacena en Object Storage.
3. El servicio ML carga la version aprobada.
4. Spring Boot invoca la inferencia.
5. El resultado se persiste y se expone a React.

## 9. Seguridad y gobierno minimo viable

- Variables sensibles fuera del codigo fuente.
- CORS restringido por entorno.
- Validacion de payloads en backend.
- Sanitizacion de entradas para evitar errores de scoring.
- Versionado de modelos y datasets.
- Registro de auditoria basico para ejecuciones de clasificacion.

## 10. Riesgos y gestion arquitectonica

| Riesgo | Impacto | Probabilidad | Mitigacion |
|---|---|---:|---|
| Dataset insuficiente o de baja calidad | Alto | Alto | Usar dataset publico + sintetico y definir criterios minimos de calidad |
| Bajo rendimiento del modelo | Alto | Medio | Establecer baseline temprano y medir precision, recall y F1 |
| Acoplamiento fuerte Java-Python | Medio | Medio | Contrato REST versionado y pruebas de integracion tempranas |
| Retraso en OCI | Medio | Medio | Desplegar esqueleto en semana 2 y no al final |
| Falta de observabilidad | Medio | Medio | Logs estructurados, health endpoints y checklist de despliegue |
| Scope creep del hackathon | Alto | Alto | Proteger alcance MVP y mover extras a backlog post-demo |

## 11. Roadmap tecnico resumido

### Semana 1

- Definicion de dominio, contratos API y esquema de datos.
- Seleccion y limpieza inicial del dataset.
- Setup de repositorio, CI minima y convenciones.

### Semana 2

- Prototipo React.
- Skeleton Spring Boot.
- PoC de servicio ML.
- Primer despliegue tecnico en OCI.

### Semana 3

- Integracion end-to-end.
- Persistencia de historico.
- Entrenamiento baseline y validacion inicial.

### Semana 4

- Mejora de experiencia de usuario.
- Ajuste de modelo y recomendaciones.
- Hardening tecnico, logs, errores y pruebas.

### Semana 5

- Estabilizacion, demo scripts y evidencias.
- Afinamiento cloud, seguridad minima y documentacion final.

## 12. Conclusiones

La arquitectura recomendada para EnergiAI equilibra velocidad, claridad de responsabilidades y capacidad de evolucion. Para el hackathon, la prioridad debe ser una cadena de valor completa y demostrable: dato -> clasificacion -> recomendacion -> visualizacion. La separacion entre React, Spring Boot, Python y OCI es suficiente para sostener calidad tecnica sin sacrificar tiempo de entrega.
