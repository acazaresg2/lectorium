**DOCUMENTO TÉCNICO DE TRANSFERENCIA Y RESUMEN EJECUTIVO**

**Proyecto: Aplicación móvil Local-First para aprendizaje de idiomas mediante lectura**

Versión consolidada para inicio de generación de código con Codex\
Fecha de corte: 24 de agosto de 2026

**\
ESTADO ACTUAL\**
Pasos 1-2 del roadmap completados. El Paso 3 es el siguiente paso de implementación.
\
Reader Contract V1 es la única fuente de verdad técnica del lector.

# 0. Resumen ejecutivo {#resumen-ejecutivo}

Este documento reemplaza el condensado anterior como documento de transferencia. Su objetivo es proporcionar a otro modelo de IA, a Codex y a cualquier desarrollador una única referencia coherente del proyecto, sin decisiones duplicadas ni bloques de código incompatibles.

La aplicación será multiplataforma (Android e iOS), compatible con celular y tablet, y estará orientada al aprendizaje de idiomas mediante lectura progresiva. V1 será Local-First y no requerirá cuenta, servidor ni sincronización en la nube.

La arquitectura del lector queda gobernada por Reader Contract V1 v1.0. Los prototipos anteriores quedan subordinados a dicho contrato: cuando exista cualquier diferencia entre un prototipo histórico y esta especificación, el prototipo se considera obsoleto y debe corregirse.

| **Elemento** | **Estado actual** | **Fuente de verdad** |
|----|----|----|
| Definición de producto | Cerrada | Este documento |
| Arquitectura Local-First | Cerrada | Este documento |
| Reader Contract V1 | Cerrado v1.0 | Reader Contract V1, sección 4 |
| Proyecto Expo | Creado | Repositorio real |
| Expo Router + TypeScript | Configurado | Repositorio real |
| Git + GitHub | Configurados / Vinculado | Repositorio real |
| Estructura canónica del proyecto | Creado | Repositorio real |
| EPUB de laboratorio | Pendiente / siguiente paso | Fixture del proyecto |
| Prototipo EPUB + WebView + epub.js | Bloqueado por Paso 3 | Código del repositorio |
| ReaderBridge integrado | Bloqueado por Paso 4 | Roadmap, paso 5 |
| Selección + contexto | Pendiente | Roadmap, paso 6 |
| Persistencia CFI | Pendiente | Roadmap, paso 7 |
| TXTEngine | Pendiente | Roadmap, paso 8 |

# 1. Objetivo principal del proyecto {#objetivo-principal-del-proyecto}

- Crear una biblioteca local de lecturas en EPUB y TXT exclusivamente. PDF queda fuera de V1.

- Incluir cuentos demo precargados por nivel Beginner, Elementary e Intermediate.

- Leer dentro de la aplicación y seleccionar palabras, frases o sentencias sin abandonar el lector.

- Mostrar traducciones y contexto de la selección mediante servicios desacoplados.

- Reproducir pronunciación mediante una abstracción de TTS.

- Guardar vocabulario y repasarlo mediante SuperMemo SM-2.

- Registrar lectura, progreso, XP, rachas y sesiones de estudio.

- Programar sesiones mediante calendario y notificaciones.

- Garantizar que la funcionalidad esencial opere sin Internet.

- Dejar V2/V3 preparadas sin introducir su complejidad en V1.

# 2. Principios rectores y reglas no negociables {#principios-rectores-y-reglas-no-negociables}

- Reader Contract V1 es la única fuente de verdad del protocolo del lector.

- No introducir nombres de comandos, eventos o payloads alternativos en el código.

- La UI no conoce epub.js, DOM ni detalles internos del EPUB.

- WebView no consulta SQLite, no llama servicios de traducción y no contiene lógica de negocio.

- ReaderBridge es la única frontera WebView ↔ React Native.

- Traducción y TTS se consumen mediante servicios desacoplados.

- No utilizar CDNs ni dependencias remotas para el runtime V1. Todas las bibliotecas requeridas para el lector deben ser locales y estar empaquetadas en la app.

