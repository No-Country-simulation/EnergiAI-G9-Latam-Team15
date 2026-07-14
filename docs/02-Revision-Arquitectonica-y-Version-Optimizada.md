# Revision Arquitectonica, Validacion y Version Optimizada del MVP

**Fecha:** 2026-07-13  
**Rol:** Chief Software Architect / Technical Project Manager  
**Objetivo:** Validar la documentacion existente de EnergiAI, identificar riesgos reales de ejecucion y proponer una version optimizada para maximizar la probabilidad de exito en 5 semanas de hackathon.

## 1. Dictamen ejecutivo

La arquitectura propuesta para EnergiAI es **coherente, moderna y tecnicamente defendible** para una solucion orientada a analisis de consumo energetico. La separacion entre React, Spring Boot y Python Scikit-Learn es correcta desde una perspectiva empresarial.

Sin embargo, para contexto de hackathon, la arquitectura actual presenta un riesgo claro de **sobre-diseno operativo** si el equipo intenta implementar simultaneamente:

- frontend completo,
- backend robusto,
- microservicio ML desacoplado,
- persistencia historica,
- integracion OCI completa,
- observabilidad suficiente,
- y calidad de demo.

**Conclusión principal:**  
La arquitectura es buena como arquitectura objetivo, pero necesita una **reduccion tactica del alcance tecnico** para asegurar entrega funcional, demostrable y estable en 5 semanas.

## 2. Validacion solicitada

### 2.1 Coherencia arquitectonica

**Estado:** Aprobada con ajustes.

#### Hallazgos

- Existe una linea clara entre capa de experiencia, capa de negocio, capa analitica y capa de plataforma.
- La decision de usar Spring Boot como orquestador central es correcta.
- La separacion del servicio ML en Python es consistente con el stack previsto.
- La estrategia de almacenamiento de modelos y datasets en OCI Object Storage es adecuada.

#### Observaciones

- La arquitectura empresarial y la arquitectura MVP estan bien diferenciadas en el documento principal.
- El documento `architecture/02-Arquitectura-Propuesta.md` es demasiado basico para servir como artefacto de referencia y ademas presenta un cierre mal formado al final del flujo. Debe considerarse solo como boceto inicial, no como documento rector.
- El alcance funcional mezcla dos dominios de usuario: residencial y pequenos establecimientos. Para el MVP conviene elegir uno solo.

### 2.2 Riesgos de integracion

**Estado:** Medios a altos.

#### Riesgos principales

1. **Integracion Spring Boot -> Python ML**
   - Riesgo de contratos inestables.
   - Riesgo de latencia o timeout.
   - Riesgo de divergencia entre features usadas en entrenamiento y en inferencia.

2. **Integracion con OCI**
   - Riesgo de consumir tiempo excesivo en configuracion cloud.
   - Riesgo de credenciales, networking o despliegue tardio.

3. **Integracion frontend -> backend**
   - Riesgo moderado y controlable, siempre que el contrato se congele temprano.

#### Dictamen

El mayor riesgo de integracion no es React ni Spring Boot; es la combinacion de:

- datos reales o sinteticos,
- entrenamiento ML,
- empaquetado del modelo,
- inferencia Python,
- y despliegue cloud sincronizado.

### 2.3 Viabilidad en 5 semanas

**Estado:** Viable con recorte y disciplina fuerte de alcance.

#### Viable si se cumple

- Se congela el MVP en semana 1.
- Se consigue flujo vertical funcionando en semana 2.
- Se trabaja con un baseline ML temprano, no con un modelo "perfecto".
- OCI se valida por primera vez en semana 2, no al final.

#### No viable si se intenta

- multi-tenant real,
- autenticacion robusta completa,
- dashboard analitico avanzado,
- pipelines complejos de entrenamiento automatizado,
- o integraciones OCI de nivel enterprise completo.

### 2.4 Complejidad para un equipo de hackathon

