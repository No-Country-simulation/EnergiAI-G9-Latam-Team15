# Contribuir a EnergiAI

Gracias por contribuir a **EnergiAI-G9-Latam-Team15**.

Este repositorio sigue una disciplina de contribucion orientada a hackathon, pero con estandares de mantenimiento compatibles con un proyecto serio y escalable.

## Tabla de Contenidos

- [Principios](#principios)
- [Flujo de trabajo](#flujo-de-trabajo)
- [Estrategia de ramas](#estrategia-de-ramas)
- [Convencion de commits](#convencion-de-commits)
- [Pull Requests](#pull-requests)
- [Reglas de documentacion](#reglas-de-documentacion)
- [Reglas de calidad minima](#reglas-de-calidad-minima)

## Principios

- cambios pequenos y enfocados,
- trazabilidad tecnica y funcional,
- documentacion actualizada si cambia arquitectura, backlog o alcance,
- colaboracion respetuosa y revisiones claras,
- proteccion del MVP por encima de ideas no priorizadas.

## Flujo de trabajo

1. Revisa el backlog y valida que el trabajo tenga owner.
2. Crea una rama desde `develop`.
3. Implementa el cambio en un alcance pequeno.
4. Actualiza documentacion si el cambio modifica arquitectura, roadmap, riesgos o contratos.
5. Ejecuta validaciones minimas del modulo afectado.
6. Abre un Pull Request con evidencia suficiente.

## Estrategia de ramas

Ramas admitidas:

- `main`
- `develop`
- `feature/<dominio>-<nombre>`
- `release/<version>`
- `hotfix/<nombre>`

Ejemplos:

```text
feature/frontend-dashboard-clasificacion
feature/backend-endpoint-classifications
feature/ml-baseline-random-forest
hotfix/timeout-ml-service
```

## Convencion de commits

Formato:

```text
<tipo>(<modulo>): <descripcion corta>
```

Ejemplos:

```text
feat(frontend): agrega vista de resultado energetico
feat(backend): expone endpoint de clasificacion
feat(ml): agrega baseline para inferencia
docs(architecture): actualiza c4 nivel 2
fix(infra): corrige variable de despliegue oci
```

Tipos sugeridos:

- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`

## Pull Requests

Todo Pull Request debe incluir:

- objetivo del cambio,
- alcance funcional o tecnico,
- evidencia de prueba,
- impacto en arquitectura o contratos,
- riesgos o deuda conocida.

### Checklist minimo

- [ ] El cambio compila o es verificable
- [ ] El cambio no rompe contratos existentes
- [ ] La documentacion afectada fue actualizada
- [ ] El PR tiene descripcion clara
- [ ] El cambio mantiene foco en el MVP o backlog aprobado

## Reglas de documentacion

Debe actualizarse documentacion cuando el cambio afecte:

- arquitectura,
- integracion backend-ML,
- backlog oficial,
- roadmap,
- riesgos,
- roles o dependencias,
- estrategia OCI.

Documentos rectores:

- `docs/03-Guia-Maestra-Proyecto-EnergiAI.md`
- `architecture/03-Arquitectura-Empresarial-EnergiAI.md`
- `docs/01-Estructura-Repositorio-y-GitFlow.md`

## Reglas de calidad minima

### Frontend

- componentes pequenos y con responsabilidad clara,
- separacion entre UI y acceso a servicios,
- manejo basico de estados de carga y error.

### Backend

- contratos REST claros,
- validacion de payloads,
- logs basicos,
- endpoint de salud cuando aplique.

### ML

- separacion entre entrenamiento e inferencia,
- versionado del modelo,
- consistencia entre features de entrenamiento e inferencia.

### Infra / OCI

- no exponer secretos,
- parametrizar variables de entorno,
- documentar pasos de despliegue.

## Regla final

Si un cambio mejora una parte del sistema pero aumenta el riesgo de la demo final, debe replantearse antes de mergear.
