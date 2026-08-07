# docs/architecture/

Auditorías técnicas y evaluaciones de estado de los componentes de arquitectura de EnergiAI.

## Diferencia con `architecture/` (raíz del repositorio)

- `architecture/` (raíz) contiene la **especificación** de la arquitectura: visión, arquitectura propuesta, arquitectura empresarial, decisiones arquitectónicas (DA-01 a DA-05) y el contrato de integración vigente. Es normativo y de lectura obligatoria (ver `docs/00-Indice-Arquitectura.md`).
- `docs/architecture/` (esta carpeta) contiene **auditorías** que evalúan qué tan implementada está esa especificación en un momento dado. Es diagnóstico, no normativo, y se espera que quede desactualizado con el avance del proyecto — cada auditoría lleva fecha y debe releerse contra el estado real del código antes de tomar decisiones a partir de ella.

## Contenido

- `AUDITORIA_BACKEND.md` — estado real del módulo `backend/` frente al contrato de integración.
- `AUDITORIA_ML.md` — estado real del módulo `ml-service/` frente a la arquitectura declarada.
- `MOTOR_RECOMENDACIONES_v1.md` — auditoría y especificación del motor de reglas de recomendaciones actualmente implementado en el frontend.