**Estado:** Moderada-alta.

#### Evaluacion

El equipo tiene suficiente diversidad de roles para cubrir el stack, pero la complejidad aumenta por la necesidad de coordinar:

- Data Engineer
- Data Scientist
- Backend
- Frontend
- Arquitectura / integracion

El riesgo no es falta de roles; el riesgo es la **sincronizacion entre entregables interdependientes**.

### 2.5 Dependencias entre componentes

**Estado:** Claras, pero algunas son criticas.

#### Mapa de dependencias

1. Dataset limpio -> entrenamiento ML
2. Entrenamiento ML -> artefacto de modelo
3. Artefacto de modelo -> servicio Python operativo
4. Servicio Python operativo -> backend de clasificacion
5. Backend operativo -> frontend funcional
6. Backend y ML desplegados -> demo cloud estable

#### Dependencias criticas

- Sin dataset validado, el trabajo de ML se bloquea.
- Sin contrato backend-ML, backend y ciencia de datos trabajan a ciegas.
- Sin flujo end-to-end temprano, la semana 4 se convierte en integracion tardia.

### 2.6 Posibles cuellos de botella

**Estado:** Identificados.

#### Cuellos de botella probables

1. **Dataset**
   - calidad,
   - disponibilidad,
   - estructura insuficiente para clasificacion.

2. **Servicio ML**
   - serializacion del modelo,
   - consistencia de features,
   - manejo de errores.

3. **Arquitecto / integracion**
   - exceso de decisiones centralizadas puede frenar avance si no se congelan contratos pronto.

4. **OCI**
   - curva de configuracion superior a la esperada.

5. **Frontend**
   - riesgo de consumir demasiado tiempo en visuales no esenciales para la demo.

## 3. Observaciones criticas

### O-01. El MVP actual aun esta ligeramente sobredimensionado

La arquitectura documental plantea un MVP razonable, pero operativamente aun incluye demasiadas metas concurrentes: historico, recomendaciones, persistencia, OCI, trazabilidad, observabilidad y separacion completa de servicios.

### O-02. El mayor riesgo no es tecnico aislado; es de coordinacion

La complejidad real esta en sincronizar dataset, modelo, contrato de inferencia, backend y frontend en solo 5 semanas.

### O-03. OCI debe ser un habilitador, no el centro del proyecto

Si el equipo invierte demasiado esfuerzo en servicios OCI secundarios, puede sacrificar el valor visible del producto.

### O-04. Recomendaciones inteligentes dependen de un modelo explicable o reglas complementarias

La clasificacion sola no garantiza una demo fuerte. Las recomendaciones deben poder explicarse aunque el modelo sea simple.

### O-05. La persistencia historica no debe bloquear la primera demo funcional

Es valiosa, pero no es critica antes de tener clasificacion operativa en punta a punta.

## 4. Mejoras recomendadas

### MR-01. Reducir el dominio del MVP a un solo tipo de usuario

Recomendacion: enfocar el MVP en **usuario residencial**.  
Beneficio: simplifica variables, narrativa, dataset y recomendaciones.

### MR-02. Congelar un contrato minimo backend-ML en semana 1

Definir desde el inicio:

- payload de entrada,
- payload de salida,
- manejo de error,
- version del modelo,
- timestamp de inferencia.

### MR-03. Convertir recomendaciones en logica hibrida

Usar:

- clasificacion por modelo,
- recomendaciones por reglas de negocio parametrizadas.

Beneficio: mejora control, explicabilidad y estabilidad de la demo.

### MR-04. Desacoplar "arquitectura objetivo" de "arquitectura de entrega"

Mantener la arquitectura empresarial documentada, pero ejecutar una version de entrega con menos componentes criticos simultaneos.

### MR-05. Definir una ruta A y una ruta B para la demo

- **Ruta A:** inferencia real con modelo cargado.
- **Ruta B:** stub controlado con respuestas consistentes si falla el servicio ML.

