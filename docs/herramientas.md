# Herramientas

Stack tecnológico del proyecto, con la versión usada y el papel que cumple cada herramienta.

## Entorno de trabajo

| Herramienta | Versión | Uso | Estado |
|---|---|---|---|
| Pop!_OS | Ubuntu 24 (base) | Sistema operativo del equipo de desarrollo | En uso |
| Git | Por confirmar (`git --version`) | Control de versiones | En uso |
| GitHub | Repositorio `Johan-xz/cvautomizer` | Repositorio remoto | En uso |
| Docker | Por confirmar (`docker --version`) | Entorno aislado de ejecución | En uso |

## Lenguaje y gestor de paquetes

| Herramienta | Versión | Uso | Estado |
|---|---|---|---|
| Python | 3.11.16 (imagen `python:3.11-slim`) | Lenguaje principal | En uso |
| uv | 0.13.0 | Instalación de dependencias dentro de la imagen | En uso |

## Dependencias del proyecto

Las versiones de producción están fijadas en `requirements.txt`.

| Librería | Versión | Uso | Estado |
|---|---|---|---|
| pyyaml | 6.0.1 | Leer `data/candidate.yaml` | En uso |
| pydantic | 2.5.0 | Modelos y validación de datos | En uso |
| reportlab | 4.0.9 | Generación del PDF | En uso (generador en desarrollo) |
| jinja2 | 3.1.2 | Plantillas de texto | Instalada, sin uso todavía |

Las herramientas de desarrollo están en `requirements-dev.txt`.

| Librería | Versión | Uso | Estado |
|---|---|---|---|
| pytest | Sin fijar | Ejecutar pruebas | En uso |
| pypdf | Sin fijar | Leer el PDF generado y verificar su texto | En uso |

## Pendientes de este documento

- **Fijar versiones de pytest y pypdf** en `requirements-dev.txt`. Sin versión fija, dos builds pueden instalar librerías distintas.
- **Decidir sobre jinja2**: usarla para algún fin concreto, como una vista previa en HTML, o quitarla de `requirements.txt`.
- **Registrar las versiones de Git y Docker** con sus comandos de verificación, porque cambian con las actualizaciones del sistema.

## Cómo verificar el entorno

Dentro del contenedor, desde la carpeta del proyecto:

```bash
python --version
uv --version
python -c "import pydantic, yaml, reportlab, pytest, pypdf; print('ok')"
```

En el equipo de desarrollo:

```bash
git --version
docker --version
```
