# Estructura de Repositorio y Estrategia Git Flow

**Fecha:** 2026-07-13  
**Objetivo:** Definir una estructura de repositorio ejecutable para el equipo y una estrategia de ramas compatible con un hackathon de 5 semanas.

## 1. Estructura de repositorio recomendada

```text
EnergiAI-G9-Latam-Team15/
|-- frontend/
|   |-- src/
|   |-- public/
|   |-- tests/
|   `-- package.json
|-- backend/
|   |-- src/main/java/
|   |-- src/main/resources/
|   |-- src/test/java/
|   `-- pom.xml
|-- ml-service/
|   |-- app/
|   |-- models/
|   |-- notebooks/
|   |-- tests/
|   `-- requirements.txt
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- samples/
|-- infra/
|   |-- oci/
|   |-- docker/
|   `-- scripts/
|-- docs/
|-- architecture/
|-- diagrams/
|-- planning/
`-- .github/
    `-- workflows/
```

## 2. Criterios de estructuracion

- **`frontend/`** concentra la experiencia digital React.
- **`backend/`** concentra API, reglas de negocio y persistencia.
- **`ml-service/`** aísla entrenamiento e inferencia Python.
- **`data/`** separa insumos crudos, transformados y muestras para demo.
- **`infra/`** contiene IaC ligera, Docker y automatizaciones de despliegue.
- **Documentacion** se mantiene fuera del codigo para facilitar lectura ejecutiva.

## 3. Estrategia Git Flow adaptada al hackathon

El repositorio ya se encuentra inicializado y esta documentacion formaliza el modelo operativo vigente para el equipo.

### 3.1 Ramas principales

- **`main`**: codigo estable y demostrable.
- **`develop`**: integracion continua del trabajo del equipo.

### 3.2 Ramas de soporte

- **`feature/<dominio>-<nombre>`**
  - Ejemplo: `feature/backend-classification-api`
  - Uso: nuevas capacidades funcionales o tecnicas creadas desde `develop`.

### 3.3 Flujo oficial

```text
main
  ↑
develop
  ↑
feature/*
```

### 3.4 Reglas operativas

1. Todo desarrollo parte de `develop`.
2. Ninguna rama `feature/*` se fusiona sin:
   - build exitoso
   - smoke test funcional
   - revision minima por otro integrante
3. Toda rama `feature/*` vuelve primero a `develop`.
4. `main` solo recibe merges validados desde `develop`.
5. Cada merge debe referenciar issue, tarea o decision tecnica.

## 4. Convencion de commits

Formato recomendado:

```text
<tipo>(<modulo>): <descripcion corta>
```

Ejemplos:

```text
feat(frontend): agrega dashboard de clasificacion
feat(backend): expone endpoint de scoring
feat(ml): incorpora baseline random forest
docs(architecture): agrega c4 nivel 2
fix(infra): corrige variable de entorno OCI
```

## 5. Politica minima de pull requests

- PR pequeno y enfocado.
- Evidencia de prueba incluida.
- Impacto arquitectonico descrito.
- Cambios de contrato API explicitados.
- Riesgos o deuda tecnica registrados.

## 6. Recomendaciones operativas vigentes

1. Mantener `main` como linea base estable del proyecto.
2. Usar `develop` como rama de integracion continua.
3. Crear ramas `feature/*` desde `develop` para cada cambio trazable.
4. Configurar proteccion basica sobre `main`.
5. Activar workflow CI para frontend, backend y ML.
6. Crear tablero Kanban enlazado a ramas y PRs.
