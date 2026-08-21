# ESPECIFICACIÓN TÉCNICA Y ARQUITECTURA: PROYECTO LECTORIUM (PASOS 3 Y 4)

## 1. REGLAS GENERALES Y ARQUITECTURA

* **Contrato:** Reader Contract V1 (`protocolVersion: 1.0`).
* **Fronteras del Proyecto:** `app/` para rutas/pantallas y `src/` para lógica/componentes del lector.
* **Política Local-First:** no existen dependencias remotas en runtime.
* **Política de CDN:** no se permite ningún `<script src="http://...">`, `<script src="https://...">`, CDN, fallback remoto o dependencia equivalente.
* **Librerías WebView:** `epub.js` y `jszip` deben existir como fuentes locales bajo `assets/libs/`.
* **Inyección WebView:** las fuentes JavaScript locales se inyectan dentro del HTML mediante placeholders.
* **Comandos Native→Web permitidos:**

  * `INIT_BOOK`
  * `GO_TO_LOCATION`
  * `NAVIGATE_NEXT`
  * `NAVIGATE_PREVIOUS`
  * `SET_FONT_SIZE`
  * `SET_THEME`
  * `CLEAR_SELECTION`
* **Eventos Web→Native utilizados por el prototipo:**

  * `READER_READY`
  * `BOOK_ERROR`
  * `LOCATION_CHANGED`
  * `PAGE_CHANGED`
  * `SELECTION_CLEARED`
  * `CHAPTER_ENDED`
* **Comandos/eventos obsoletos excluidos:** `LOAD_BOOK`, `GET_LOCATION`, `ADD_HIGHLIGHT`, `REMOVE_HIGHLIGHT`, `SET_HIGHLIGHTS`, `COMMAND_RESPONSE`, `HIGHLIGHT_CLICKED`.
* **Formato de mensajes:**

  * `type`
  * `requestId`
  * `protocolVersion`
  * `payload`
* **`requestId`:**

  * Native→Web: identificador correlacionable del comando.
  * Web→Native: identificador del evento emitido.
* **Fixture EPUB:** `assets/fixtures/lab-book.epub`.
* **Dependencias locales:**

  * `assets/libs/epub.min.js`
  * `assets/libs/jszip.min.js`

---

## 2. PASO 3 — EPUB DE LABORATORIO

### 2.1 Estructura del Fixture

```text
assets/
└── fixtures/
    └── lab-book.epub
```

### 2.2 Estructura fuente

```text
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
```

### 2.3 `mimetype`

```text
application/epub+zip
```

### 2.4 `META-INF/container.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<container
    version="1.0"
    xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile
        full-path="OEBPS/content.opf"
        media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
```

### 2.5 `OEBPS/content.opf`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<package
    xmlns="http://www.idpf.org/2007/opf"
    version="3.0"
    unique-identifier="book-id">

  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">
      urn:uuid:7a2e6f6e-4f4d-4f76-9c9c-6c5f7d1e2026
    </dc:identifier>

    <dc:title>The Lost Key / La llave perdida</dc:title>

    <dc:language>en</dc:language>
    <dc:language>es</dc:language>

    <dc:creator>Language Reader Lab</dc:creator>

    <dc:description>
      A bilingual laboratory EPUB for testing the Local-First reader.
      Un EPUB bilingüe de laboratorio para probar el lector Local-First.
    </dc:description>

    <meta property="dcterms:modified">
      2026-08-21T00:00:00Z
    </meta>

    <meta name="cover" content="cover-image"/>
  </metadata>

  <manifest>
    <item
        id="nav"
        href="nav.xhtml"
        media-type="application/xhtml+xml"
        properties="nav"/>

    <item
        id="chapter1"
        href="Text/chapter1.xhtml"
        media-type="application/xhtml+xml"/>

    <item
        id="chapter2"
        href="Text/chapter2.xhtml"
        media-type="application/xhtml+xml"/>

    <item
        id="chapter3"
        href="Text/chapter3.xhtml"
        media-type="application/xhtml+xml"/>

    <item
        id="styles"
        href="styles.css"
        media-type="text/css"/>

    <item
        id="cover-image"
        href="Images/cover.svg"
        media-type="image/svg+xml"
        properties="cover-image"/>

    <item
        id="key-image"
        href="Images/key.svg"
        media-type="image/svg+xml"/>
  </manifest>

  <spine>
    <itemref idref="chapter1"/>
    <itemref idref="chapter2"/>
    <itemref idref="chapter3"/>
  </spine>

</package>
```

### 2.6 `OEBPS/nav.xhtml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:epub="http://www.idpf.org/2007/ops"
    lang="en"
    xml:lang="en">

<head>
  <meta charset="UTF-8"/>
  <title>Contents / Contenido</title>
  <link rel="stylesheet" href="styles.css"/>
</head>

<body>

<nav epub:type="toc">

  <h1>Contents / Contenido</h1>

  <ol>
    <li>
      <a href="Text/chapter1.xhtml">
        Chapter 1: The Discovery / Capítulo 1: El descubrimiento
      </a>
    </li>

    <li>
      <a href="Text/chapter2.xhtml">
        Chapter 2: The Search / Capítulo 2: La búsqueda
      </a>
    </li>

    <li>
      <a href="Text/chapter3.xhtml">
        Chapter 3: The Reunion / Capítulo 3: El reencuentro
      </a>
    </li>
  </ol>

</nav>

</body>
</html>
```

### 2.7 `OEBPS/styles.css`

```css
html,
body {
  margin: 0;
  padding: 0;
}

body {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.65;
  margin: 1.5em;
  color: #202020;
  background: #ffffff;
}

h1,
h2,
h3 {
  font-family: Arial, Helvetica, sans-serif;
}

h1 {
  font-size: 1.8em;
}

h2 {
  font-size: 1.35em;
}

p {
  margin: 0 0 1em 0;
}