## 5. Version optimizada para maximizar probabilidad de exito

## 5.1 Principio rector

La version optimizada debe priorizar:

- demostracion visible,
- estabilidad,
- explicabilidad,
- y bajo riesgo de integracion.

## 5.2 Arquitectura optimizada recomendada

### Opcion recomendada para hackathon

- **React SPA**
- **Spring Boot API**
- **Python ML service**
- **Una sola base de datos relacional**
- **OCI Object Storage**
- **Despliegue en una sola VM o entorno simplificado en OCI con Docker Compose**

### Justificacion

Se mantiene la separacion tecnologica, pero se reduce la complejidad operativa al evitar despliegues dispersos o infraestructura excesivamente fragmentada.

## 5.3 Ajustes tacticos

1. Frontend con una sola vista principal y un flujo de clasificacion.
2. Backend con maximo 3 endpoints clave:
   - `POST /classifications`
   - `GET /classifications/{id}`
   - `GET /health`
3. ML con un solo endpoint:
   - `POST /predict`
4. Recomendaciones generadas inicialmente por reglas mapeadas a la clase final.
5. Historico persistido solo para consultas basicas.

## 6. MVP minimo indispensable

El MVP minimo indispensable para competir con altas probabilidades debe ser:

1. Formulario web para capturar datos de consumo.
2. Clasificacion del usuario en:
   - Eficiente
   - Moderado
   - Ineficiente
3. Resultado visible en pantalla.
4. Recomendacion accionable asociada a la clasificacion.
5. Evidencia de despliegue o integracion en OCI.

### Lo que NO debe formar parte del MVP minimo indispensable

- autenticacion completa,
- analitica historica avanzada,
- roles y permisos,
- entrenamiento automatico recurrente,
- dashboard BI complejo,
- microservicios adicionales.

## 7. Funcionalidades opcionales para diferenciar el proyecto

Estas funcionalidades deben entrar solo si el MVP ya esta estable.

### F-01. Comparativo de consumo estimado

Mostrar al usuario como se posiciona frente a un rango de consumo esperado para su perfil.

### F-02. Recomendaciones personalizadas por habito

Ejemplos:

- consumo alto en horario pico,
- uso intensivo nocturno,
- potencial de ahorro por cambio de rutina.

### F-03. Explicacion de la clasificacion

Mostrar variables mas influyentes o un resumen tipo:

"Tu clasificacion fue Ineficiente principalmente por alto consumo promedio y fuerte concentracion en horarios pico".

### F-04. Simulador de mejora

Permitir modificar uno o dos parametros y recalcular una clasificacion potencial.

### F-05. Score visual de eficiencia

Complementar la clase con un score de 0 a 100 para mejorar impacto visual en la demo.

## 8. Recomendacion final de gestion del proyecto

### Semana 1

- Congelar dominio residencial.
- Aprobar dataset.
- Definir contrato backend-ML.
- Crear backlog cerrado del MVP.

### Semana 2

- Tener vertical slice funcionando aunque el modelo sea baseline.
- Validar despliegue inicial OCI.

### Semana 3

- Consolidar persistencia, recomendaciones y smoke test.

### Semana 4

- Mejorar UX y narrativa de demo.
- Incorporar una sola funcionalidad diferenciadora.

### Semana 5

- No agregar alcance.
- Solo estabilizar, ensayar demo y generar evidencias.

## 9. Conclusiones

EnergiAI tiene una base arquitectonica solida y competitiva. La clave para ganar probabilidad de exito no es agregar mas componentes, sino **reducir incertidumbre y aumentar la confiabilidad del flujo principal**.

La arquitectura objetivo actual debe mantenerse como vision. La implementacion del hackathon debe operar con una **arquitectura simplificada, trazable y muy demostrable**, donde el valor central sea:

**dato de consumo -> clasificacion -> recomendacion -> visualizacion clara -> despliegue OCI**
