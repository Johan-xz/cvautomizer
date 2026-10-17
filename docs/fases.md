# Fases del proyecto

Las fases se ordenan por dependencia: cada una necesita que la anterior esté terminada. Las fechas no están comprometidas; el orden sí.

## Resumen

| Fase | Objetivo | Estado |
|---|---|---|
| 0. Entorno | Contenedor, Git y repositorio funcionando | Completada |
| 1. Modelo de datos | Datos del candidato validados contra el YAML | En curso |
| 2. Generador Harvard | PDF correcto a partir del modelo | Pendiente |
| 3. Matching | Adaptar el CV a cada oferta | Pendiente |
| 4. Compatibilidad ATS | Verificar que el PDF se lee bien | Pendiente |
| 5. Flujo y limpieza | Controlador, CLI y estructura final | Pendiente |

---

## Fase 0: Entorno (completada)

**Objetivo:** tener un entorno reproducible y el código en GitHub.

**Entregables:**
- Imagen `cvautomizer:1.0` con las dependencias de `requirements.txt`.
- Contenedor `cvautomizer` con la carpeta del proyecto montada.
- Repositorio sincronizado entre el equipo local y GitHub.
- `.gitignore` y `.dockerignore` que excluyen `output/` y los datos personales.

**Criterio de cierre:** cumplido. `python -c "import pydantic, yaml, reportlab"` funciona dentro del contenedor, y `git push` llega a GitHub.

---

## Fase 1: Modelo de datos (en curso)

**Objetivo:** que `Candidate` describa exactamente la estructura de `candidate.yaml` y que los datos inválidos se detecten al cargarlos.

**Entregables:**
- Modelos `Candidate`, `Experience`, `Leadership`, `Education`, `Skills` y `Language` (hecho).
- Validación de fechas `YYYY-MM` y `YYYY-MM-DD`, y de fin posterior a inicio (hecho).
- Función `formatear_mes` en `src/utils/dates.py` (hecho).
- Pruebas de validación en `tests/unit/` (hecho).
- Comprobación de que el YAML real carga sin errores (**pendiente de confirmar**).

**Criterio de cierre:** `pytest tests/unit` pasa completo, y el parser carga `data/candidate.yaml` sin errores.

**Riesgo conocido:** `setup_parser.py` sobrescribe los modelos y el parser si se ejecuta. Debe eliminarse antes de cerrar la fase.

---

## Fase 2: Generador Harvard (pendiente)

**Objetivo:** que `cv_generator.py` use los nombres de campo del modelo nuevo y produzca un PDF correcto.

**Entregables:**
- Adaptar el generador a `Candidate` actual. Hoy usa atributos que ya no existen, como `skills` como diccionario y `phone` sin valor por defecto.
- Escapar caracteres especiales antes de pasar texto a `Paragraph` (ver ADR-004).
- Usar `formatear_mes` para las fechas de experiencia y liderazgo.
- Mostrar EDUCATION antes de EXPERIENCE para egresados recientes (ver ADR-007).
- Revisar que el CV quepa en una página, o avisar cuando no quepa.
- Crear la carpeta de salida automáticamente en `main.py`.

**Criterio de cierre:** el PDF se genera con tu perfil real, y una prueba con pypdf confirma que los encabezados y las skills aparecen como texto.

---

## Fase 3: Matching (pendiente)

**Objetivo:** que el CV se adapte a cada oferta, no solo calcular un porcentaje.

**Entregables:**
- Normalizar nombres de skills con un diccionario de sinónimos: `Node.js` y `NodeJS`, `scikit-learn` y `sklearn`.
- Usar también `keywords` y `description` de la oferta, no solo `required_skills`.
- Calcular años de experiencia uniendo los periodos que se traslapan, para no inflar el total.
- Ordenar experiencias y bullets por relevancia para la oferta.
- Definir qué decide el matcher y qué se controla a mano con `show`.
- Corregir la división entre cero cuando la oferta no tiene skills requeridas.

**Criterio de cierre:** dos ofertas distintas producen CVs con distinto orden de contenido, y el porcentaje de match coincide con una comprobación manual.

---

## Fase 4: Compatibilidad ATS (pendiente)

**Objetivo:** que el PDF se lea correctamente por sistemas ATS.

**Entregables:**
- Pruebas que lean el PDF con pypdf y verifiquen encabezados estándar y skills clave.
- Fuentes con soporte para acentos y caracteres del español, sin ilustraciones que oculten texto.
- Metadatos del PDF: título y autor.
- Fechas en formato "Mes Año" en todo el documento.
- Revisión de cómo se extraen los caracteres especiales, como el `•` de las viñetas y el `–` de los rangos de fechas.

**Criterio de cierre:** el texto extraído del PDF contiene todas las secciones, skills y fechas esperadas, sin caracteres corruptos.

---

## Fase 5: Flujo y limpieza (pendiente)

**Objetivo:** que el flujo completo tenga una sola entrada clara y el proyecto quede listo para usarse con otros datos.

**Entregables:**
- Implementar `src/controllers/cv_controller.py` y mover ahí la lógica de `main.py`.
- `main.py` solo lee argumentos y llama al controlador.
- Pruebas de integración en `tests/integration/` que cubran el flujo completo.
- Eliminar `setup_parser.py` y el código que genera.
- Actualizar el README del repositorio, que hoy está desactualizado.

**Criterio de cierre:** `python main.py --candidate ... --offer ...` genera el PDF y el análisis sin pasos manuales.

---

## Trabajo futuro (sin fecha)

Estas ideas no están comprometidas. Se revisan cuando termine la fase 5.

- **Integración continua:** ejecutar las pruebas automáticamente en cada push con GitHub Actions.
- **Dockerfile de producción:** una imagen de varias etapas que no incluya pytest ni pypdf (ver ADR-009).
- **Más de una oferta a la vez:** procesar una carpeta de ofertas y generar un PDF por cada una.
- **Entrada en texto libre:** extraer requisitos de una oferta pegada como texto, no solo de JSON.
- **Salida en Word:** generar también `.docx` cuando un formulario lo pida.
- **Interfaz web:** un formulario para cargar la oferta y descargar el CV.