blockquote {
  margin: 1em 1.5em;
  padding: 0.75em 1em;
  border-left: 4px solid #888;
  background: #f2f2f2;
}

ul,
ol {
  margin-top: 0.5em;
  margin-bottom: 1em;
}

.note {
  padding: 0.75em;
  background: #f7f1c8;
  font-style: italic;
}

strong {
  font-weight: 700;
}

em {
  font-style: italic;
}

a {
  text-decoration: underline;
}

img {
  max-width: 100%;
}

.cover {
  text-align: center;
}

.img-inline {
  display: inline;
  vertical-align: middle;
  max-height: 1.3em;
}
```

### 2.8 `OEBPS/Text/chapter1.xhtml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html
    xmlns="http://www.w3.org/1999/xhtml"
    lang="en"
    xml:lang="en">

<head>
  <meta charset="UTF-8"/>
  <title>Chapter 1: The Discovery</title>
  <link rel="stylesheet" href="../styles.css"/>
</head>

<body>

<h1>
  Chapter 1: The Discovery /
  Capítulo 1: El descubrimiento
</h1>

<p lang="en">
  It was a <strong>rainy</strong> Tuesday afternoon when
  <em>Oliver</em> found an old wooden box in the attic.
  The box was covered in dust, and its lock was rusty.
</p>

<p lang="es">
  Era una tarde lluviosa de martes cuando Oliver encontró
  una vieja caja de madera en el ático.
</p>

<p>
  "Emma, come here! You have to see this!"
  he shouted.
</p>

<p>
  "¡Emma, ven aquí! ¡Tienes que ver esto!",
  gritó Oliver.
</p>

<p>
  Emma arrived carrying a small notebook.
  She looked at the box with curiosity.
</p>

<blockquote>
  "Some doors are meant to stay closed."
  / "Algunas puertas están hechas para permanecer cerradas."
</blockquote>

<p>
  The lock was stubborn, but after a few attempts it finally
  clicked. Inside they found a folded note and a tiny silver key.
</p>

<p class="note">
  Note / Nota: The inscription contained
  á, é, í, ó, ú, ñ and ordinary English characters.
</p>

<ul>
  <li>old-fashioned</li>
  <li>blue-green</li>
  <li>half-open</li>
  <li>mysterious</li>
</ul>

<p>
  Read more about the old house in the
  <a href="chapter2.xhtml">next chapter / siguiente capítulo</a>.
</p>

</body>
</html>
```

### 2.9 `OEBPS/Text/chapter2.xhtml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html
    xmlns="http://www.w3.org/1999/xhtml"
    lang="en"
    xml:lang="en">

<head>
  <meta charset="UTF-8"/>
  <title>Chapter 2: The Search</title>
  <link rel="stylesheet" href="../styles.css"/>
</head>

<body>

<h1>
  Chapter 2: The Search /
  Capítulo 2: La búsqueda
</h1>

<p>
  The note contained a simple sentence:
  <strong>“Find the room beneath the old clock.”</strong>
</p>

<p lang="es">
  La nota contenía una frase sencilla:
  <em>“Busca la habitación debajo del reloj antiguo.”</em>
</p>

<p>
  Oliver and Emma searched the house from top to bottom.
  They checked the library, the kitchen, and even the garden.
</p>

<p>
  "This is taking forever," Emma said.
  "Maybe we're looking in the wrong place."
</p>

<ol>
  <li>Check the attic.</li>
  <li>Check the library.</li>
  <li>Check the hallway.</li>
  <li>Check the room beneath the clock.</li>
</ol>

<p>
  At the end of the hallway they noticed a narrow,
  almost invisible door.
</p>

<p>
  The key did not fit.
  They tried again — slowly, carefully, patiently.
</p>

<p>
  "Wait," said Emma.
  "There is another keyhole."
</p>

<p lang="es">
  "Espera", dijo Emma.
  "Hay otra cerradura."
</p>

<p>
  Behind the second panel they discovered a small passage
  leading downstairs.
</p>

<p>
  The air smelled of stone, dust, and something strangely sweet.
</p>

</body>
</html>
```

### 2.10 `OEBPS/Text/chapter3.xhtml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html
    xmlns="http://www.w3.org/1999/xhtml"
    lang="en"
    xml:lang="en">

<head>
  <meta charset="UTF-8"/>
  <title>Chapter 3: The Reunion</title>
  <link rel="stylesheet" href="../styles.css"/>
</head>

<body>

<h1>
  Chapter 3: The Reunion /
  Capítulo 3: El reencuentro
</h1>

<p>
  At the bottom of the stairs they found a circular room.
  In the center stood a stone pedestal.
</p>

<p>
  On top of it lay a beautiful golden key,
  glowing softly
  <img
      src="../Images/key.svg"
      alt="A golden key / Una llave dorada"
      class="img-inline"/>
  in the darkness.
</p>

<p>
  Oliver picked it up carefully.
  "This must be the key from the story."
</p>

<p lang="es">
  Oliver la levantó con cuidado.
  "Esta debe ser la llave de la historia."
</p>

<p>
  A hidden mechanism began to move.
  Somewhere above them, an old door opened.
</p>

<p>
  They returned upstairs and found the wooden box waiting
  beside the grandfather clock.
</p>

<p>
  The golden key opened a second compartment.
  Inside was a letter from their grandfather.
</p>

<blockquote>
  If you found this key, you were curious enough to search,
  patient enough to continue, and brave enough to discover.
</blockquote>

<p lang="es">
  Si encontraste esta llave, fuiste lo bastante curioso para buscar,
  paciente para continuar y valiente para descubrir.
</p>

<p>
  The siblings smiled.
  The mystery was over — but another adventure was beginning.
</p>

