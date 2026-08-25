# AGENTS.md — Lectorium

## 1. Rol

Este archivo define **cómo debe trabajar Codex** en Lectorium. No duplica la especificación técnica.

Fuentes de verdad:
1. `docs/PROJECT_SPEC.md` — autoridad global: producto, roadmap, estado, reglas no negociables y Reader Contract V1.
2. `docs/PROJECT_CONTEXT.md` — detalle técnico de los pasos 3 y 4.
3. `docs/INDEX.md` — mapa de navegación rápida e índice del sistema de registro.
4. Código del repositorio — estado físico actual.
5. `AGENTS.md` — reglas operativas de Codex.

Nunca inventes una solución para resolver contradicciones entre fuentes. Reporta la contradicción y detén la parte afectada.

## 2. Objetivo operativo

Trabaja con el **mínimo cambio necesario**:
- alcance exacto;
- pocos archivos;
- contexto sólo cuando sea relevante;
- validación suficiente;
- ningún trabajo futuro no solicitado.

No conviertas una tarea local en una refactorización general.

## 3. Ahorro de contexto y tokens

**No leas los documentos de especificación completos en cada tarea por defecto.**

Estrategia de localización:
1. Consulta primero `docs/INDEX.md` para identificar la sección exacta requerida.
2. Abre únicamente los archivos y secciones indicados por el índice.

Lectura dirigida por paso:
- Consultar la sección "3. Mapeo Rápido por Paso del Roadmap" en `docs/INDEX.md`.

Primero localiza en `docs/INDEX.md`; después lee la sección exacta. No recorras todo el repositorio sin motivo.
No repitas búsquedas ni lecturas que ya resolvieron la misma pregunta dentro del turno.

## 4. Estado y orden del roadmap

Estado de corte: 25-08-2026.

- Paso 1 — Reader Contract V1: COMPLETADO.
- Paso 2 — Expo + estructura: COMPLETADO.
- Paso 3 — EPUB de laboratorio: COMPLETADO.
- Paso 4 — prototipo técnico mínimo: SIGUIENTE.
- Paso 5+ — no implementar todavía.

Orden:
`4 → 5 → 6 → 7 → 8 → 9 → 10 → 11`

Nunca adelantes funcionalidades de pasos posteriores aunque parezcan necesarias.

## 5. Reader Contract V1

`Reader Contract V1 v1.0` es la **única fuente de verdad** del protocolo Native ↔ WebView (ubicado en `docs/PROJECT_SPEC.md` §6).

No reintroducir ni crear equivalentes de:
`LOAD_BOOK`, `GET_LOCATION`, `ADD_HIGHLIGHT`, `REMOVE_HIGHLIGHT`, `SET_HIGHLIGHTS`, `COMMAND_RESPONSE`, `HIGHLIGHT_CLICKED`.

Reglas esenciales:
- Todo mensaje: `type`, `requestId`, `protocolVersion`, `payload`.
- Native→Web: `requestId` correlaciona el comando.
- Web→Native espontáneo: `requestId` identifica el evento; no crea una solicitud pendiente.
- Versiones incompatibles → `PROTOCOL_VERSION_MISMATCH`.
- `ReaderLocation` es la única ubicación persistente.
- Los offsets de selección no sustituyen `ReaderLocation`.
- Seleccionar texto no guarda vocabulario automáticamente.
- No introducir highlights en V1.

Si una tarea modifica el contrato, consulta `docs/INDEX.md` y lee `docs/PROJECT_SPEC.md` §6 antes de tocar código.

## 6. Fronteras arquitectónicas

- `app/` → rutas/pantallas Expo Router.
- `src/` → lógica y componentes.
- `src/reader/` → implementación del lector.
- `ReaderScreen` → UI.
- `ReaderController` → coordinación.
- `ReaderEngine` → abstracción.
- `EPUBEngine` / `TXTEngine` → adaptadores.
- `ReaderBridge` → única frontera Native ↔ WebView.
- Repositories → única vía a SQLite.

Nunca:
- UI → `epub.js`, DOM o SQLite.
- WebView → SQLite o servicios de negocio.
- `ReaderBridge` → convertirse en bus general.
- capas inferiores → importar capas superiores.
- WebView → lógica de traducción/TTS/persistencia de negocio.

## 7. Local-First

Runtime V1 no depende de red para la lectura local.

Prohibido:
- CDN;
- `<script src="http://...">`;
- `<script src="https://...">`;
- fallback remoto;
- secretos/API keys embebidos.

Para EPUB:
- `assets/libs/epub.min.js` local;
- `assets/libs/jszip.min.js` local;
- inyección local dentro del HTML;
- nunca carga remota.

