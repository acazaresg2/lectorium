# TAREA A — Paso 3: EPUB de laboratorio

Lee completo el archivo PROJECT_SPEC.md (raíz del repo) y luego la sección
"## 2. PASO 3 — EPUB DE LABORATORIO" completa de docs/PROJECT_CONTEXT.md
antes de hacer nada. Son tu única fuente de verdad para esta tarea. No
inventes contenido distinto al que ahí se especifica.

## Alcance de esta tarea
Únicamente la sección 2 de docs/PROJECT_CONTEXT.md (subsecciones 2.1 a 2.13):
mimetype, META-INF/container.xml, OEBPS/content.opf, OEBPS/nav.xhtml,
OEBPS/styles.css, OEBPS/Text/chapter1.xhtml, chapter2.xhtml, chapter3.xhtml,
OEBPS/Images/cover.svg, key.svg, y el script scripts/build-lab-epub.py
(subsección 2.13).

## Qué hacer
1. Crea la carpeta lab-book-source/ con exactamente la estructura de archivos
   descrita, copiando el contenido literal de cada bloque de código del
   documento — sin modificarlo, sin resumirlo, sin "mejorarlo".
2. Crea scripts/build-lab-epub.py con el contenido literal de la subsección
   2.13.
3. Ejecuta:
   python scripts/build-lab-epub.py
   para generar assets/fixtures/lab-book.epub.
4. Valida el EPUB resultante (con una herramienta de validación EPUB
   disponible, o abriéndolo con una librería EPUB estándar de Node) y
   muéstrame el resultado de esa validación.
5. Confírmame si lab-book-source/ debe conservarse como fuente reproducible
   del build o si prefiero borrarla (no la borres sin preguntar).

## Qué NO hacer
- No instales react-native-webview, epub.js ni jszip — eso es el Paso 4,
  no esta tarea.
- No toques nada dentro de src/ ni app/.
- No implementes ReaderBridge, selección, ni nada fuera del EPUB en sí.
- No reutilices contenido de archivos con nombres como "Paso 4 V1.1.txt",
  "Paso 5 V1.1.txt", "Condensado..." ni "Pasos_3_y_4.txt" si aparecen en el
  proyecto: son versiones obsoletas, ya reemplazadas por PROJECT_SPEC.md y
  docs/PROJECT_CONTEXT.md.

## Criterio de terminado
- assets/fixtures/lab-book.epub existe, es un ZIP válido con `mimetype` sin
  comprimir como primera entrada, y se abre correctamente con una librería
  EPUB estándar.
- scripts/build-lab-epub.py existe y es reproducible (correrlo de nuevo
  regenera el mismo archivo sin errores).
- Muéstrame el árbol final de assets/fixtures/ y scripts/, y un resumen
  breve de lo que hiciste.

Cuando termines, detente y espera mi confirmación antes de seguir con
cualquier otra tarea (no continúes automáticamente hacia el Paso 4).
