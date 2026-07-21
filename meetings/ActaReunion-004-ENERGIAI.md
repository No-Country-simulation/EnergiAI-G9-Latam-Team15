# ACTA DE REUNIÓN 004 – ENERGIAI

## Fecha

21 de julio de 2026

## Hora

11:00 a.m. (Colombia / Perú)

## Medio

Canal de voz Discord – Reunión de Seguimiento Sprint 1

---

# Objetivo de la Reunión

Realizar seguimiento técnico y organizacional del Sprint 1, validar avances de arquitectura, gestión documental, estrategia de datos y definir acciones para continuar el desarrollo del MVP EnergiAI.

---

# Asistentes

- Bernardo Adolfo Gómez Montoya – Software / Solution Architect
- Elvis Leniker Trinidad Caldas – Backend Developer
- Carlos Fabián Mesa Muñoz – Backend Developer
- Magno Cristian Coronel Salazar – Data Analyst

---

# Ausentes

- Luis Angel Chavez Mejía – Product Owner
- Harrinson Villabona – Data Scientist
- Alonso Carbajal – Full Stack Developer
- Anayely Reyes – Data Engineer

---

# Objetivos Revisados

✅ Estado general del Sprint 1

✅ Gestión documental del proyecto

✅ Situación actual de Data Engineering

✅ Contrato de Integración JSON v1

✅ Organización mediante GitFlow

✅ Identificación de fuentes de datos energéticos

---

# Temas Tratados

1. Revisión del avance general del proyecto.
2. Implementación del repositorio documental compartido en Google Drive.
3. Estado del rol Data Engineer.
4. Investigación preliminar de datasets para EnergiAI.
5. Formalización del Contrato de Integración JSON v1.
6. Validación de ramas y gobernanza Git.
7. Próximas actividades para Data Engineering y Data Science.

---

# Avances Logrados

## Gestión Documental

✅ Creación del espacio documental colaborativo del equipo.

Nombre:

```text
EnergiAI_Project_Repository
```

Objetivo:

- Centralizar documentación.
- Almacenar actas.
- Gestionar datasets.
- Consolidar arquitectura.
- Organizar evidencias.
- Mantener investigación técnica.

### Estado de Accesos

Accesos habilitados:

- Bernardo Adolfo Gómez Montoya
- Alonso Carbajal
- Elvis Leniker Trinidad Caldas
- Carlos Fabián Mesa Muñoz
- Magno Cristian Coronel Salazar

Pendientes por compartir correo Gmail:

- Luis Angel Chavez Mejía
- Harrinson Villabona
- Anayely Reyes

---

## Arquitectura

✅ Formalización del Contrato de Integración JSON v1.

Documento:

```text
architecture/contracts/API_CONTRACT_V1.md
```

Rama:

```text
feature/architect-contrato-integracion-v0.1
```

Contenido:

- Endpoint principal del MVP.
- Request JSON.
- Response JSON.
- Manejo de errores.
- Flujo Frontend → Backend → ML Service.
- Alcance funcional del MVP.

---

## Data Engineering

Debido a la ausencia temporal del rol Data Engineer se ejecutó una actividad de mitigación desde Arquitectura para evitar bloqueos en el Sprint 1.

### Actividades realizadas

✅ Investigación inicial de fuentes de datos energéticos.

Fuentes identificadas:

- XM Colombia
- SIMEM Colombia
- OSINERGMIN Perú
- INEI Perú
- UCI Household Energy Dataset

### Documentos elaborados

```text
Dataset_Research_Report_v1.md
Dataset_Strategy_v1.md
```

### Rama creada

```text
feature/data-engineering-bootstrap-v1
```

Estado:

La documentación quedó publicada en GitHub para revisión y continuidad por parte de los responsables técnicos.

---

## Gestión de Configuración

✅ Aplicación del flujo GitFlow definido por el equipo.

✅ Separación de responsabilidades mediante ramas independientes.

✅ Publicación y versionado de entregables técnicos en GitHub.

---

# Riesgos Identificados

## Riesgo 01

**Ausencia temporal del rol Data Engineer.**

Impacto:

Alto.

Mitigación:

- Investigación preliminar de datasets.
- Estrategia inicial documentada.
- Apoyo temporal desde Arquitectura y Backend.

---

## Riesgo 02

**Dependencia del Dataset Maestro para iniciar actividades de Data Science y Machine Learning.**

Impacto:

Alto.

Mitigación:

- Evaluación de datasets reales.
- Selección de fuente principal.
- Construcción progresiva del Dataset Maestro v1.

---

# Acuerdos

✅ Mantener Google Drive como repositorio documental colaborativo.

✅ Mantener GitHub como repositorio oficial para código fuente y documentación técnica versionada.

✅ Revisar y validar el documento:

```text
API_CONTRACT_V1.md
```

✅ Continuar con la evaluación de datasets energéticos identificados.

✅ Solicitar los correos Gmail pendientes para habilitar accesos al Drive.

✅ Definir responsable operativo para la consolidación del Dataset Maestro EnergiAI.

---

# Compromisos

| Responsable | Actividad |
|------------|------------|
| Bernardo Gómez Montoya | Administrar repositorio documental compartido |
| Bernardo Gómez Montoya | Coordinar validación del API Contract v1 |
| Elvis Trinidad | Apoyar evaluación técnica de datasets |
| Carlos Fabián Mesa | Apoyar revisión técnica de integración |
| Equipo Técnico | Revisar y validar documentación publicada |
| Integrantes pendientes | Compartir correo Gmail para habilitar acceso al Drive |

---

# Próximos Pasos

1. Obtener los correos Gmail faltantes.
2. Validar el API Contract v1.
3. Seleccionar Dataset Base.
4. Construir Dataset Maestro v1.
5. Iniciar EDA (Exploratory Data Analysis).
6. Iniciar entrenamiento del modelo ML.
7. Continuar integración Backend, Frontend y ML Service.

---

# Estado General del Sprint 1

✅ Repositorio Documental Implementado

✅ Contrato de Integración JSON v1 Formalizado

✅ Investigación Inicial de Datasets Completada

✅ Gobernanza Git Implementada

✅ Ramas Técnicas Publicadas

🟡 Dataset Maestro Pendiente

🟡 Entrenamiento Modelo ML Pendiente

🟡 Integración Técnica Completa Pendiente

---

# Conclusión

Durante la reunión se confirmó la consolidación de la base documental del proyecto, la formalización del contrato de integración JSON y la mitigación inicial del riesgo asociado al rol Data Engineer.

El proyecto continúa avanzando conforme a la planificación del Sprint 1, quedando como prioridad inmediata la selección y construcción del Dataset Maestro EnergiAI para habilitar las actividades de Data Science y Machine Learning.