- No almacenar claves secretas de APIs en la aplicación móvil.

- No depender de Internet para leer libros locales, reanudar progreso, consultar vocabulario guardado, operar estadísticas/calendario locales o usar el TTS del sistema cuando esté disponible.

- Usar UUIDv4 como PK TEXT. No usar IDs autoincrementales como PK.

- Las fechas se almacenan como TEXT ISO-8601, preferentemente UTC.

- Cada tabla tiene un Repository dedicado; ningún acceso directo a SQLite fuera de la capa de persistencia.

- No introducir V2/V3 antes de que V1 esté funcional, salvo interfaces/DTOs que no agreguen comportamiento innecesario.

- No introducir PDF ni EPUB con DRM salvo decisión explícita posterior.

# 3. Plataforma, repositorio y flujo de desarrollo {#plataforma-repositorio-y-flujo-de-desarrollo}

Stack acordado: Expo + React Native + TypeScript + Expo Router. El código fuente se mantiene en GitHub. Codex trabajará sobre el repositorio como fuente de verdad del código.

Expo Go se utilizará durante el desarrollo para ciclos rápidos cuando las capacidades utilizadas sean compatibles. Cuando una capacidad requiera un entorno nativo específico, se utilizará un Development Build/EAS sin cambiar la arquitectura del proyecto.

Flujo operativo recomendado: cambio pequeño → prueba local → validación en Expo → commit → push a GitHub → siguiente cambio.

# 4. Arquitectura global {#arquitectura-global}

App UI\
└── Features / Screens\
└── ReaderScreen\
└── ReaderController\
└── ReaderEngine\
├── EPUBEngine\
│ └── EPUBWebView\
│ └── ReaderBridge ↔ WebView Bundle\
└── TXTEngine\
\
Servicios desacoplados:\
TranslationService → LocalTranslationRepository / RemoteTranslationProvider\
SpeechService → expo-speech\
SRSService → SM-2\
FileStorageService → archivos físicos\
Repositories → SQLite\
NotificationService → expo-notifications\
AIService → placeholder de interfaz (V2/V3)

La dirección de dependencias es descendente. Ninguna capa inferior debe importar una capa superior. EPUBEngine puede conocer la implementación WebView; ReaderController no debe conocer epub.js. La UI solo usa el contrato del lector y servicios de aplicación.

# 5. Almacenamiento y modelo de datos {#almacenamiento-y-modelo-de-datos}

Los archivos EPUB/TXT se almacenan físicamente mediante expo-file-system. SQLite guarda metadatos, rutas, progreso, vocabulario, sesiones, estadísticas y configuración; no se almacena el binario completo del libro dentro de SQLite.

Todas las entidades sincronizables incorporan created_at, updated_at, deleted_at, sync_status y dirty cuando corresponda a su futura sincronización. Estos campos no implican que V1 sincronice nada: preparan el modelo para V3.

| **Versión** | **Tablas / entidades** |
|----|----|
| V1 | user_profile; user_languages; app_settings; books; book_progress; words; translations; flashcards; reading_sessions; user_statistics; study_goals; study_sessions |
| V2 | ai_explanations; learning_exercises; exercise_attempts; learning_recommendations |
| V3 | user_account; sync_queue; devices; ai_conversations; ai_messages |

Restricciones principales: user_languages UNIQUE(user_id, language_code); app_settings UNIQUE(setting_key); books UNIQUE(file_hash); book_progress UNIQUE(book_id); words UNIQUE(word, language_code); flashcards UNIQUE(translation_id); user_statistics UNIQUE(user_id, date).

# 6. Reader Contract V1 --- fuente de verdad única {#reader-contract-v1-fuente-de-verdad-única}

Reader Contract V1 v1.0 define exclusivamente el protocolo y los tipos que cruzan la frontera Native ↔ WebView. Cualquier código histórico que utilice LOAD_BOOK, GET_LOCATION, ADD_HIGHLIGHT, REMOVE_HIGHLIGHT, SET_HIGHLIGHTS, HIGHLIGHT_CLICKED o COMMAND_RESPONSE como parte del contrato V1 debe considerarse obsoleto y no debe reutilizarse.

