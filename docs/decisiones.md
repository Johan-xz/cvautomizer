# Registro de decisiones de arquitectura

Cada decisión sigue el formato: **Contexto**, **Decisión** y **Consecuencias**. Si una decisión cambia, se marca como reemplazada y se enlaza la nueva.

---

## ADR-001: Python 3.11 como lenguaje base

**Estado:** aceptada

**Contexto:** el proyecto necesita parsear YAML, validar datos y generar PDF. Las librerías elegidas (pydantic, reportlab, pytest) son compatibles con Python 3.11.

**Decisión:** usar Python 3.11 en la imagen base `python:3.11-slim`.

**Consecuencias:**
- La versión del intérprete es la misma en desarrollo y en la imagen.
- Se pueden usar anotaciones modernas como `str | None`.
- Cambiar de versión requiere reconstruir la imagen y revisar compatibilidad de dependencias.

---

## ADR-002: Docker para el entorno de desarrollo

**Estado:** aceptada

**Contexto:** el proyecto se desarrolla en Pop!_OS, y las dependencias del sistema (como `gcc`) y de Python deben ser las mismas en cualquier equipo.

**Decisión:** construir una imagen con todas las dependencias fijadas en `requirements.txt`. El código no va dentro de la imagen para desarrollo: la carpeta del proyecto se monta en `/app`.

**Consecuencias:**
- Editar código o pruebas no requiere reconstruir la imagen.
- Cambiar una dependencia sí requiere reconstruir.
- Un contenedor nuevo no conserva lo que se instaló a mano dentro de él. Las dependencias deben ir siempre en los archivos de requisitos.

---

## ADR-003: uv como instalador de dependencias

**Estado:** aceptada

**Contexto:** se necesita una forma rápida y reproducible de instalar dependencias dentro de la imagen.

**Decisión:** instalar uv con el script oficial y usar `uv pip install --system -r requirements.txt` durante el build.

**Consecuencias:**
- La instalación es rápida y el resultado es el mismo en cada build, porque las versiones están fijadas.
- El build necesita `curl` para descargar uv, y depende de que el servicio de instalación esté disponible.
- Si se quiere reducir dependencias de build, se puede copiar el binario de uv desde su imagen oficial en lugar de instalarlo con `curl`. No se ha evaluado todavía.

---

## ADR-004: reportlab para generar el PDF

**Estado:** aceptada

**Contexto:** el CV debe tener un diseño fijo (formato Harvard) y el texto debe poder extraerse del PDF, porque es lo que lee un sistema ATS.

**Decisión:** usar reportlab, que dibuja el documento directamente, sin pasar por un navegador ni por HTML.

**Consecuencias:**
- El control de fuentes, márgenes y posición del texto es directo.
- El texto queda seleccionable y extraíble, lo que permite verificarlo con pypdf (ver ADR-009).
- Hay que escapar los caracteres especiales (`&`, `<`, `>`) antes de pasarlos a `Paragraph`, porque reportlab interpreta algunos como markup. Pendiente de implementar.
- Alternativas de conversión de HTML a PDF no se han evaluado formalmente. Si el diseño crece mucho, conviene revisarlo.

---

## ADR-005: YAML como única fuente de datos del candidato

**Estado:** aceptada

**Contexto:** mantener varias versiones del CV es lo que el proyecto quiere evitar. Los datos del candidato deben estar en un solo lugar.

**Decisión:**
- `data/candidate.yaml` contiene los datos reales del candidato y **no** se versiona (está en `.gitignore`).
- `data/candidate.example.yaml` es una plantilla sin datos personales y sí se versiona.

**Consecuencias:**
- El repositorio es público sin exponer teléfono, correo ni código postal.
- Cada persona que clone el proyecto copia la plantilla y agrega sus propios datos.
- Si el YAML real se subió al historial en algún momento, sigue ahí aunque ya no esté rastreado. Hasta ahora el historial solo contiene el ejemplo.

---

## ADR-006: Validación con pydantic y fechas en formato YYYY-MM

**Estado:** aceptada

**Contexto:** un dato mal escrito en el YAML (por ejemplo, `2025/09`) debe detectarse antes de generar el PDF y no durante la generación.

**Decisión:**
- Los modelos se definen con pydantic en `src/models/candidate.py`.
- Las fechas se guardan como texto y se validan con una expresión regular que acepta `YYYY-MM` o `YYYY-MM-DD`.
- Una experiencia no puede terminar antes de empezar. La comparación se hace solo por año y mes.
- Para el PDF, las fechas se convierten a "Mes Año" en inglés (por ejemplo, "Sep 2025") con `formatear_mes`.

**Consecuencias:**
- Los errores aparecen al cargar el YAML, con el nombre del campo y el valor incorrecto.
- Las fechas siguen siendo texto en el modelo, lo que permite ordenarlas y validarlas sin depender de un tipo `date` que no acepta fechas parciales.
- Si se agrega otro idioma para el PDF, solo cambia `MESES` en `src/utils/dates.py`.

---

## ADR-007: Formato Harvard de una columna con encabezados estándar

**Estado:** aceptada, con cambios pendientes

