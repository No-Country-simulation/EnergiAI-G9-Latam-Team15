# Diagrama de Secuencia — POST /api/v1/analisis-energetico

**Fecha:** 2026-08-05
**Objetivo:** Documentar el flujo real end-to-end verificado en la demo del 2026-08-04 (`meetings/ActaReunion-008-ENERGIAI.md`), incluyendo el camino de fallo. Cierra el gap señalado en `docs/governance/AUDITORIA_PROYECTO_v1.md` §3.1.

## Camino feliz

```mermaid
sequenceDiagram
    actor U as Usuario
    participant FE as Frontend (React)
    participant BE as Backend (AnalisisEnergeticoController)
    participant SVC as AnalisisEnergeticoService
    participant ML as ML Service (FastAPI /predict)

    U->>FE: Completa FormularioConsumo
    FE->>BE: POST /api/v1/analisis-energetico
    BE->>BE: Valida AnalisisRequestDTO (Bean Validation)
    BE->>SVC: procesarAnalisis(request)
    SVC->>SVC: costoEstimado = consumo_kwh x 0.75
    SVC->>ML: POST /predict (mismas 5 features)
    ML-->>SVC: { categoria, probabilidad }
    SVC->>SVC: arma AnalisisResponseDTO (+ 3 recomendaciones fijas, ver ADR-002)
    SVC-->>BE: AnalisisResponseDTO
    BE-->>FE: 200 OK + JSON
    FE-->>U: SemaforoEficiencia + TarjetaCosto + ListaRecomendaciones
```

## Camino de fallo — ML Service no disponible

```mermaid
sequenceDiagram
    actor U as Usuario
    participant FE as Frontend (React)
    participant BE as Backend (AnalisisEnergeticoController)
    participant SVC as AnalisisEnergeticoService
    participant ML as ML Service

    U->>FE: Completa FormularioConsumo
    FE->>BE: POST /api/v1/analisis-energetico
    BE->>SVC: procesarAnalisis(request)
    SVC->>ML: POST /predict
    ML--xSVC: timeout / error de red
    SVC->>SVC: catch: categoria="Ineficiente", probabilidad=0.81 (fallback fijo)
    SVC-->>BE: AnalisisResponseDTO (con valores de contingencia)
    BE-->>FE: 200 OK (¡no hay señal de error!)
    FE-->>U: Resultado mostrado como normal
```

**Nota de riesgo (ver `architecture/contracts/CONTRATO_INTERNO_BACKEND_ML.md`):** el fallback del backend responde `200 OK` incluso cuando el ML Service falló — el usuario no tiene forma de distinguir una predicción real de una de contingencia. Es una decisión deliberada de resiliencia de demo, pero debe quedar explícita para quien opere el sistema en producción.

## Camino de validación fallida (400)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant FE as Frontend (React)
    participant BE as Backend (AnalisisEnergeticoController)

    U->>FE: Envía formulario con consumo_kwh vacío
    FE->>BE: POST /api/v1/analisis-energetico
    BE->>BE: Bean Validation falla (@NotNull en consumoKwh)
    BE-->>FE: 400 Bad Request
```

## Documentos relacionados

- `diagrams/03-C4-Nivel-3-Componentes.md`
- `architecture/contracts/API_CONTRACT_V1.md`
- `architecture/contracts/CONTRATO_INTERNO_BACKEND_ML.md`