## 6.1 Tipos canónicos {#tipos-canónicos}

export const PROTOCOL_VERSION = \'1.0\';\
\
export type ReaderLocation =\
\| {\
format: \'epub\';\
bookId: string;\
chapterIndex?: number;\
chapterTitle?: string;\
progressPercentage: number;\
totalChapters: number;\
cfi: string;\
}\
\| {\
format: \'txt\';\
bookId: string;\
chapterIndex?: number;\
chapterTitle?: string;\
progressPercentage: number;\
totalChapters: number;\
paragraphIndex: number;\
charOffset: number;\
};\
\
export interface SelectionRect {\
x: number;\
y: number;\
width: number;\
height: number;\
coordinateSpace: \'webview\';\
}\
\
export interface TextSelection {\
selectedText: string;\
rawText: string;\
selectionType: \'word\' \| \'phrase\' \| \'sentence\';\
sentenceContext: string;\
paragraphContext?: string;\
bookId: string;\
chapterIndex: number;\
location: ReaderLocation;\
range: { startOffset: number; endOffset: number };\
rect: SelectionRect;\
}\
\
export interface ReaderMessage\<T extends string, P\> {\
type: T;\
requestId: string;\
protocolVersion: string;\
payload: P;\
}

Semántica de requestId: en comandos Native → Web identifica la solicitud y permite correlación con la confirmación o timeout. En eventos espontáneos Web → Native actúa como eventId de trazabilidad. Los eventos no crean una solicitud pendiente ni esperan una respuesta.

protocolVersion es obligatorio en todos los mensajes. Un mismatch se reporta explícitamente con PROTOCOL_VERSION_MISMATCH y nunca se ignora silenciosamente.

## 6.2 Comandos Native → Web {#comandos-native-web}

| **Comando** | **Payload** | **Semántica** |
|----|----|----|
| INIT_BOOK | { bookId, fileUri, format, initialLocation? } | Carga/inicializa el libro local. |
| GO_TO_LOCATION | { location: ReaderLocation } | Navega a una ubicación persistente válida. |
| NAVIGATE_NEXT | {} | Avanza una unidad de navegación. |
| NAVIGATE_PREVIOUS | {} | Retrocede una unidad de navegación. |
| SET_FONT_SIZE | { fontSize: number } | Ajusta tamaño del texto. |
| SET_THEME | { theme: light \| dark \| sepia } | Aplica tema al lector. |
| CLEAR_SELECTION | {} | Limpia selección activa. |

## 6.3 Eventos Web → Native {#eventos-web-native}

| **Evento** | **Payload** | **Naturaleza** |
|----|----|----|
| READER_READY | { version: string } | Evento de ciclo de vida; no espera respuesta. |
| BOOK_ERROR | { code, message } | Error de lectura/renderizado/protocolo. |
| LOCATION_CHANGED | { location } | Evento espontáneo de ubicación. |
| PAGE_CHANGED | { location, pageIndex?, totalPages? } | Evento espontáneo de página. |
| TEXT_SELECTED | TextSelection | Evento espontáneo de selección. |
| SELECTION_CLEARED | {} | Evento espontáneo. |
| CHAPTER_ENDED | { location } | Evento espontáneo. |

## 6.4 Estados y errores {#estados-y-errores}

export type ReaderStatus =\
\| \'idle\'\
\| \'loading\'\
\| \'ready\'\
\| \'reading\'\
\| \'selecting\'\
\| \'translation_open\'\
\| \'paused\'\
\| \'error\';\
\
export const READER_ERROR_CODES = \[\
\'EPUB_LOAD_FAILED\',\
\'EPUB_INVALID\',\
\'EPUB_RENDER_FAILED\',\
\'TXT_LOAD_FAILED\',\
\'TXT_ENCODING_ERROR\',\
\'READER_INITIALIZATION_FAILED\',\
\'LOCATION_INVALID\',\
\'REQUEST_TIMEOUT\',\
\'PROTOCOL_VERSION_MISMATCH\',\
\] as const;