**Contexto:** los sistemas ATS leen mejor los documentos de una sola columna, sin tablas ni cuadros de texto, y con encabezados reconocibles.

**Decisión:**
- Una sola columna, sin tablas ni imágenes.
- Encabezados estándar: PROFESSIONAL SUMMARY, EXPERIENCE, EDUCATION, SKILLS, LANGUAGES, INTERESTS.
- Experiencias y educación en orden cronológico inverso.
- Para egresados recientes, EDUCATION va antes de EXPERIENCE. **Pendiente**: el generador actual todavía pone EXPERIENCE primero.
- Un solo PDF por oferta, con tamaño de página carta.

**Consecuencias:**
- Los parsers de ATS extraen el texto en el orden correcto.
- El diseño es sobrio y tiene menos control visual que un CV con columnas. Es una decisión intencional.
- Falta decidir si "LEADERSHIP & ACTIVITIES" debe llamarse "LEADERSHIP AND ACTIVITIES", porque el símbolo `&` puede cortar algunas lecturas.

---

## ADR-008: Arquitectura por capas tipo MVC

**Estado:** aceptada, implementación parcial

**Contexto:** el proyecto tiene lectura de datos, análisis de la oferta, cálculo de match y generación de salida. Mezclar estas tareas en un solo script dificulta probarlas.

**Decisión:** separar el código en capas:

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| Modelos | `src/models/` | Estructura de datos con pydantic |
| Parsers | `src/parsers/` | Leer YAML o JSON y convertirlo a modelos |
| Analizadores | `src/analyzers/` | Extraer información de la oferta |
| Matching | `src/matching/` | Calcular coincidencias entre candidato y oferta |
| Vistas | `src/generators/` | Generar PDF y JSON de análisis |
| Controlador | `src/controllers/` | Coordinar el flujo completo (**pendiente**) |
| Utilidades | `src/utils/` | Funciones compartidas, como formato de fechas |

El `main.py` solo lee argumentos y llama al controlador.

**Consecuencias:**
- Cada capa se prueba por separado en `tests/unit/`, y el flujo completo en `tests/integration/`.
- Hasta que exista el controlador, `main.py` tiene la lógica del flujo. Hay que moverla cuando se implemente.

---

## ADR-009: Pruebas con pytest y verificación del PDF con pypdf

**Estado:** aceptada

**Contexto:** los scripts de prueba anteriores solo imprimían resultados y no validaban nada. Además, no basta con que el PDF se genere: debe contener el texto correcto.

**Decisión:**
- Las pruebas se escriben con pytest.
- Para validar el resultado, se lee el PDF generado con pypdf y se verifica que los encabezados y las skills aparecen como texto.
- Las pruebas que generan archivos usan carpetas temporales (`tmp_path`), no `output/`.
- pytest y pypdf están en `requirements-dev.txt`, que la imagen también instala por ahora.

**Consecuencias:**
- Se puede comprobar que un ATS encontrará el texto del CV.
- Las herramientas de desarrollo viven en la imagen de desarrollo. Cuando haya un despliegue de producción, conviene separarlas con un Dockerfile de varias etapas.

---

## ADR-010: output/ fuera del control de versiones

**Estado:** aceptada

**Contexto:** los PDF y análisis generados son resultados temporales y personales.

**Decisión:** `output/` está en `.gitignore` y se elimina del repositorio. El programa crea la carpeta cuando la necesita.

**Consecuencias:**
- El repositorio solo contiene código, plantillas y documentación.
- Antes de generar un archivo, el código debe crear el directorio padre con `Path(...).parent.mkdir(parents=True, exist_ok=True)`. Pendiente de implementar en `main.py`.

---

## ADR-011: Contenedor con nombre fijo y usuario del host

**Estado:** aceptada

**Contexto:** el contenedor se creó sin usuario definido, así que corría como root. Los archivos que generaba dentro de la carpeta montada quedaban a nombre de root y Git dejaba de poder escribir en `.git`.

**Decisión:**
- Crear un único contenedor con nombre fijo, `cvautomizer`, a partir de la imagen con tag `cvautomizer:1.0`.
- Ejecutarlo con el usuario del host: `--user $(id -u):$(id -g)`.
- Para cambiar de versión de imagen, eliminar el contenedor y crearlo de nuevo con el tag nuevo.
- Los comandos de Git se ejecutan desde la terminal del host, no desde el contenedor.

**Consecuencias:**
- Los archivos generados pertenecen al usuario del host.
- Dentro del contenedor, con un usuario distinto de root, `pip install` no puede escribir en las rutas del sistema. Las dependencias se agregan a `requirements.txt` y se reconstruye la imagen.

---

## ADR-012: Integrar cambios remotos con rebase y sin force push

**Estado:** aceptada

**Contexto:** al hacer push, GitHub rechazó el envío porque tenía un commit que la copia local no tenía.

**Decisión:**
- Integrar los cambios remotos con `git pull --rebase origin main` para mantener un historial lineal.
- No usar `git push --force` en la rama principal, porque borra commits del remoto.

**Consecuencias:**
- El historial queda en orden y sin commits de merge innecesarios.
- Si hay cambios sin confirmar, se guardan temporalmente con `git stash` antes del rebase.