</body>
</html>
```

### 2.11 `OEBPS/Images/cover.svg`

```xml
<svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 400 600"
    width="400"
    height="600">

  <rect width="400" height="600" fill="#263238"/>

  <text
      x="200"
      y="150"
      text-anchor="middle"
      font-family="Georgia, serif"
      font-size="32"
      fill="#ffffff">
    The Lost Key
  </text>

  <text
      x="200"
      y="195"
      text-anchor="middle"
      font-family="Georgia, serif"
      font-size="23"
      fill="#eeeeee">
    La llave perdida
  </text>

  <circle
      cx="200"
      cy="330"
      r="75"
      fill="none"
      stroke="#f5c542"
      stroke-width="10"/>

  <rect
      x="190"
      y="250"
      width="20"
      height="120"
      fill="#f5c542"/>

</svg>
```

### 2.12 `OEBPS/Images/key.svg`

```xml
<svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 200 120"
    width="200"
    height="120">

  <circle
      cx="55"
      cy="60"
      r="35"
      fill="none"
      stroke="#d4a017"
      stroke-width="10"/>

  <path
      d="M85 60 H175 M145 60 V40 M160 60 V80"
      fill="none"
      stroke="#d4a017"
      stroke-width="10"
      stroke-linecap="square"/>

</svg>
```

### 2.13 `scripts/build-lab-epub.py`

```python
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
import shutil

ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "lab-book-source"
OUTPUT = ROOT / "assets" / "fixtures" / "lab-book.epub"

REQUIRED = [
    SOURCE / "mimetype",
    SOURCE / "META-INF" / "container.xml",
    SOURCE / "OEBPS" / "content.opf",
    SOURCE / "OEBPS" / "nav.xhtml",
    SOURCE / "OEBPS" / "styles.css",
    SOURCE / "OEBPS" / "Text" / "chapter1.xhtml",
    SOURCE / "OEBPS" / "Text" / "chapter2.xhtml",
    SOURCE / "OEBPS" / "Text" / "chapter3.xhtml",
    SOURCE / "OEBPS" / "Images" / "cover.svg",
    SOURCE / "OEBPS" / "Images" / "key.svg",
]

for path in REQUIRED:
    if not path.exists():
        raise FileNotFoundError(f"Missing EPUB source file: {path}")

mime = (SOURCE / "mimetype").read_text(encoding="utf-8")

if mime != "application/epub+zip":
    raise ValueError("mimetype must contain exactly application/epub+zip")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

if OUTPUT.exists():
    OUTPUT.unlink()

with ZipFile(OUTPUT, "w") as epub:
    # EPUB requirement: first entry and uncompressed.
    epub.writestr(
        "mimetype",
        mime,
        compress_type=ZIP_STORED,
    )

    for source_file in REQUIRED[1:]:
        relative = source_file.relative_to(SOURCE)
        epub.write(
            source_file,
            relative.as_posix(),
            compress_type=ZIP_DEFLATED,
        )

print(f"Created: {OUTPUT}")
```

Comando de generación:

```bash
python scripts/build-lab-epub.py
```

Salida:

```text
assets/fixtures/lab-book.epub
```

---

## 3. PASO 4 — BUNDLE Y DEPENDENCIAS LOCALES

### 3.1 Estructura de Archivos

```text
assets/
├── fixtures/
│   └── lab-book.epub
│
└── libs/
    ├── epub.min.js
    └── jszip.min.js

src/
└── reader/
    └── engines/
        └── webview/
            ├── EPUBWebView.tsx
            └── epub-webview-bundle/
                ├── index.html
                └── bridge-client.js
```

### 3.2 `assets/libs/epub.min.js`

Archivo de distribución local de `epub.js`.

Requisitos:

* Debe existir físicamente en `assets/libs/epub.min.js`.
* Debe contener exclusivamente la fuente distribuible de `epub.js`.
* No debe contener un `<script>` externo.
* No debe contener una URL CDN.
* No debe cargarse desde una URL durante runtime.

Versión fijada para el empaquetado:

```bash
npm pack epubjs@0.3.71
```

### 3.3 `assets/libs/jszip.min.js`

Archivo de distribución local de JSZip.

Requisitos:

* Debe existir físicamente en `assets/libs/jszip.min.js`.
* Debe contener exclusivamente la fuente distribuible de JSZip.
* No debe contener un `<script>` externo.
* No debe contener una URL CDN.
* No debe cargarse desde una URL durante runtime.

Versión fijada para el empaquetado:

```bash
npm pack jszip@3.10.1
```

### 3.4 Implementación del HTML Bundle (`index.html`)

Ruta:

```text
src/reader/engines/webview/epub-webview-bundle/index.html
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">

  <meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no,
             viewport-fit=cover"
  >

  <title>Reader</title>

  <style>
    * {
      box-sizing: border-box;
    }

    html,
    body {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: #ffffff;
    }

    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #viewer {
      width: 100%;
      height: 100%;
      overflow: hidden;
      position: relative;
    }
  </style>
</head>

<body>

  <div id="viewer"></div>

  <script>
    /* JSZIP_PLACEHOLDER */
  </script>

  <script>
    /* EPUBJS_PLACEHOLDER */
  </script>

  <script>
    /* BRIDGE_CLIENT_PLACEHOLDER */
  </script>