No se agrega PAGINATING como estado persistente. Es una actividad interna de renderizado.

## 6.5 Reglas de protocolo {#reglas-de-protocolo}

- El campo requestId es obligatorio y siempre es una cadena no vacía.

- Cada comando con expectativa de confirmación obtiene un requestId único generado por ReaderBridge.

- Los eventos espontáneos llevan un eventId en el mismo campo requestId; no existe respuesta implícita.

- Los mensajes con versión incompatible se rechazan con error explícito.

- ReaderBridge mantiene RequestTracker con timeout configurable para INIT_BOOK, GO_TO_LOCATION y navegación.

- La ubicación persistente es únicamente ReaderLocation. range.startOffset/endOffset no constituye ubicación persistente.

- rawText conserva el texto crudo del DOM; selectedText es su versión normalizada/trim sin alterar el contenido lingüístico.

- La selección no guarda vocabulario automáticamente. Guardar requiere acción explícita del usuario.

- No existe HIGHLIGHT_WORD en V1.

- La paginación horizontal es la preferida, pero la elección final queda sujeta a validación en el prototipo.

# 7. Implementación EPUB y WebView {#implementación-epub-y-webview}

EPUB se renderiza dentro de react-native-webview usando epub.js. JSZip y epub.js deben existir como assets locales del proyecto y sus contenidos se inyectan en el HTML del WebView. El runtime no contiene referencias http(s) a CDNs ni fallback remoto.

assets/\
libs/\
epub.min.js\
jszip.min.js\
fixtures/\
lab-book.epub\
demo-books/\
beginner/\
elementary/\
intermediate/\
\
src/reader/engines/webview/epub-webview-bundle/\
index.html\
bridge-client.ts\
selection-handler.ts // cuando corresponda al paso 6

El bundle del WebView se compone a partir de strings/recursos locales. El HTML final debe contener, en este orden conceptual: HTML base → JSZip local → epub.js local → bridge client local → handlers locales necesarios. No se usa \<script src=\"https://\...\"\>.

