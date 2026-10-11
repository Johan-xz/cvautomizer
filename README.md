# CVAutomizer

Herramienta en Python para **automatizar la adaptación de un CV a cada oferta de trabajo**, reduciendo el tiempo que toma personalizar el currículum manualmente antes de cada aplicación.

## Problema que resuelve

Postular a varias vacantes suele implicar reescribir o ajustar el CV una y otra vez: reordenar experiencia, resaltar habilidades relevantes y adaptar el lenguaje a cada oferta. Ese proceso manual consume tiempo y es fácil de posponer o hacer de forma inconsistente.

CVAutomizer automatiza ese ajuste: a partir de un perfil base con toda la información del candidato, genera un CV en PDF adaptado a la oferta de trabajo específica, sin tener que editar el documento a mano en cada aplicación.

## Cómo funciona (flujo general)

1. **Datos base del candidato** (`data/`): la experiencia, educación, habilidades y demás información se mantienen en archivos estructurados (JSON/YAML), en un solo lugar, en vez de en múltiples versiones de CV.
2. **Procesamiento** (`src/`): el proyecto toma esos datos junto con la información de la oferta de trabajo y genera un CV adaptado, priorizando y ajustando el contenido según lo relevante para esa vacante.
3. **Resultado** (`output/`): el CV final se genera en formato PDF, listo para enviar.

## Estructura del proyecto

```
cvautomizer/
├── data/         # Perfil/datos base del candidato (JSON/YAML)
├── src/          # Código fuente del proceso de generación/adaptación del CV
├── output/       # CVs en PDF generados por la herramienta
└── dockerfile    # Definición de imagen Docker para ejecutar el proyecto
```

## Beneficio principal

Pasar de editar un CV a mano por cada postulación a mantener **una sola fuente de datos** y generar automáticamente una versión adaptada por oferta, reduciendo tiempo y errores en el proceso de aplicación a empleos.

## Estado del proyecto

En desarrollo inicial: se está definiendo la estructura base (`data/`, `src/`, `output/`, `dockerfile`) sobre la que se implementará el flujo de generación de CVs.