</body>
</html>
```

### 3.5 Implementación del Bridge Client (`bridge-client.js`)

Ruta:

```text
src/reader/engines/webview/epub-webview-bundle/bridge-client.js
```

```javascript
(function () {
  'use strict';

  var PROTOCOL_VERSION = '1.0';

  var book = null;
  var rendition = null;

  var bookId = null;
  var bookFormat = null;
  var currentLocation = null;
  var isInitialized = false;

  function createId(prefix) {
    var random =
      Math.random().toString(36).slice(2) +
      Math.random().toString(36).slice(2);

    return prefix + '-' + Date.now().toString(36) + '-' + random;
  }

  function postEvent(type, payload, requestId) {
    var message = {
      type: type,
      requestId: requestId || createId('event'),
      protocolVersion: PROTOCOL_VERSION,
      payload: payload
    };

    if (
      window.ReactNativeWebView &&
      typeof window.ReactNativeWebView.postMessage === 'function'
    ) {
      window.ReactNativeWebView.postMessage(
        JSON.stringify(message)
      );
    }
  }

  function postError(code, message, requestId) {
    postEvent(
      'BOOK_ERROR',
      {
        code: code,
        message: message
      },
      requestId
    );
  }

  function destroyBook() {
    try {
      if (rendition) {
        rendition.destroy();
      }
    } catch (_) {
      // Cleanup is best-effort.
    }

    try {
      if (book) {
        book.destroy();
      }
    } catch (_) {
      // Cleanup is best-effort.
    }

    rendition = null;
    book = null;
    currentLocation = null;
    isInitialized = false;
  }

  function getSpineItems() {
    if (!book || !book.spine || !book.spine.items) {
      return [];
    }

    return book.spine.items;
  }

  function getCurrentLocation() {
    if (!rendition) {
      return null;
    }

    var location = null;

    try {
      location = rendition.currentLocation();
    } catch (_) {
      return null;
    }

    if (!location || !location.start) {
      return null;
    }

    var start = location.start;
    var spineItems = getSpineItems();

    var chapterIndex =
      typeof start.index === 'number'
        ? start.index
        : 0;

    var chapter = spineItems[chapterIndex];

    var cfi = start.cfi || '';

    var progress = 0;

    try {
      if (typeof rendition.progress === 'function') {
        progress = Number(rendition.progress()) || 0;
      }
    } catch (_) {
      progress = 0;
    }

    progress = Math.max(
      0,
      Math.min(100, Math.round(progress * 100))
    );

    return {
      format: 'epub',
      bookId: bookId,
      chapterIndex: chapterIndex,
      chapterTitle:
        chapter && chapter.label
          ? String(chapter.label)
          : undefined,
      progressPercentage: progress,
      totalChapters: spineItems.length,
      cfi: cfi
    };
  }

  function emitLocationChanged(requestId) {
    var location = getCurrentLocation();

    if (!location) {
      return;
    }

    currentLocation = location;

    postEvent(
      'LOCATION_CHANGED',
      {
        location: location
      },
      requestId
    );
  }

  function emitPageChanged(requestId) {
    var location = getCurrentLocation();

    if (!location) {
      return;
    }

    currentLocation = location;

    var pageIndex;
    var totalPages;

    try {
      var current = rendition.currentLocation();

      if (current && current.start) {
        if (typeof current.start.displayedPage === 'number') {
          pageIndex = current.start.displayedPage;
        }

        if (typeof current.start.displayedTotal === 'number') {
          totalPages = current.start.displayedTotal;
        }
      }
    } catch (_) {
      // Page information is optional.
    }

    postEvent(
      'PAGE_CHANGED',
      {
        location: location,
        pageIndex: pageIndex,
        totalPages: totalPages
      },
      requestId
    );
  }

  function emitChapterEnded() {
    var location = getCurrentLocation();

    if (!location) {
      return;
    }

    postEvent(
      'CHAPTER_ENDED',
      {
        location: location
      }
    );
  }

  function setupRenditionEvents() {
    if (!rendition) {
      return;
    }

    rendition.on(
      'locationChanged',
      function () {
        emitLocationChanged();
        emitPageChanged();
      }
    );

    rendition.on(
      'rendered',
      function () {
        emitPageChanged();
      }
    );

    rendition.on(
      'relocated',
      function () {
        emitLocationChanged();
        emitPageChanged();
      }
    );

    rendition.on(
      'displayed',
      function () {
        emitLocationChanged();
        emitPageChanged();
      }
    );

    rendition.on(
      'renderError',
      function (error) {
        postError(
          'EPUB_RENDER_FAILED',
          error && error.message
            ? error.message
            : 'EPUB render failed.'
        );
      }
    );
  }

  function decodeDataUri(uri) {
    var commaIndex = uri.indexOf(',');

    if (commaIndex === -1) {
      throw new Error('Invalid EPUB data URI.');
    }

    var metadata = uri.slice(0, commaIndex);
    var data = uri.slice(commaIndex + 1);

    var isBase64 = metadata.indexOf(';base64') !== -1;

    if (!isBase64) {
      throw new Error(
        'EPUB data URI must use base64 encoding.'
      );
    }

    var binary = window.atob(data);
    var bytes = new Uint8Array(binary.length);

    for (var i = 0; i < binary.length; i += 1) {
      bytes[i] = binary.charCodeAt(i);
    }

    return bytes.buffer;
  }

  function loadBook(payload, requestId) {
    if (!payload) {
      postError(
        'EPUB_LOAD_FAILED',
        'INIT_BOOK payload is missing.',
        requestId
      );
      return;
    }

    if (payload.format !== 'epub') {
      postError(
        'EPUB_INVALID',
        'The WebView prototype only accepts format "epub".',
        requestId
      );
      return;
    }

    if (!payload.bookId) {
      postError(
        'EPUB_INVALID',
        'INIT_BOOK requires bookId.',
        requestId
      );
      return;
    }

    if (!payload.fileUri) {
      postError(
        'EPUB_LOAD_FAILED',
        'INIT_BOOK requires fileUri.',
        requestId
      );
      return;
    }

    if (typeof window.ePub !== 'function') {
      postError(
        'EPUB_LOAD_FAILED',
        'Local epub.js is not available.',
        requestId
      );
      return;
    }

    try {
      destroyBook();

      bookId = payload.bookId;
      bookFormat = payload.format;

      /*
       * Paso 4:
       * El Native side convierte temporalmente el EPUB local
       * a una data URI y la entrega mediante el campo fileUri.
       *
       * Esto permite mantener INIT_BOOK como único comando,
       * sin crear un payload alternativo como base64Data.
       */
      var arrayBuffer = decodeDataUri(payload.fileUri);

      book = window.ePub(arrayBuffer);

      var viewer = document.getElementById('viewer');

      if (!viewer) {
        throw new Error(
          'Reader viewer element was not found.'
        );
      }

      rendition = book.renderTo(
        viewer,
        {
          width: '100%',
          height: '100%',
          flow: 'paginated',
          spread: 'none'
        }
      );

      setupRenditionEvents();

      book.ready
        .then(function () {
          return rendition.display(
            payload.initialLocation &&
            payload.initialLocation.format === 'epub' &&
            payload.initialLocation.cfi
              ? payload.initialLocation.cfi
              : undefined
          );
        })
        .then(function () {
          isInitialized = true;

          var location = getCurrentLocation();

          if (location) {
            currentLocation = location;
          }

          /*
           * READER_READY is a lifecycle event.
           * It does not become a COMMAND_RESPONSE.
           */
          postEvent(
            'READER_READY',
            {
              version: PROTOCOL_VERSION
            }
          );

          emitLocationChanged();
          emitPageChanged();
        })
        .catch(function (error) {
          postError(
            'EPUB_LOAD_FAILED',
            error && error.message
              ? error.message
              : 'Unable to initialize EPUB.',
            requestId
          );
        });
    } catch (error) {
      postError(
        'EPUB_LOAD_FAILED',
        error && error.message
          ? error.message
          : 'Unable to load EPUB.',
        requestId
      );
    }
  }

  function goToLocation(payload, requestId) {
    if (!rendition || !isInitialized) {
      postError(
        'READER_INITIALIZATION_FAILED',
        'Reader is not initialized.',
        requestId
      );
      return;
    }

    if (
      !payload ||
      !payload.location ||
      payload.location.format !== 'epub'
    ) {
      postError(
        'LOCATION_INVALID',
        'GO_TO_LOCATION requires an EPUB ReaderLocation.',
        requestId
      );
      return;
    }

    if (!payload.location.cfi) {
      postError(
        'LOCATION_INVALID',
        'EPUB ReaderLocation requires cfi.',
        requestId
      );
      return;
    }

    rendition
      .display(payload.location.cfi)
      .then(function () {
        emitLocationChanged(requestId);
        emitPageChanged();
      })
      .catch(function (error) {
        postError(
          'EPUB_RENDER_FAILED',
          error && error.message
            ? error.message
            : 'Unable to navigate to location.',
          requestId
        );
      });
  }

  function navigateNext(requestId) {
    if (!rendition || !isInitialized) {
      postError(
        'READER_INITIALIZATION_FAILED',
        'Reader is not initialized.',
        requestId
      );
      return;
    }

    rendition
      .next()
      .then(function () {
        emitLocationChanged(requestId);
        emitPageChanged();
      })
      .catch(function (error) {
        postError(
          'EPUB_RENDER_FAILED',
          error && error.message
            ? error.message
            : 'Unable to navigate next.',
          requestId
        );
      });
  }

  function navigatePrevious(requestId) {
    if (!rendition || !isInitialized) {
      postError(
        'READER_INITIALIZATION_FAILED',
        'Reader is not initialized.',
        requestId
      );
      return;
    }

    rendition
      .prev()
      .then(function () {
        emitLocationChanged(requestId);
        emitPageChanged();
      })
      .catch(function (error) {
        postError(
          'EPUB_RENDER_FAILED',
          error && error.message
            ? error.message
            : 'Unable to navigate previous.',
          requestId
        );
      });
  }

  function setFontSize(payload, requestId) {
    if (!rendition || !isInitialized) {
      postError(
        'READER_INITIALIZATION_FAILED',
        'Reader is not initialized.',
        requestId
      );
      return;
    }

    var fontSize = Number(payload && payload.fontSize);

    if (!isFinite(fontSize) || fontSize <= 0) {
      postError(
        'LOCATION_INVALID',
        'fontSize must be a positive number.',
        requestId
      );
      return;
    }

    try {
      rendition.themes.fontSize(
        String(fontSize) + '%'
      );

      emitLocationChanged(requestId);
    } catch (error) {
      postError(
        'EPUB_RENDER_FAILED',
        error && error.message
          ? error.message
          : 'Unable to change font size.',
        requestId
      );
    }
  }

  function setTheme(payload, requestId) {
    if (!rendition || !isInitialized) {
      postError(
        'READER_INITIALIZATION_FAILED',
        'Reader is not initialized.',
        requestId
      );
      return;
    }

    var theme = payload && payload.theme;

    if (
      theme !== 'light' &&
      theme !== 'dark' &&
      theme !== 'sepia'
    ) {
      postError(
        'EPUB_RENDER_FAILED',
        'Unsupported reader theme.',
        requestId
      );
      return;
    }

    var background = '#ffffff';
    var foreground = '#1a1a1a';

    if (theme === 'dark') {
      background = '#121212';
      foreground = '#eeeeee';
    }

    if (theme === 'sepia') {
      background = '#f4ecd8';
      foreground = '#3b3b3b';
    }

    try {
      rendition.themes.default({
        body: {
          background: background + ' !important',
          color: foreground + ' !important'
        }
      });

      emitLocationChanged(requestId);
    } catch (error) {
      postError(
        'EPUB_RENDER_FAILED',
        error && error.message
          ? error.message
          : 'Unable to change theme.',
        requestId
      );
    }
  }

  function clearSelection(requestId) {
    try {
      var selection = window.getSelection();

      if (selection) {
        selection.removeAllRanges();
      }

      if (
        rendition &&
        rendition.getContents
      ) {
        var contents = rendition.getContents();

        contents.forEach(function (content) {
          var documentSelection =
            content.document.getSelection();

          if (documentSelection) {
            documentSelection.removeAllRanges();
          }
        });
      }

      postEvent(
        'SELECTION_CLEARED',
        {},
        requestId
      );
    } catch (error) {
      postError(
        'READER_INITIALIZATION_FAILED',
        error && error.message
          ? error.message
          : 'Unable to clear selection.',
        requestId
      );
    }
  }

  function handleCommand(message) {
    if (!message || typeof message !== 'object') {
      return;
    }

    if (message.protocolVersion !== PROTOCOL_VERSION) {
      postError(
        'PROTOCOL_VERSION_MISMATCH',
        'Expected protocol version ' +
          PROTOCOL_VERSION +
          ', received ' +
          String(message.protocolVersion),
        message.requestId
      );

      return;
    }

    if (
      typeof message.requestId !== 'string' ||
      message.requestId.length === 0
    ) {
      postError(
        'READER_INITIALIZATION_FAILED',
        'Protocol message requires a non-empty requestId.'
      );

      return;
    }

    switch (message.type) {
      case 'INIT_BOOK':
        loadBook(message.payload, message.requestId);
        break;

      case 'GO_TO_LOCATION':
        goToLocation(message.payload, message.requestId);
        break;

      case 'NAVIGATE_NEXT':
        navigateNext(message.requestId);
        break;

      case 'NAVIGATE_PREVIOUS':
        navigatePrevious(message.requestId);
        break;

      case 'SET_FONT_SIZE':
        setFontSize(message.payload, message.requestId);
        break;

      case 'SET_THEME':
        setTheme(message.payload, message.requestId);
        break;

      case 'CLEAR_SELECTION':
        clearSelection(message.requestId);
        break;

      default:
        /*
         * No se crea ningún evento "COMMAND_RESPONSE".
         * Los comandos fuera del contrato simplemente no son aceptados.
         */
        postError(
          'READER_INITIALIZATION_FAILED',
          'Unsupported Reader Contract V1 command: ' +
            String(message.type),
          message.requestId
        );
        break;
    }
  }

  function handleNativeMessage(event) {
    try {
      var raw = event && event.data;

      if (typeof raw !== 'string') {
        return;
      }

      var message = JSON.parse(raw);

      handleCommand(message);
    } catch (error) {
      postError(
        'READER_INITIALIZATION_FAILED',
        error && error.message
          ? error.message
          : 'Invalid protocol message.'
      );
    }
  }

  window.addEventListener(
    'message',
    handleNativeMessage
  );

  document.addEventListener(
    'message',
    handleNativeMessage
  );

  window.destroyReader = function () {
    destroyBook();

    bookId = null;
    bookFormat = null;
  };

  /*
   * READER_READY here means:
   * "The WebView bundle itself is initialized."
   *
   * Book readiness is emitted again after INIT_BOOK succeeds.
   */
  postEvent(
    'READER_READY',
    {
      version: PROTOCOL_VERSION
    }
  );

})();
```

### 3.6 Componente React Native (`EPUBWebView.tsx`)

Ruta:

```text
src/reader/engines/webview/EPUBWebView.tsx
```

```tsx
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import {
  ActivityIndicator,
  StyleSheet,
  View,
} from 'react-native';
import WebView, {
  WebViewMessageEvent,
} from 'react-native-webview';