## 8. Paso 3 — EPUB de laboratorio

Objetivo: generar y validar `assets/fixtures/lab-book.epub`.

Fuente detallada:
- Consultar `docs/INDEX.md` §3 (Paso 3) para abrir las secciones correspondientes en `docs/PROJECT_CONTEXT.md` y `docs/PROJECT_SPEC.md`.

Generación:
```bash
python3 scripts/build-lab-epub.py

```

Fuentes desempaquetadas: `scripts/lab-book-source/`.

Antes de terminar:

* fixture creado en la ruta correcta (`assets/fixtures/lab-book.epub`);
* `mimetype` primero y sin compresión;
* todos los recursos requeridos presentes;
* EPUB válido;
* validación EPUB ejecutada si existe herramienta disponible.

No rediseñar el fixture ni cambiar su cobertura sin autorización.

## 9. Paso 4 — prototipo mínimo

Objetivo: Expo + RN + WebView + `epub.js`/JSZip locales.

Fuente detallada:

* Consultar `docs/INDEX.md` §3 (Paso 4) para abrir las secciones correspondientes en `docs/PROJECT_CONTEXT.md` y `docs/PROJECT_SPEC.md`.

Reglas del prototipo:

* HTML local;
* `epub.js` y JSZip inyectados localmente;
* EPUB leído desde almacenamiento local;
* transporte temporal mediante `INIT_BOOK.fileUri` con data URI Base64;
* no crear `base64Data`;
* no crear comandos alternativos de carga;
* `SelectionHandler` real → Paso 6;
* `ReaderBridge` completo → Paso 5.

## 10. Flujo de cada tarea

Antes:

1. Identificar paso del roadmap.
2. Consultar `docs/INDEX.md` para ubicar las secciones necesarias.
3. Identificar archivos permitidos/protegidos.
4. Leer sólo la documentación necesaria en `docs/`.
5. Inspeccionar código existente y dependencias directas.

Durante:

* tocar sólo el alcance;
* no cambiar nombres contractuales;
* no adelantar pasos;
* no añadir dependencias innecesarias;
* no refactorizar código no relacionado.

Después:

1. Ejecutar validaciones aplicables.
2. Revisar `git diff`.
3. Revisar `git status`.
4. Confirmar ausencia de artefactos accidentales.

## 11. Validación eficiente

Valida primero lo directamente afectado y amplía sólo cuando sea necesario.

Usa los scripts/comandos reales del repositorio. No inventes comandos.

Ejemplos, sólo si están disponibles y son pertinentes:

```bash
npx tsc --noEmit
npx expo-doctor

```

Si una validación no puede ejecutarse, informa el comando y la causa. Nunca simules un resultado.

## 12. Archivos protegidos

No modificar automáticamente:

* `docs/INDEX.md`
* `docs/PROJECT_SPEC.md`
* `docs/PROJECT_CONTEXT.md`
* Reader Contract V1 / tipos contractuales
* configuración no relacionada;
* código de pasos futuros.

Si código y documentación difieren, reporta la discrepancia en vez de corregirla por intuición.

## 13. Stubs y pendientes

Un stub documentado es válido.

No adelantar automáticamente:

* `SelectionHandler` → Paso 6;
* `ProgressPersistence` → Paso 7;
* `TXTEngine` → Paso 8;
* `AIService` → placeholder;
* servicios futuros → lógica funcional.

Una interfaz existente no significa que su implementación esté desbloqueada.

## 14. Git

Cuando la tarea requiera commit:

* un commit = una tarea lógica;
* no mezclar pasos;
* revisar diff antes del commit;
* revisar status después;
* no reescribir commits existentes salvo instrucción explícita.

## 15. Criterios de terminado

La tarea termina cuando:

* objetivo exacto cumplido;
* alcance no ampliado;
* roadmap respetado;
* Reader Contract respetado;
* dependencias locales respetadas;
* validaciones aplicables ejecutadas;
* no existen cambios accidentales.

Informe final:

* qué cambió;
* archivos afectados;
* validaciones y resultados;
* limitaciones;
* commit, si correspondía.

## 16. Regla de parada

Detente y solicita decisión explícita cuando:

* exista conflicto entre fuentes de verdad;
* haya que alterar Reader Contract V1;
* haya que saltar un bloqueo;
* haya que introducir una dependencia remota;
* haya que modificar archivos protegidos fuera del alcance;
* no pueda determinarse el criterio de terminado.

## 17. Principio

`consultar docs/INDEX.md → localizar → leer lo necesario → cambiar poco → validar → revisar diff → terminar`

