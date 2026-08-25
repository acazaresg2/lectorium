# Índices del Sistema de Registro (System of Record Index)

Este documento es un índice de navegación de alta velocidad para Codex y desarrolladores. Permite localizar la información requerida sin necesidad de escanear `PROJECT_SPEC.md` ni `PROJECT_CONTEXT.md` en su totalidad.

---

## 1. Índice de `PROJECT_SPEC.md` (Especificación Global)

| Tema / Dominio | Sección en `PROJECT_SPEC.md` |
| :--- | :--- |
| **Resumen Ejecutivo y Estado Actual** | `## 0. Resumen ejecutivo` |
| **Objetivos del Producto V1** | `## 1. Objetivo principal del proyecto` |
| **Reglas No Negociables / Arquitectura General** | `## 2. Principios rectores y reglas no negociables` |
| **Stack, Repositorio y Entorno (Expo Router)** | `## 3. Plataforma, repositorio y flujo de desarrollo` |
| **Diagrama y Capas de Arquitectura Global** | `## 4. Arquitectura global` |
| **Esquema SQLite, Modelos de Datos y Entidades** | `## 5. Almacenamiento y modelo de datos` |
| **Reader Contract V1 (Fuente Única de Verdad Protocolo)** | `## 6. Reader Contract V1 --- fuente de verdad única` |
| -- *Tipos Canónicos (`ReaderLocation`, `TextSelection`)* | `#### 6.1 Tipos canónicos` |
| -- *Comandos Native → Web* | `#### 6.2 Comandos Native → Web` |
| -- *Eventos Web → Native* | `#### 6.3 Eventos Web → Native` |
| -- *Estados del Lector y Códigos de Error* | `#### 6.4 Estados y errores` |
| -- *Reglas de Protocolo (`requestId`, `protocolVersion`)* | `#### 6.5 Reglas de protocolo` |
| **Implementación EPUB y Inyección de WebView** | `## 7. Implementación EPUB y WebView` |
| **Especificación Técnica de `ReaderBridge`** | `## 8. ReaderBridge --- especificación de implementación` |
| **Especificación de Selección y Contexto (Paso 6)** | `## 9. Selección y contexto --- paso 6 pendiente` |
| **Persistencia de Progreso y CFI (Paso 7)** | `## 10. Persistencia de progreso y CFI --- paso 7 pendiente` |
| **Motor de Archivos de Texto TXT (Paso 8)** | `## 11. TXTEngine --- siguiente fase después del bridge` |
| **Servicios de Aplicación (`Translation`, `Speech`, `AI`)** | `## 12. Servicios de aplicación` |
| **Módulos Funcionales V1 (SRS, Calendario, Onboarding)** | `## 13. Módulos funcionales V1` |
| **Estructura Canónica de Directorios (`app/` y `src/`)** | `## 14. Estructura canónica de carpetas` |
| **Especificación del EPUB de Laboratorio** | `## 15. EPUB de laboratorio` |
| **Roadmap Consolidado de Pasos (1 al 11)** | `## 16. Roadmap de implementación` |
| **Estrategia de Trabajo y Plantilla para Codex** | `## 17. Estrategia de trabajo con Codex` |
| **Criterios de Consistencia Pre-implementación** | `## 18. Criterios de consistencia antes de avanzar` |
| **Límites Técnicos y Temas Pendientes Formales** | `## 19. Pendientes formales y límites` |
| **Instrucciones de Contexto para Agentes e IA** | `## 20. Instrucciones para cualquier IA o desarrollador...` |
| **Mapa de Responsabilidades por Componente** | `## Apéndice A. Mapa de responsabilidades del lector` |

---

## 2. Índice de `PROJECT_CONTEXT.md` (Detalle Técnico Pasos 3 y 4)

| Tema / Dominio | Sección en `PROJECT_CONTEXT.md` |
| :--- | :--- |
| **Reglas Generales y Lista Corta del Protocolo** | `## 1. REGLAS GENERALES Y ARQUITECTURA` |
| **Paso 3: Guía y Estructura EPUB de Laboratorio** | `## 2. PASO 3 — EPUB DE LABORATORIO` |
| -- *Estructura de Carpetas Fixture y Fuentes* | `### 2.1 Estructura del Fixture` & `### 2.2 Estructura fuente` |
| -- *Especificación `mimetype` y `container.xml`* | `### 2.3 mimetype` & `### 2.4 META-INF/container.xml` |
| **Paso 4: Guía de Implementación Prototipo Mínimo** | `## 3. PASO 4 — PROTOTIPO TÉCNICO MÍNIMO` |

---

## 3. Mapeo Rápido por Paso del Roadmap

Para minimizar consumo de tokens según el paso actual de desarrollo:

- **Paso 3 (EPUB de Laboratorio):** Consultar únicamente `PROJECT_CONTEXT.md` §2 y `PROJECT_SPEC.md` §15.
- **Paso 4 (Prototipo Mínimo WebView):** Consultar `PROJECT_CONTEXT.md` §1, §3 y `PROJECT_SPEC.md` §6, §7.
- **Paso 5 (ReaderBridge):** Consultar `PROJECT_SPEC.md` §6, §8.
- **Paso 6 (Selección + Contexto):** Consultar `PROJECT_SPEC.md` §6.1, §9.
- **Paso 7 (Persistencia CFI):** Consultar `PROJECT_SPEC.md` §5, §10.
- **Paso 8 (TXTEngine):** Consultar `PROJECT_SPEC.md` §11.
- **Paso 9 (Traducción):** Consultar `PROJECT_SPEC.md` §12.1.
- **Paso 10 (TTS / Pronunciación):** Consultar `PROJECT_SPEC.md` §12.2.