import * as FileSystem from 'expo-file-system';
import { Asset } from 'expo-asset';

import type { ReaderLocation } from '../../types/ReaderLocation';

const PROTOCOL_VERSION = '1.0';

type ReaderTheme = 'light' | 'dark' | 'sepia';

type ReaderMessage = {
  type: string;
  requestId: string;
  protocolVersion: string;
  payload: unknown;
};

type EPUBWebViewProps = {
  bookId: string;
  fileUri: string;

  initialLocation?: ReaderLocation;

  onReady?: () => void;

  onLocationChange?: (
    location: ReaderLocation
  ) => void;

  onPageChange?: (payload: {
    location: ReaderLocation;
    pageIndex?: number;
    totalPages?: number;
  }) => void;

  onChapterEnded?: (
    location: ReaderLocation
  ) => void;

  onError?: (
    code: string,
    message: string
  ) => void;
};

const HTML_TEMPLATE = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">

  <meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no,
             viewport-fit=cover"
  >

  <title>Reader</title>

  <style>
    * {
      box-sizing: border-box;
    }

    html,
    body {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: #ffffff;
    }

    body {
      font-family:
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        sans-serif;
    }

    #viewer {
      width: 100%;
      height: 100%;
      overflow: hidden;
      position: relative;
    }
  </style>
