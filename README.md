# CVAutomizer: documentación

Herramienta en Python que genera un CV en PDF adaptado a cada oferta de trabajo, con formato Harvard y pensado para sistemas ATS.

Estos documentos explican **qué decisiones se tomaron, con qué herramientas se trabaja y en qué fase está el proyecto**.

## Índice

- [decisiones.md](/docs/decisiones.md): registro de decisiones de arquitectura (ADR), con su contexto y consecuencias.
- [herramientas.md](/docs/herramientas.md): stack tecnológico, versiones y uso de cada herramienta.
- [fases.md](/docs/fases.md): fases del proyecto, estado actual y trabajo futuro.

## Estado actual

Actualizado: 2026-10-13.

- Entorno: contenedor Docker `cvautomizer` creado desde la imagen `cvautomizer:1.0`, con el proyecto montado.
- Control de versiones: repositorio en GitHub sincronizado con la copia local.
- Datos: modelo `Candidate` unificado con `data/candidate.yaml`, con validación de fechas en formato `YYYY-MM`.
- Generación de PDF: en desarrollo. El generador todavía usa atributos del modelo anterior.

## Cómo mantener esta documentación

- Cada decisión importante se agrega como un ADR nuevo en `decisiones.md`, con el siguiente número disponible. No se borran decisiones anteriores: si cambian, se marca la anterior como reemplazada y se enlaza la nueva.
- Al cerrar una fase, se actualiza su estado en `fases.md`.
- Si cambia una versión en `requirements.txt`, se actualiza la tabla de `herramientas.md`.
