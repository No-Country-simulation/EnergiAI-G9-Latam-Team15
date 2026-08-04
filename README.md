# EnergiAI-G9-Latam-Team15

Repositorio oficial del proyecto **EnergiAI** para el Hackathon Oracle + Alura + NoCountry.

EnergiAI es una solucion orientada al analisis de patrones de consumo energetico para clasificar usuarios en:

- `Eficiente`
- `Moderado`
- `Ineficiente`

La plataforma combina:

- **React** para la experiencia web
- **Spring Boot** para la API y la orquestacion del negocio
- **Python Scikit-Learn** para inferencia de modelos
- **Oracle Cloud Infrastructure (OCI)** para despliegue, almacenamiento y soporte operativo

## Tabla de Contenidos

- [Vision General](#vision-general)
- [Objetivo del Hackathon](#objetivo-del-hackathon)
- [Arquitectura](#arquitectura)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Roadmap](#roadmap)
- [Git Flow](#git-flow)
- [OCI](#oci)
- [Documentacion](#documentacion)
- [Equipo](#equipo)
- [Como Contribuir](#como-contribuir)
- [Licencia](#licencia)

## Vision General

EnergiAI transforma datos de consumo electrico en informacion accionable para apoyar decisiones de ahorro y sostenibilidad.

### Propuesta de valor

- clasificacion automatica del perfil energetico,
- recomendaciones claras y accionables,
- visualizacion simple para demo y adopcion,
- arquitectura desacoplada y evolutiva,
- integracion cloud pragmatica sobre OCI.

## Objetivo del Hackathon

Construir un MVP demostrable, estable y defendible que entregue el flujo:

`dato de consumo -> clasificacion -> recomendacion -> visualizacion -> evidencia OCI`

El foco del MVP se encuentra en **usuario residencial**, priorizando claridad funcional y bajo riesgo de integracion.

## Arquitectura

La arquitectura del proyecto esta documentada en detalle en los siguientes artefactos:

- [Vision General](architecture/01-Vision-General.md)
- [Arquitectura Inicial](architecture/02-Arquitectura-Propuesta.md)
- [Arquitectura Empresarial y MVP](architecture/03-Arquitectura-Empresarial-EnergiAI.md)
- [C4 Nivel 1 - Contexto](diagrams/01-C4-Nivel-1-Contexto.md)
- [C4 Nivel 2 - Contenedores](diagrams/02-C4-Nivel-2-Contenedores.md)
- [Revision Arquitectonica y Version Optimizada](docs/02-Revision-Arquitectonica-y-Version-Optimizada.md)
- [Guia Maestra del Proyecto](docs/03-Guia-Maestra-Proyecto-EnergiAI.md)

### Stack principal

| Capa | Tecnologia | Responsabilidad |
|---|---|---|
| Frontend | React | experiencia web y visualizacion |
| Backend | Spring Boot | API, reglas de negocio e integracion |
| ML | Python + Scikit-Learn | inferencia de clasificacion |
| Datos | Base relacional + Object Storage | persistencia y artefactos |
| Cloud | OCI | despliegue, almacenamiento, observabilidad |

## Estructura del Repositorio

```text
EnergiAI-G9-Latam-Team15/
|-- .github/
|-- assets/
|   |-- branding/
|   |-- diagrams/
|   |-- presentations/
|   `-- screenshots/
|-- architecture/
|-- backend/
|   `-- src/
|       |-- main/
|       |   |-- java/
|       |   `-- resources/
|       `-- test/
|           `-- java/
|-- data/
|   |-- processed/
|   |-- raw/
|   `-- samples/
|-- diagrams/
|-- docs/
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- components/
|   |   |-- pages/
|   |   |-- services/
|   |   `-- styles/
|   `-- tests/
|-- infra/
|   |-- docker/
|   |-- oci/
|   `-- scripts/
|-- meetings/
|   `-- ActaReunion-001-ENERGIAI.md
|-- ml-service/
|   |-- app/
|   |-- models/
|   |-- notebooks/
|   `-- tests/
|-- planning/
|-- .gitignore
|-- CODE_OF_CONDUCT.md
|-- CONTRIBUTING.md
|-- LICENSE
`-- README.md
```

### Organizacion de assets

| Carpeta | Uso |
|---|---|
| `assets/branding/` | logos, identidad visual, piezas de marca |
| `assets/diagrams/` | exportaciones visuales de arquitectura y flujos |
| `assets/screenshots/` | capturas para README, demo y evidencias |
| `assets/presentations/` | materiales de pitch, presentaciones y anexos |

## Roadmap

| Semana | Objetivo principal | Resultado esperado |
|---|---|---|
| Sprint 0 | alineacion y setup | alcance, roles, dataset preliminar, estructura |
| Sprint 1 | contratos y skeletons | frontend, backend y ML base |
| Sprint 2 | vertical slice | flujo end-to-end operativo |
| Sprint 3 | consolidacion | baseline ML, persistencia y recomendaciones |
| Sprint 4 | calidad y diferenciacion | UX, smoke tests, funcionalidad diferencial |
| Sprint 5 | estabilizacion | demo final, evidencias, cierre documental |

Documentos relacionados:

- [Roadmap Tecnico de 5 Semanas](planning/03-Roadmap-Tecnico-5-Semanas.md)
- [Guia Maestra del Proyecto](docs/03-Guia-Maestra-Proyecto-EnergiAI.md)

## Git Flow

Estrategia de ramas adoptada:

- `main`: linea base estable y oficial del proyecto
- `develop`: rama de integracion continua previa a promotion a `main`
- `feature/<dominio>-<nombre>`: nuevas capacidades creadas desde `develop`

Flujo oficial:

```text
main
  ↑
develop
  ↑
feature/*
```

Reglas operativas:

1. Toda nueva capacidad nace desde `develop` en una rama `feature/*`.
2. Todo Pull Request funcional o tecnico se integra primero en `develop`.
3. `main` recibe unicamente integraciones validadas desde `develop` para consolidar lineas base estables.

Convencion de commits:

```text
feat(frontend): agrega formulario de clasificacion
feat(backend): implementa endpoint /classifications
feat(ml): publica baseline random forest
docs(pmo): actualiza guia maestra
fix(infra): corrige variables OCI
```

Referencia:

- [Estructura de Repositorio y Git Flow](docs/01-Estructura-Repositorio-y-GitFlow.md)

## OCI

OCI se utiliza como habilitador pragmatica del MVP, priorizando:

- despliegue temprano,
- almacenamiento de datasets y modelos,
- evidencia real de integracion cloud,
- soporte a la demo final.

Servicios OCI recomendados:

- **OCI Compute** o **Container Instances**
- **OCI Object Storage**
- **OCI Logging**
- **OCI Monitoring**
- **OCI Vault** si el tiempo del hackathon lo permite

Referencia:

- [Arquitectura Empresarial y MVP](architecture/03-Arquitectura-Empresarial-EnergiAI.md)
- [Guia Maestra del Proyecto](docs/03-Guia-Maestra-Proyecto-EnergiAI.md)

## Documentacion

La documentacion principal del proyecto se encuentra organizada en:

- `architecture/` para arquitectura objetivo y MVP
- `diagrams/` para diagramas C4 y representacion visual
- `docs/` para documentacion ejecutiva, PMO y gobierno
- `planning/` para roles, riesgos y roadmap

Indice recomendado:

- [Indice Maestro de Documentacion](docs/00-Indice-Arquitectura.md)
- [Guia Maestra del Proyecto EnergiAI](docs/03-Guia-Maestra-Proyecto-EnergiAI.md)
- [Gestion de Riesgos Arquitectonicos](planning/04-Gestion-de-Riesgos-Arquitectonicos.md)

## Equipo

| Integrante | Rol oficial inicial |
|---|---|
| Luis Angel Chavez Mejia | Product Owner |
| Bernardo Gomez | Software Architect |
| Harrinson Villabona | Data Scientist |
| Anayely Reyes | Data Engineer |
| Carlos Fabian Mesa | Backend Developer |
| Elvis Trinidad | Backend Developer |
| Magno Cristian | Data Analyst |
| Alonso Carbajal | Full Stack Developer |

Referencia:

- [Roles del Equipo](planning/01-Roles.md)

## Como Contribuir

Antes de abrir cambios:

1. Lee [CONTRIBUTING.md](CONTRIBUTING.md).
2. Revisa el [Codigo de Conducta](CODE_OF_CONDUCT.md).
3. Verifica si el cambio impacta arquitectura, backlog o documentacion.
4. Mantiene los cambios pequenos, trazables y revisables.

## Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).