</head>

<body>

  <div id="viewer"></div>

  <script>
    /* JSZIP_PLACEHOLDER */
  </script>

  <script>
    /* EPUBJS_PLACEHOLDER */
  </script>

  <script>
    /* BRIDGE_CLIENT_PLACEHOLDER */
  </script>

</body>
</html>
`;

function escapeScriptSource(
  source: string
): string {
  /*
   * Evita que una aparición accidental de </script>
   * cierre el script contenedor.
   */
  return source.replace(
    /<\/script/gi,
    '<\\/script'
  );
}

function createRequestId(
  prefix: string
): string {
  const random =
    Math.random().toString(36).slice(2) +
    Math.random().toString(36).slice(2);

  return (
    prefix +
    '-' +
    Date.now().toString(36) +
    '-' +
    random
  );
}

function buildCommand(
  type:
    | 'INIT_BOOK'
    | 'GO_TO_LOCATION'
    | 'NAVIGATE_NEXT'
    | 'NAVIGATE_PREVIOUS'
    | 'SET_FONT_SIZE'
    | 'SET_THEME'
    | 'CLEAR_SELECTION',
  payload: unknown
): ReaderMessage {
  return {
    type,
    requestId: createRequestId('cmd'),
    protocolVersion: PROTOCOL_VERSION,
    payload,
  };
}

async function readLocalAssetSource(
  moduleReference: number
): Promise<string> {
  const asset = Asset.fromModule(
    moduleReference
  );

  await asset.downloadAsync();

  if (!asset.localUri) {
    throw new Error(
      'Local asset URI is unavailable.'
    );
  }

  return FileSystem.readAsStringAsync(
    asset.localUri,
    {
      encoding:
        FileSystem.EncodingType.UTF8,
    }
  );
}

function normalizeFileUriForPrototype(
  base64: string
): string {
  /*
   * Paso 4:
   * INIT_BOOK mantiene su único payload contractual.
   *
   * fileUri se representa temporalmente como una
   * data URI local para transportar el fixture al WebView.
   *
   * No se crea base64Data ni LOAD_BOOK.
   */
  return (
    'data:application/epub+zip;base64,' +
    base64
  );
}

export const EPUBWebView: React.FC<
  EPUBWebViewProps
> = ({
  bookId,
  fileUri,
  initialLocation,
  onReady,
  onLocationChange,
  onPageChange,
  onChapterEnded,
  onError,
}) => {
  const webViewRef =
    useRef<WebView>(null);

  const [
    htmlContent,
    setHtmlContent,
  ] = useState<string | null>(null);

  const [
    bookDataUri,
    setBookDataUri,
  ] = useState<string | null>(null);

  const [
    initializationError,
    setInitializationError,
  ] = useState<string | null>(null);

  const [
    isWebViewMounted,
    setIsWebViewMounted,
  ] = useState(false);

  /*
   * Carga de assets locales:
   *
   * Estos archivos deben existir físicamente:
   *
   * assets/libs/jszip.min.js
   * assets/libs/epub.min.js
   */
  useEffect(() => {
    let cancelled = false;

    async function prepareHtml() {
      try {
        setInitializationError(null);

        /*
         * Los require() apuntan a archivos locales.
         *
         * Si Metro/Expo de tu proyecto no trata .js como
         * asset textual, usa el paso de empaquetado indicado
         * en la documentación del proyecto para convertir
         * estos vendor files en recursos de texto locales.
         */
        const jszipSource =
          await readLocalAssetSource(
            require('../../../../../assets/libs/jszip.min.js')
          );

        const epubSource =
          await readLocalAssetSource(
            require('../../../../../assets/libs/epub.min.js')
          );

        /*
         * bridge-client.js no se carga mediante <script src>.
         * Se incorpora como fuente local.
         */
        const bridgeClientSource =
          await readLocalAssetSource(
            require('./epub-webview-bundle/bridge-client.js')
          );

        if (cancelled) {
          return;
        }

        const finalHtml =
          HTML_TEMPLATE
            .replace(
              '/* JSZIP_PLACEHOLDER */',
              escapeScriptSource(
                jszipSource
              )
            )
            .replace(
              '/* EPUBJS_PLACEHOLDER */',
              escapeScriptSource(
                epubSource
              )
            )
            .replace(
              '/* BRIDGE_CLIENT_PLACEHOLDER */',
              escapeScriptSource(
                bridgeClientSource
              )
            );

        setHtmlContent(finalHtml);
      } catch (error) {
        if (cancelled) {
          return;
        }

        const message =
          error instanceof Error
            ? error.message
            : 'Unable to prepare reader bundle.';

        setInitializationError(message);

        onError?.(
          'READER_INITIALIZATION_FAILED',
          message
        );
      }
    }

    prepareHtml();

    return () => {
      cancelled = true;
    };
  }, [onError]);

  /*
   * El EPUB se mantiene fuera del WebView hasta que
   * el HTML local está preparado.
   */
  useEffect(() => {
    let cancelled = false;

    async function loadBookFile() {
      try {
        const info =
          await FileSystem.getInfoAsync(
            fileUri
          );

        if (!info.exists) {
          throw new Error(
            `EPUB file does not exist: ${fileUri}`
          );
        }

        const base64 =
          await FileSystem.readAsStringAsync(
            fileUri,
            {
              encoding:
                FileSystem.EncodingType.Base64,
            }
          );

        if (cancelled) {
          return;
        }

        setBookDataUri(
          normalizeFileUriForPrototype(
            base64
          )
        );
      } catch (error) {
        if (cancelled) {
          return;
        }

        const message =
          error instanceof Error
            ? error.message
            : 'Unable to read EPUB file.';

        setInitializationError(message);

        onError?.(
          'EPUB_LOAD_FAILED',
          message
        );
      }
    }

    loadBookFile();

    return () => {
      cancelled = true;
    };
  }, [fileUri, onError]);

  const sendCommand =
    useCallback(
      (
        type:
          | 'INIT_BOOK'
          | 'GO_TO_LOCATION'
          | 'NAVIGATE_NEXT'
          | 'NAVIGATE_PREVIOUS'
          | 'SET_FONT_SIZE'
          | 'SET_THEME'
          | 'CLEAR_SELECTION',
        payload: unknown
      ) => {
        if (!webViewRef.current) {
          return;
        }

        const message =
          buildCommand(
            type,
            payload
          );

        webViewRef.current.postMessage(
          JSON.stringify(message)
        );
      },
      []
    );

  /*
   * En cuanto el WebView ya fue montado y tenemos
   * el EPUB local, enviamos INIT_BOOK.
   */
  useEffect(() => {
    if (
      !isWebViewMounted ||
      !bookDataUri ||
      !webViewRef.current
    ) {
      return;
    }

    sendCommand(
      'INIT_BOOK',
      {
        bookId,
        fileUri: bookDataUri,
        format: 'epub',
        initialLocation:
          initialLocation?.format === 'epub'
            ? initialLocation
            : undefined,
      }
    );
  }, [
    isWebViewMounted,
    bookDataUri,
    bookId,
    initialLocation,
    sendCommand,
  ]);

  const handleMessage =
    useCallback(
      (
        event: WebViewMessageEvent
      ) => {
        try {
          const message =
            JSON.parse(
              event.nativeEvent.data
            ) as ReaderMessage;

          if (
            message.protocolVersion !==
            PROTOCOL_VERSION
          ) {
            onError?.(
              'PROTOCOL_VERSION_MISMATCH',
              `Expected protocol ${PROTOCOL_VERSION}, received ${message.protocolVersion}.`
            );

            return;
          }

          switch (message.type) {
            case 'READER_READY': {
              onReady?.();
              break;
            }

            case 'BOOK_ERROR': {
              const payload =
                message.payload as {
                  code?: string;
                  message?: string;
                };

              onError?.(
                payload.code ??
                  'READER_INITIALIZATION_FAILED',
                payload.message ??
                  'Unknown reader error.'
              );

              break;
            }

            case 'LOCATION_CHANGED': {
              const payload =
                message.payload as {
                  location: ReaderLocation;
                };

              if (payload.location) {
                onLocationChange?.(
                  payload.location
                );
              }

              break;
            }

            case 'PAGE_CHANGED': {
              const payload =
                message.payload as {
                  location: ReaderLocation;
                  pageIndex?: number;
                  totalPages?: number;
                };

              if (payload.location) {
                onPageChange?.({
                  location:
                    payload.location,
                  pageIndex:
                    payload.pageIndex,
                  totalPages:
                    payload.totalPages,
                });
              }

              break;
            }

            case 'CHAPTER_ENDED': {
              const payload =
                message.payload as {
                  location: ReaderLocation;
                };

              if (payload.location) {
                onChapterEnded?.(
                  payload.location
                );
              }

              break;
            }

            case 'SELECTION_CLEARED':
              /*
               * El Paso 4 no implementa selección.
               * El evento pertenece al contrato, pero su
               * comportamiento completo se implementará
               * en Paso 6.
               */
              break;

            default:
              /*
               * No hay compatibilidad hacia atrás.
               * No se reconocen comandos/eventos obsoletos.
               */
              break;
          }
        } catch (error) {
          const message =
            error instanceof Error
              ? error.message
              : 'Invalid WebView message.';

          onError?.(
            'READER_INITIALIZATION_FAILED',
            message
          );
        }
      },
      [
        onReady,
        onLocationChange,
        onPageChange,
        onChapterEnded,
        onError,
      ]
    );

  /*
   * Limpieza del lector al desmontar.
   */
  useEffect(() => {
    return () => {
      try {
        webViewRef.current?.injectJavaScript(
          `
            if (window.destroyReader) {
              window.destroyReader();
            }
            true;
          `
        );
      } catch {
        // WebView may already be destroyed.
      }
    };
  }, []);

  const loading =
    !htmlContent ||
    !bookDataUri;

  if (initializationError) {
    return (
      <View
        style={styles.errorContainer}
      >
        <ActivityIndicator size="small" />
      </View>
    );
  }

  if (loading) {
    return (
      <View
        style={styles.loadingContainer}
      >
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <WebView
        ref={webViewRef}
        source={{
          html: htmlContent,
          baseUrl: '',
        }}
        style={styles.webview}
        javaScriptEnabled
        domStorageEnabled
        originWhitelist={['*']}
        scrollEnabled={false}
        onLoadEnd={() => {
          setIsWebViewMounted(true);
        }}
        onMessage={handleMessage}
        onError={(event) => {
          onError?.(
            'READER_INITIALIZATION_FAILED',
            event.nativeEvent.description ||
              'WebView error.'
          );
        }}
        showsVerticalScrollIndicator={false}
        showsHorizontalScrollIndicator={false}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },

  webview: {
    flex: 1,
    backgroundColor: '#ffffff',
  },

  loadingContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ffffff',
  },

  errorContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ffffff',
  },
});
```