const finalHtml = HTML_TEMPLATE\
.replace(\'/\* JSZIP_PLACEHOLDER \*/\', jszipSource)\
.replace(\'/\* EPUBJS_PLACEHOLDER \*/\', epubSource)\
.replace(\'/\* BRIDGE_CLIENT_PLACEHOLDER \*/\', bridgeClientSource);\
\
\<WebView\
source={{ html: finalHtml, baseUrl: \'\' }}\
javaScriptEnabled\
domStorageEnabled\
scrollEnabled={false}\
onMessage={handleMessage}\
/\>

Para el prototipo actual, el EPUB puede transportarse temporalmente como Base64 mediante INIT_BOOK para aislar el riesgo de integración. Esta decisión queda limitada al flujo de prototipo y debe validarse para libros grandes antes de convertirla en comportamiento definitivo de producción.

# 8. ReaderBridge --- especificación de implementación {#readerbridge-especificación-de-implementación}

class ReaderBridge {\
// 1. Mantiene referencia al WebView.\
// 2. Genera requestId para comandos.\
// 3. Registra PendingRequest en RequestTracker.\
// 4. Encola comandos mientras el WebView no está listo.\
// 5. Envía JSON por postMessage().\
// 6. Resuelve/rechaza por la confirmación correlacionada.\
// 7. Expone suscripciones a eventos espontáneos.\
// 8. Limpia listeners y timeouts al desmontarse.\
}

La implementación concreta puede utilizar una cola y un RequestTracker separados como archivos internos, pero no puede cambiar la semántica del contrato. ReaderBridge no es un bus general de la aplicación: su única responsabilidad es la frontera del lector.

# 9. Selección y contexto --- paso 6 pendiente {#selección-y-contexto-paso-6-pendiente}

La selección se realizará dentro del WebView mediante DOM Range / window.getSelection() y se enviará como TextSelection. No se envolverá cada palabra con \<span\> por defecto.

El handler debe calcular selectedText, rawText, selectionType, sentenceContext, paragraphContext y SelectionRect. Debe evitar duplicados mediante debounce. La estrategia definitiva de CFI de rango persistente queda fuera del contrato V1 y se resolverá únicamente cuando el paso 7 lo requiera.

Stub permitido para Codex:

export interface SelectionHandler {\
attach(): void;\
detach(): void;\
setBookContext(bookId: string, chapterIndex: number): void;\
}\
\
// TODO(step-6): implementar extracción DOM y contexto.\
// El archivo puede compilar aunque el comportamiento real aún no exista.

# 10. Persistencia de progreso y CFI --- paso 7 pendiente {#persistencia-de-progreso-y-cfi-paso-7-pendiente}

La persistencia se ejecutará mediante debounce/throttle y nunca en cada scroll. Los disparadores son: cambio significativo de ubicación, cambio de capítulo/página, app a background, desmontaje del lector y cierre del libro.

EPUB persistirá cfi como ubicación primaria. TXT utilizará una representación específica que se definirá durante el paso 8. range.startOffset/endOffset nunca sustituye a ReaderLocation.

export interface ProgressPersistence {\
save(location: ReaderLocation, extra?: { readingTimeSeconds?: number }): Promise\<void\>;\
flush(): Promise\<void\>;\
}\
\
// TODO(step-7): conectar con BookProgressRepository y ciclo de vida de la app.

# 11. TXTEngine --- siguiente fase después del bridge {#txtengine-siguiente-fase-después-del-bridge}

TXTEngine es deliberadamente un módulo posterior. Debe normalizar UTF-8, UTF-16, BOM, Windows-1252 y otras codificaciones comunes, y aceptar saltos de línea \n, \r\n y variantes.

El tipo ReaderLocation para TXT ya está definido. La representación persistente final de charOffset/paragraphIndex deberá validarse durante este paso y quedar documentada antes de integrarse a producción.

export interface TXTEngineContract {\
load(uri: string): Promise\<void\>;\
getLocation(): ReaderLocation;\
goToLocation(location: Extract\<ReaderLocation, { format: \'txt\' }\>): Promise\<void\>;\
next(): Promise\<void\>;\
previous(): Promise\<void\>;\
}\
\
// TODO(step-8): implementar normalización y estrategia de persistencia TXT.

# 12. Servicios de aplicación {#servicios-de-aplicación}

## 12.1 TranslationService {#translationservice}

V1 requiere un servicio mínimo. El lector no conoce proveedores ni repositorios. La implementación se compone de TranslationService → LocalTranslationRepository y, cuando proceda, RemoteTranslationProvider. La traducción online es opcional y nunca rompe la lectura local.

export interface TranslationService {\
translate(input: {\
text: string;\
sourceLanguage: string;\
targetLanguage: string;\
context?: string;\
}): Promise\<TranslationResult\[\]\>;\
}

## 12.2 SpeechService {#speechservice}

export interface SpeechService {\
speak(text: string, language: string): Promise\<void\>;\
stop(): Promise\<void\>;\
}\
\
// Implementación V1: adapter sobre expo-speech.\
// La disponibilidad real de voces depende del sistema operativo.

## 12.3 AIService {#aiservice}

AIService es únicamente una interfaz/placeholder en V1. No se implementa lógica de IA ni llamadas a proveedores en el cliente. Cuando exista IA, el flujo será App → AI Service → Backend/API → proveedor de IA. Nunca se embeben claves secretas en la app.

export interface AIService {\
explain?:(input: unknown) =\> Promise\<unknown\>;\
contextualTranslate?:(input: unknown) =\> Promise\<unknown\>;\
}\
\
// V1: adapter stub. No-op o implementación que lance\
// un error controlado de funcionalidad no disponible.

# 13. Módulos funcionales V1 {#módulos-funcionales-v1}

| **Módulo** | **Diseño** |
|----|----|
| SRS | SuperMemo SM-2. Estados: new, learning, review, mastered. |
| Calendario | react-native-big-calendar sugerido; día/semana/mes; objetivos recurrentes. |
| Notificaciones | expo-notifications para sesiones programadas. |
| Biblioteca | Importación y gestión local de EPUB/TXT. |
| Onboarding | Bienvenida → nombre → avatar opcional → idioma origen → idioma objetivo → nivel → biblioteca → demos. |
| Estadísticas | Sesiones, progreso, XP y racha en almacenamiento local. |
| Idiomas | V1: español (es) como origen e inglés (en) como objetivo; arquitectura abierta a múltiples idiomas. |

# 14. Estructura canónica de carpetas {#estructura-canónica-de-carpetas}

app/\
\_layout.tsx\
index.tsx\
onboarding/\
welcome.tsx\
name.tsx\
languages.tsx\
level.tsx\
(tabs)/\
library/index.tsx\
vocabulary/index.tsx\
calendar/index.tsx\
stats/index.tsx\
profile/index.tsx\
vocabulary/review.tsx\
reader/\[bookId\].tsx\
\
src/\
reader/\
ReaderScreen.tsx\
ReaderController.ts\
ReaderEngine.ts\
engines/\
EPUBEngine.ts\
TXTEngine.ts\
webview/\
EPUBWebView.tsx\
epub-webview-bundle/\
index.html\
bridge-client.ts\
selection-handler.ts\
TXTRenderer.tsx\
bridge/\
ReaderBridge.ts\
messages.ts\
requestTracker.ts\
state/\
readerState.ts\
readerUIState.ts\
types/\
ReaderLocation.ts\
TextSelection.ts\
SelectionRect.ts\
persistence/\
progressPersistence.ts\
\
translation/\
TranslationPanel/\
TranslationPanel.tsx\
TranslationPanel.mobile.tsx\
TranslationPanel.tablet.tsx\
useTranslationPanelState.ts\
TranslationService.ts\
providers/\
LocalTranslationRepository.ts\
RemoteTranslationProvider.ts\
types.ts\
\
speech/SpeechService.ts\
ai/AIService.ts\
db/\
client.ts\
migrations/\
001_v1_schema.ts\
002_v2_schema.ts\
003_v3_schema.ts\
repositories/\
\...un Repository por tabla V1\...\
files/FileStorageService.ts\
srs/{sm2.ts,SRSService.ts}\
features/{library,vocabulary,calendar,stats,profile,onboarding}/\
notifications/NotificationService.ts\
shared/{components,hooks,theme,utils/{uuid.ts,dates.ts,encoding.ts}}\
types/domain.ts\
config/{env.ts,constants.ts}\
\
assets/\
libs/{epub.min.js,jszip.min.js}\
fixtures/lab-book.epub\
demo-books/{beginner,elementary,intermediate}/

Regla clave: app/ contiene rutas de Expo Router. La lógica de negocio vive en src/. Solo src/reader conoce detalles específicos de epub.js/WebView, y únicamente dentro de su subárbol.

# 15. EPUB de laboratorio {#epub-de-laboratorio}

El fixture permanente The Lost Key · La llave perdida contiene tres capítulos y cubre títulos, párrafos, diálogos, cursivas, negritas, enlaces, palabras con guiones, puntuación, apóstrofes, caracteres acentuados y ñ, imágenes, listas y estructuras HTML variadas.

Debe empaquetarse como EPUB válido con mimetype sin compresión. Antes de considerarlo fixture estable, debe validarse con una herramienta de validación EPUB.

# 16. Roadmap de implementación {#roadmap-de-implementación}

| **Paso** | **Estado** | **Alcance** |
|----|----|----|
| 1\. Reader Contract V1 | COMPLETADO | Contrato v1.0 cerrado. |
| 2\. Proyecto Expo + estructura | COMPLETADO | Implementación de carpetas app/, src/, assets/ y tsconfig.json. |
| 3\. EPUB de laboratorio | SIGUIENTE | Fixture local permanente. |
| 4\. Prototipo técnico mínimo | BLOQUEADO POR PASO 3 | Expo + RN + WebView + epub.js con dependencias locales; prueba de renderizado. |
| 5\. ReaderBridge | BLOQUEADO POR PASO 4 | Implementar bridge según contrato único, RequestTracker, timeout, versión y eventos. |
| 6\. Selección + contexto | BLOQUEADO | TextSelection, SelectionRect, contexto y limpieza de selección. |
| 7\. CFI + persistencia | BLOQUEADO | BookProgressRepository, persistencia de EPUB y ciclo de vida. |
| 8\. TXTEngine | PENDIENTE | Codificaciones, párrafos, offsets y persistencia TXT. |
| 9\. TranslationPanel | PENDIENTE | Primero TranslationService mínimo; luego UI nativa. |
| 10\. TTS | PENDIENTE | SpeechService + expo-speech. |
| 11\. Resto de V1 | PENDIENTE | SRS, calendario, estadísticas, XP/racha, notificaciones, onboarding y demos. |

# 17. Estrategia de trabajo con Codex {#estrategia-de-trabajo-con-codex}

Codex debe trabajar por tareas pequeñas, verificables y alineadas al contrato. No debe recibir como instrucción genérica construir toda la aplicación.

Cada tarea enviada a Codex debe indicar explícitamente los siguientes campos:
1. **Objetivo:** Qué se va a construir en la tarea actual.
2. **Paso del roadmap:** A qué paso específico pertenece.
3. **Archivos que puede crear o modificar:** Alcance delimitado de archivos y directorios permitidos.
4. **Archivos que NO debe modificar:** Archivos protegidos de configuración, documentación o componentes de otros pasos.
5. **Criterios de terminado:** Condiciones obligatorias para considerar finalizada la tarea.
6. **Validaciones que debe ejecutar:** Pruebas y verificaciones de compilación o ejecución.
7. **Resultado esperado:** Informe final de cambios y commit exclusivo en Git.


### Ejemplo y plantilla canónica de tarea para Codex

- **Objetivo:** Implementar exclusivamente las funcionalidades requeridas por el paso actual.
- **Paso del roadmap:** [Número y nombre del paso actual].
- **Fuente de verdad:** `PROJECT_SPEC.md` (especialmente Reader Contract V1, sección 6) y `docs/PROJECT_CONTEXT.md`.
- **Archivos que puede crear o modificar:** [Lista explícita de archivos o carpetas permitidas].
- **Archivos que NO debe modificar:** `PROJECT_SPEC.md`, `docs/PROJECT_CONTEXT.md`, ni nombres de comandos/eventos o payloads contractuales.
- **Restricciones y reglas de desarrollo:**
  - No avanzar automáticamente al siguiente paso del roadmap ni introducir funcionalidades de pasos posteriores (como SQLite, IA, traducción, TTS o highlights).
  - No introducir dependencias remotas o CDNs.
  - Si encuentra una discrepancia entre el repositorio y esta especificación, debe reportarla antes de resolverla (salvo autorización explícita).
- **Criterios de terminado:** El código compila sin errores de TypeScript, cumple estrictamente con el paso asignado y no deja código o dependencias huérfanas.
- **Validaciones que debe ejecutar:** Ejecutar verificaciones de sintaxis, compilación de TypeScript y resolución de rutas en Expo Router.
- **Resultado esperado:** Un commit exclusivo y verificado en Git para el paso actual, junto con un informe que detalle: archivos creados/modificados, dependencias tocadas, comandos ejecutados y resultados de las validaciones.

# 18. Criterios de consistencia antes de avanzar {#criterios-de-consistencia-antes-de-avanzar}

- No existen referencias a LOAD_BOOK en el proyecto.

- No existen comandos GET_LOCATION, ADD_HIGHLIGHT, REMOVE_HIGHLIGHT o SET_HIGHLIGHTS en Reader Contract V1.

- No existe COMMAND_RESPONSE como evento contractual; la correlación se resuelve mediante requestId dentro del mecanismo de respuesta definido por Bridge, sin ampliar el conjunto de eventos V1.

- No existe \<script src=\"http(s)://\...\"\> en el bundle del lector.

- epub.js y jszip proceden de assets locales.

- Todos los mensajes del protocolo incluyen requestId y protocolVersion.

- La semántica de requestId coincide entre TypeScript, Bridge y bridge-client.

- ReaderLocation es la única ubicación persistente.

- El WebView no toca SQLite ni servicios de negocio.

- La estructura de directorios (app/, src/reader/, assets/libs/) existe físicamente en el repositorio.

- tsconfig.json está presente y valida la compilación TypeScript.

- La compilación puede continuar aunque un módulo futuro esté representado por una interfaz/stub compilable.

# 19. Pendientes formales y límites {#pendientes-formales-y-límites}

| **Tema** | **Situación** | **Regla** |
|----|----|----|
| TXT persistence | Pendiente | Resolver en paso 8; no bloquear el bridge actual. |
| CFI de rango de selección | Pendiente | No usar aproximaciones como ubicación persistente. |
| Highlights | Fuera de V1 | No agregar comandos al contrato V1. |
| AIService | Stub | Compila sin implementación funcional. |
| TTS offline completo | Depende del SO | SpeechService abstrae disponibilidad de voces. |
| Libros EPUB grandes | Validación pendiente | Base64 sirve para prototipo; validar estrategia de producción antes de consolidarla. |
| Paginación horizontal vs vertical | Validación de UX/prototipo | Preferencia inicial: horizontal; decisión final basada en pruebas. |

# 20. Instrucciones para cualquier IA o desarrollador que reciba este documento {#instrucciones-para-cualquier-ia-o-desarrollador-que-reciba-este-documento}

Este documento se debe tratar como el estado consolidado del proyecto a fecha 24 de agosto de 2026. La regla principal es no inferir que fragmentos históricos del documento anterior siguen vigentes. Los bloques marcados como ejemplo, stub o pendiente no constituyen funcionalidades implementadas.

Este documento constituye la fuente de verdad técnica del proyecto.

Antes de modificar el código:

1. Leer PROJECT_SPEC.md completo.
2. Leer docs/PROJECT_CONTEXT.md.
3. Identificar el estado actual del roadmap.
4. Respetar las dependencias y bloqueos establecidos.
5. No implementar funcionalidades pertenecientes a pasos posteriores.
6. No introducir dependencias, protocolos o arquitecturas que contradigan este documento sin autorización.

## Estado actual

El Paso 1 - Reader Contract V1 está completado.

El Paso 2 - Expo + estructura está completado.

El Paso 3 - EPUB de laboratorio es el siguiente paso oficial de implementación.

El Paso 4 - Prototipo técnico mínimo permanece bloqueado hasta completar y validar el Paso 3.

ReaderBridge y las funcionalidades posteriores no deben implementarse todavía.

# Apéndice A. Mapa de responsabilidades del lector {#apéndice-a.-mapa-de-responsabilidades-del-lector}

| **Componente** | **Responsabilidad** | **No debe hacer** |
|----|----|----|
| ReaderScreen | Composición visual del lector y UI. | Acceder a epub.js, DOM o SQLite directamente. |
| ReaderController | Coordinar acciones del usuario y estado del lector. | Manipular DOM o depender de detalles de WebView. |
| ReaderEngine | Interfaz común de lectura. | Exponer detalles internos de EPUB/TXT. |
| EPUBEngine | Adaptar ReaderEngine a EPUB/WebView. | Contener lógica de traducción o persistencia de negocio. |
| TXTEngine | Adaptar ReaderEngine a TXT. | Depender de epub.js. |
| EPUBWebView | Integrar WebView y bundle local. | Llamar SQLite o servicios de traducción. |
| ReaderBridge | Transportar mensajes y correlaciones. | Convertirse en bus general de la aplicación. |
| TranslationService | Resolver traducciones. | Manipular WebView directamente. |
| SpeechService | Abstraer TTS. | Conocer UI del lector. |
| Repositories | Persistencia SQLite. | Ser importados desde WebView. |
