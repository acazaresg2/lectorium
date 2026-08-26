TAREA A — PASO 3: EPUB DE LABORATORIO

## Objetivo

Implementar exclusivamente el Paso 3 — EPUB de laboratorio.

El resultado debe ser el fixture local permanente:

assets/fixtures/lab-book.epub

generado de forma reproducible a partir de su estructura fuente.

## Fuente de verdad

Antes de modificar cualquier archivo, lee:

1. PROJECT_SPEC.md
2. docs/PROJECT_CONTEXT.md, sección:
   "## 2. PASO 3 — EPUB DE LABORATORIO"

Estas fuentes definen el alcance y el contenido de esta tarea.

No inventes contenido, nombres, estructura ni requisitos distintos a los especificados.

Reader Contract V1 continúa siendo la autoridad del protocolo del lector, pero esta tarea no implementa ninguna funcionalidad del protocolo.

## Alcance

Implementa únicamente los artefactos correspondientes al Paso 3:

lab-book-source/
├── mimetype
├── META-INF/
│   └── container.xml
└── OEBPS/
    ├── content.opf
    ├── nav.xhtml
    ├── styles.css
    ├── Text/
    │   ├── chapter1.xhtml
    │   ├── chapter2.xhtml
    │   └── chapter3.xhtml
    └── Images/
        ├── cover.svg
        └── key.svg

y:

scripts/build-lab-epub.py

El resultado generado debe ser:

assets/fixtures/lab-book.epub

## Reglas de implementación

1. Crea lab-book-source/ con exactamente la estructura definida en docs/PROJECT_CONTEXT.md.

2. Utiliza exactamente el contenido especificado en las subsecciones 2.3 a 2.12 de docs/PROJECT_CONTEXT.md para los archivos del EPUB.

3. No modifiques, resumas, traduzcas, "mejores" ni reinventes el contenido especificado.

4. Crea scripts/build-lab-epub.py utilizando exactamente la implementación definida en la subsección 2.13 de docs/PROJECT_CONTEXT.md.

5. Ejecuta el script utilizando el intérprete disponible en este entorno:

python3 scripts/build-lab-epub.py

No asumas que existe el comando "python".

6. Conserva lab-book-source/ después de generar el EPUB. Esta carpeta es la fuente reproducible del fixture y no debe eliminarse.

7. assets/fixtures/lab-book.epub debe ser generado por el script y no creado manualmente.

## Validación

Después de generar el EPUB, valida como mínimo:

1. El archivo existe:
   assets/fixtures/lab-book.epub

2. Es un ZIP válido.

3. La primera entrada del ZIP es exactamente:
   mimetype

4. La entrada mimetype utiliza ZIP_STORED, es decir, está sin compresión.

5. El contenido exacto de mimetype es:
   application/epub+zip

6. Existen todas las entradas requeridas por la estructura fuente.

7. Las rutas internas del EPUB son correctas.

8. El EPUB pasa una validación estructural/EPUB con una herramienta de validación EPUB disponible en el entorno.

Si no existe una herramienta de validación EPUB disponible, NO sustituyas silenciosamente este requisito por una librería arbitraria ni agregues una dependencia de runtime al proyecto.

En ese caso:
- informa qué herramienta falta;
- puedes instalar temporalmente una herramienta de validación necesaria para esta comprobación si ello no modifica las dependencias del proyecto;
- ejecuta la validación;
- informa exactamente qué herramienta utilizaste y el resultado.

No agregues herramientas de validación como dependencias de producción del proyecto.

## Prueba de reproducibilidad

Después de generar y validar el EPUB:

1. Ejecuta nuevamente:

python3 scripts/build-lab-epub.py

2. Verifica que vuelve a generarse correctamente.
3. Comprueba que la estructura y contenido del EPUB siguen siendo equivalentes y válidos.

No modifiques el script únicamente para intentar obtener igualdad binaria byte-a-byte si la especificación actual no lo exige.

## Archivos permitidos

Puedes crear o modificar únicamente:

- lab-book-source/**
- scripts/build-lab-epub.py
- assets/fixtures/lab-book.epub

No modifiques otros archivos del proyecto.

## Qué NO hacer

No:

- modificar PROJECT_SPEC.md;
- modificar docs/PROJECT_CONTEXT.md;
- modificar package.json;
- instalar dependencias de runtime;
- instalar react-native-webview;
- instalar epub.js;
- instalar jszip;
- modificar app/;
- modificar src/;
- crear assets/libs/epub.min.js;
- crear assets/libs/jszip.min.js;
- implementar WebView;
- implementar EPUBWebView;
- implementar bridge-client;
- implementar ReaderBridge;
- implementar selección;
- implementar CFI;
- implementar persistencia;
- implementar SQLite;
- implementar traducción;
- implementar TTS;
- avanzar al Paso 4 ni a pasos posteriores.

No reutilices contenido de archivos históricos u obsoletos que no sean PROJECT_SPEC.md o docs/PROJECT_CONTEXT.md.

## Criterios de terminado

La tarea se considera terminada únicamente cuando:

- lab-book-source/ existe con exactamente la estructura especificada;
- todos sus archivos contienen el contenido definido por la documentación;
- scripts/build-lab-epub.py existe;
- python3 scripts/build-lab-epub.py termina correctamente;
- assets/fixtures/lab-book.epub existe;
- mimetype es la primera entrada y está sin compresión;
- el EPUB es estructuralmente válido;
- el EPUB pasa la herramienta de validación EPUB utilizada;
- una segunda ejecución del script vuelve a generar correctamente el fixture;
- no se modificaron archivos fuera del alcance de esta tarea.

## Informe final

Al terminar, informa:

1. Archivos creados.
2. Archivos modificados.
3. Comandos ejecutados.
4. Herramienta de validación EPUB utilizada.
5. Resultado de cada validación.
6. Árbol final de:
   - lab-book-source/
   - assets/fixtures/
   - scripts/
7. Cualquier problema o discrepancia encontrada.

No continúes automáticamente al Paso 4.

Detente al finalizar esta tarea y espera nuevas instrucciones.