---

## 4. AJUSTES DE EMPAQUETADO Y METRO/EXPO

### 4.1 Requisitos

* `epub.min.js` debe permanecer en `assets/libs/epub.min.js`.
* `jszip.min.js` debe permanecer en `assets/libs/jszip.min.js`.
* `bridge-client.js` debe permanecer en `src/reader/engines/webview/epub-webview-bundle/`.
* Ninguno de estos archivos debe cargarse mediante `<script src>`.
* El HTML final debe contener el código fuente de las tres dependencias inyectado directamente.
* El bundle final del WebView no debe depender de red.
* El EPUB se lee localmente mediante `expo-file-system`.
* El EPUB se transporta al WebView mediante el campo contractual `fileUri`, utilizando una `data:application/epub+zip;base64,...` local en este prototipo.
* No se introduce `base64Data` como campo adicional del contrato.
* No se introduce ningún comando alternativo para la carga del libro.

### 4.2 Flujo de empaquetado

```text
archivo local
      ↓
build/prebuild
      ↓
string local
      ↓
HTML_TEMPLATE
      ↓
WebView
```

### 4.3 Recursos generados

```text
src/reader/engines/webview/generated/
├── epubjsSource.ts
├── jszipSource.ts
└── bridgeClientSource.ts
```

Ejemplo de representación:

```typescript
export const EPUBJS_SOURCE = `...`;
```

### 4.4 Flujo de integración

```text
assets/fixtures/lab-book.epub
              │
              ▼
       EPUBWebView.tsx
              │
              │ INIT_BOOK
              │ {
              │   bookId,
              │   fileUri: data URI local,
              │   format: "epub",
              │   initialLocation?
              │ }
              ▼
          WebView
              │
              ├── JSZip local
              ├── epub.js local
              └── bridge-client local
                       │
                       ▼
                    ePub()
                       │
                       ▼
                 EPUB rendition
                       │
                       ├── READER_READY
                       ├── LOCATION_CHANGED
                       ├── PAGE_CHANGED
                       ├── CHAPTER_ENDED
                       ├── SELECTION_CLEARED
                       └── BOOK_ERROR
```
