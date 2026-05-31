# Plan Técnico de Implementación
## Dashboard de Análisis de Contenido con Claude Code
### Basado en: "Cómo crear tu propio dashboard de análisis de contenido con Claude Code"

---

# Diagnóstico inicial del documento

## Completitud del documento para convertirlo en software

| Dimensión | Estado | Detalle |
|-----------|--------|---------|
| Objetivo del producto | ✅ Completo | Dashboard local multi-plataforma (IG + YT opcional) con generación de ideas via IA |
| Actores | ✅ Completo | Un solo usuario (creadora de contenido); Claude Code como agente constructor |
| Stack tecnológico | ✅ Completo y detallado | Python, Streamlit, Plotly, SQLite, Anthropic API, Zernio |
| Endpoints de la API externa | ✅ Completo | 12 endpoints Zernio documentados con paths exactos y gotchas |
| Esquema de base de datos | ✅ Completo | 18 tablas con DDL parcial para las más críticas |
| Layout del dashboard | ✅ Completo | 7 pestañas con especificación de contenido |
| Sistema de ideas | ✅ Muy detallado | Distribución, buckets, pre-filters, system prompt literal, schema JSON |
| Fases de implementación | ✅ Completo | 10 fases explícitas (Phase 1–10) con tareas concretas |
| Reglas de negocio | ✅ Completo | Políticas de retención, gotchas críticos, restricciones read-only |
| Testing/validación | ✅ Checklist de aceptación | 12 ítems verificables |
| Autenticación/seguridad | ⚠️ Parcial | Solo API keys en .env; sin gestión de secretos avanzada |
| Despliegue/infra | ✅ Local únicamente | No hay despliegue en nube, es local por diseño |
| Manejo de errores | ✅ Tabla de troubleshooting | 7 errores documentados con solución |
| Personalización post-MVP | ✅ Listada | Ejemplos de extensiones posibles |

## Qué se puede construir con seguridad (>75% de confianza)

- ✅ Toda la estructura de archivos y módulos
- ✅ Schema SQLite completo (18 tablas)
- ✅ Cliente Zernio con los 12 endpoints verificados
- ✅ Sistema de pre-filtrado de comentarios/DMs (patrones literales dados)
- ✅ Sistema de ideas con los 3 buckets y el system prompt literal
- ✅ Dashboard de 7 pestañas con Streamlit
- ✅ Loop de descarte con aprendizaje
- ✅ Políticas de retención por tabla

## Qué requiere validación humana antes de construir

- ⚠️ `ZERNIO_ACCOUNT_ID` — se obtiene automáticamente via API pero depende de cuenta activa
- ⚠️ Add-ons Analytics e Inbox en Zernio — prerrequisito externo, no automatizable
- ⚠️ Nombres del bot/programas específicos del usuario para `BOT_PATTERNS`
- ⚠️ Timezone del usuario
- ⚠️ Si tiene YouTube conectado

## Nivel de confianza general del análisis

**95%** — El documento contiene instrucciones literales para Claude Code (sección "INSTRUCCIONES PARA CLAUDE CODE"), incluyendo DDL de tablas, paths de endpoints, patrones de código, system prompt literal, y fases de implementación. Es uno de los documentos funcionales más completos que puede usarse como base para un plan técnico.

---

# 1. Resumen técnico del producto

## Qué se va a construir

Un **dashboard web local de análisis de contenido para creadoras en Instagram y YouTube**, con las siguientes capacidades:

1. **Ingesta de datos** — Conexión a Zernio (intermediario oficial de Instagram/YouTube API) para obtener métricas, posts, comentarios y DMs.
2. **Caché local** — Base de datos SQLite local que almacena todos los datos con políticas de retención por tabla, garantizando privacidad total (ningún dato sensible sale del equipo).
3. **Dashboard analítico** — Interfaz Streamlit con 7 pestañas: resumen KPIs, tendencia temporal, demografía, grid de posts, heatmap de mejor hora, frecuencia de publicación, y generador de ideas.
4. **Generador de ideas con IA** — Motor que analiza comentarios, DMs y posts top, filtra ruido con heurísticas, y llama a Claude Sonnet via API para proponer ideas de contenido con evidencia real.
5. **Sistema de aprendizaje por descarte** — Cada idea descartada con su razón alimenta el contexto de la próxima generación, evitando repeticiones.

## Problema que resuelve

Las creadoras de contenido no tienen acceso fácil a sus datos de Instagram de forma consolidada, ni tienen un sistema que conecte esos datos con propuestas de contenido accionables basadas en lo que su audiencia realmente dice. Las herramientas SaaS existentes son caras, envían datos privados a terceros, y no generan ideas contextualizadas.

## Resultado final

Una aplicación local que corre en `http://localhost:8501`, que la creadora abre cada día para ver sus métricas, revisar el comportamiento de sus posts, y con un click generar 25 ideas de contenido ancladas en evidencia real de su audiencia. Tiempo de uso diario: ~40 segundos.

---

# 2. Interpretación técnica del procedimiento funcional

| Fase funcional (PDF) | Objetivo funcional | Traducción técnica | Componentes afectados | Entrada | Salida | Confianza |
|---------------------|-------------------|-------------------|----------------------|---------|--------|-----------|
| Setup de cuentas — Zernio | Conectar fuente de datos Instagram/YouTube | Obtener y persistir `ZERNIO_ACCOUNT_ID` via `GET /v1/accounts?platform=instagram` | `zernio_client.py`, `.env` | API Key Zernio | Account ID guardado en `.env` | Alta |
| Setup de cuentas — Anthropic | Habilitar generación de ideas | Configurar `ANTHROPIC_API_KEY` en `.env` con `load_dotenv(override=True)` | `.env`, `ideas.py` | API Key Anthropic | Variable de entorno disponible en runtime | Alta |
| Instalar Claude Code | Agente de construcción | No es parte del software a construir; es el harness de desarrollo | N/A — meta-fase | N/A | Claude Code operativo | Alta |
| Build asistido — Phase 1 Setup | Configurar proyecto | Crear `.env`, preguntar keys y timezone, auto-fetch account IDs | `zernio_client.py`, `.env` | API keys del usuario | `.env` poblado, IDs verificados | Alta |
| Build — Phase 2 Estructura | Scaffolding del proyecto | Crear estructura de carpetas, `venv`, `requirements.txt` con versiones pinned | Todos los archivos | N/A | Proyecto inicializado, dependencias instaladas | Alta |
| Build — Phase 3 Cliente Zernio | Capa de acceso a datos externos | Implementar `zernio_client.py` con 12 endpoints + retry/backoff exponencial | `zernio_client.py` | API Key + Account ID | JSON responses de Zernio cacheables | Alta |
| Build — Phase 4 Cache SQLite | Persistencia local | Crear 18 tablas con DDL, migraciones idempotentes, writers/readers | `cache.py`, `data.nosync/cache.db` | JSON de Zernio | Tablas SQLite pobladas | Alta |
| Build — Phase 5 Refresh | Orquestación de ingesta | Script CLI que llama todos los endpoints y persiste en SQLite | `refresh.py`, `zernio_client.py`, `cache.py` | Trigger manual o botón UI | Cache actualizado, `refresh_log` registrado | Alta |
| Build — Phase 6 Pre-filter | Limpieza de señal para IA | Funciones regex que filtran comentarios/DMs triviales antes de enviar a Claude | `idea_filters.py` | Lista de comentarios/DMs raw | Lista filtrada de contenido sustantivo | Alta |
| Build — Phase 7 Dashboard UI | Interfaz de usuario | App Streamlit con 7 tabs, header, selector de plataforma | `app.py` | SQLite cache | HTML renderizado en `localhost:8501` | Alta |
| Build — Phase 8 Sistema de ideas | Generación de ideas con IA | Llamadas a Claude Sonnet con prompt caching, 3 buckets, cards con 3 bloques | `ideas.py`, `prompts/ideas_system.md` | Comentarios/DMs/posts filtrados | JSON de ideas con `evidence_quotes`, `why_good_idea`, `suggested_angle` | Alta |
| Build — Phase 9 Validación | QA end-to-end | Checklist de 12 puntos, test de generación y descarte | `app.py`, `ideas.py` | Dashboard en ejecución | Checklist completado sin errores | Alta |
| Build — Phase 10 Documentación | Trazabilidad | `README.md` + `CLAUDE.md` para memoria de sesiones futuras | `README.md`, `CLAUDE.md` | Código implementado | Documentación usable | Alta |
| Uso diario — Refrescar | Actualizar datos | Botón "Refrescar datos" en UI o `python refresh.py` en CLI | `refresh.py`, `app.py` | Trigger del usuario | Cache actualizado (~30s) | Alta |
| Uso diario — Generar ideas | Propuesta de contenido con IA | Click en "Generar todas las ideas", llamada a Claude con contexto cacheado | `ideas.py`, `app.py` | Cache de posts/comentarios/DMs | 25 ideas (IG) o 20 (YT) con evidencia | Alta |
| Uso diario — Descartar ideas | Aprendizaje por feedback | Modal de descarte → `INSERT idea_discards` → `UPDATE ideas SET discarded=1` | `app.py`, `cache.py` | Razón de descarte | Idea marcada, historial disponible para próxima generación | Alta |
| Personalización | Extensibilidad | Nuevas funciones via Claude Code en sesiones futuras | Cualquier módulo | Petición en lenguaje natural | Feature implementada incrementalmente | Media |
| Add-on transcripciones | Enriquecimiento de contexto | `yt-dlp` + Whisper local; integración via subprocess con tabla `transcriptions` | Script externo, `cache.py`, `ideas.py` | URL de reel/video | Texto de transcripción en SQLite | Media (opcional) |

---

# 3. Arquitectura técnica recomendada

## Diagrama de componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                    EQUIPO LOCAL DEL USUARIO                       │
│                                                                   │
│  ┌──────────────┐    ┌──────────────────────────────────────┐    │
│  │   USUARIO    │───▶│         STREAMLIT UI (app.py)         │    │
│  │  Navegador   │    │   7 Tabs + Header + Selector Plataforma│    │
│  │ localhost:   │◀───│                                       │    │
│  │    8501      │    └───────────────────┬──────────────────┘    │
│  └──────────────┘                        │                        │
│                               ┌──────────┼──────────┐            │
│                               ▼          ▼          ▼            │
│                    ┌──────────────┐ ┌──────────┐ ┌──────────┐   │
│                    │  cache.py    │ │ideas.py  │ │refresh.py│   │
│                    │  SQLite I/O  │ │Claude AI │ │  CLI     │   │
│                    └──────┬───────┘ └────┬─────┘ └────┬─────┘   │
│                           │              │             │          │
│                    ┌──────▼───────┐      │    ┌───────▼──────┐  │
│                    │ data.nosync/ │      │    │zernio_client │  │
│                    │  cache.db    │      │    │ 12 endpoints │  │
│                    │  18 tablas   │◀─────┘    └──────┬───────┘  │
│                    └──────────────┘                   │          │
│                                         ┌─────────────┼──────┐  │
│                    ┌──────────────┐      │ idea_filters │  │   │  │
│                    │prompts/      │      │ ADORATION_   │  │   │  │
│                    │ideas_system  │      │ BOT_PATTERNS │  │   │  │
│                    │.md (literal) │      └─────────────┘  │   │  │
│                    └──────────────┘                        │   │  │
└────────────────────────────────────────────────────────────┼───┘
                                                             │
            ┌────────────────────────────────────────────────┼────┐
            │              SERVICIOS EXTERNOS                 │    │
            │                                                 │    │
            │  ┌─────────────────────┐    ┌──────────────────▼──┐ │
            │  │   ANTHROPIC API     │    │   ZERNIO API        │ │
            │  │ claude-sonnet-4-5   │◀───│ api.zernio.com/v1   │ │
            │  │ Generación de ideas │    │ Datos IG + YT       │ │
            │  │ Prompt caching      │    │ (intermediario       │ │
            │  └─────────────────────┘    │  oficial API)        │ │
            │                             └─────────────────────┘ │
            └──────────────────────────────────────────────────────┘
```

## Componentes y clasificación (obligatorio vs. recomendado)

| Capa | Componente | Obligatorio según PDF | Justificación |
|------|-----------|----------------------|---------------|
| Frontend | Streamlit 1.39+ con 7 tabs | ✅ Obligatorio | Especificado explícitamente |
| Gráficos | Plotly 5.24 | ✅ Obligatorio | Pinned en stack |
| Backend/orquestación | Python 3.9+ con venv | ✅ Obligatorio | Especificado con venv en `.venv/` |
| Motor IA | Claude Sonnet 4.5 via Anthropic API | ✅ Obligatorio | Para generación de ideas |
| Almacenamiento | SQLite 18 tablas en `data.nosync/` | ✅ Obligatorio | DDL dado literalmente |
| API externa | Zernio (12 endpoints) | ✅ Obligatorio | Única fuente de datos IG/YT |
| Pre-filtrado | `idea_filters.py` con regex | ✅ Obligatorio | Patrones dados literalmente |
| Prompt caching | `cache_control: ephemeral` | ✅ Obligatorio | Explícito en sección de ideas |
| Retry/backoff | Exponencial (2s,3s,5s,9s) | ✅ Obligatorio | Gotcha crítico #8 |
| Configuración | `.env` con `load_dotenv(override=True)` | ✅ Obligatorio | Gotcha crítico #1 |
| Documentación | `README.md` + `CLAUDE.md` | ✅ Obligatorio | Phase 10 explícita |
| Testing | `streamlit.testing.v1.AppTest` | ✅ Obligatorio | Phase 7 explícita |
| Add-on transcripciones | yt-dlp + Whisper | ⚠️ Opcional | Solo si el usuario lo pide post-MVP |
| Backup automático | JSON antes de DELETE | ✅ Obligatorio | Gotcha crítico #4 |
| Migración idempotente | PRAGMA table_info | ✅ Obligatorio | Gotcha crítico #3 |

---

# 4. Stack tecnológico recomendado

## Stack completo con versiones pinned

| Categoría | Tecnología | Versión | Justificación |
|-----------|-----------|---------|---------------|
| Lenguaje | Python | 3.9+ | Especificado. Usa `zoneinfo` stdlib (disponible desde 3.9) |
| UI/Frontend | Streamlit | 1.39.x | Pinned — en 1.40 cambia `use_container_width` en `st.image` (gotcha #6) |
| Gráficos | Plotly | 5.24.x | Pinned — compatibilidad con Streamlit 1.39 |
| HTTP client | requests | 2.32.x | Cliente para Zernio API |
| SDK IA | anthropic | 0.97.0 | Pinned — versiones antiguas pelean con httpx 0.27 (gotcha #5) |
| HTTP async | httpx | 0.28.1 | Pinned — necesario para evitar bug de proxies en SDK viejo (gotcha #5) |
| Base de datos | SQLite3 | stdlib | Cero dependencias externas, local, portátil |
| Config | python-dotenv | 1.0.1 | Con `override=True` obligatorio (gotcha #1) |
| Timezones | zoneinfo | stdlib | Conversión UTC → TZ local del usuario para heatmaps |
| Testing UI | streamlit.testing.v1 | Con Streamlit 1.39 | `AppTest` para validar arranque sin excepciones |
| Linting | flake8 / ruff | última | **Supuesto técnico recomendado** — no especificado en doc |
| VCS | git | cualquiera | Implícito por `.gitignore` presente |
| Package manager | pip + venv | stdlib | Especificado: `venv` en `.venv/` |

## `requirements.txt` recomendado (versiones pinned)

```
streamlit==1.39.0
plotly==5.24.0
requests==2.32.3
anthropic==0.97.0
httpx==0.28.1
python-dotenv==1.0.1
```

---

# 5. Diseño modular del software

## Módulo 1: `zernio_client.py` — Cliente API Zernio

| Campo | Detalle |
|-------|---------|
| Responsabilidad | Wrapper de todos los endpoints de Zernio con retry/backoff y manejo de errores HTTP |
| Entradas | `ZERNIO_API_KEY`, `ZERNIO_ACCOUNT_ID`, parámetros de cada endpoint |
| Salidas | JSON response parseado por función |
| Funciones principales | `list_accounts()`, `get_account_health()`, `get_daily_metrics()`, `get_best_time_to_post()`, `get_posting_frequency()`, `get_content_decay()`, `list_inbox_comments()`, `get_post_comments()`, `get_usage_stats()`, `get_account_insights()`, `get_demographics()`, `get_follower_history()`, `list_conversations()`, `get_conversation_messages()`, `get_youtube_channel_insights()`, `get_youtube_demographics()`, `get_youtube_daily_views()` |
| Dependencias | `requests`, `.env`, `time` (para backoff) |
| Riesgos técnicos | 402/403 si add-ons no activos; token IG expirado; `/v1/analytics` con bug (no usar) |
| Pruebas necesarias | Test de cada endpoint con mocks; test de retry en 5xx; test de 402 handling |

## Módulo 2: `cache.py` — Capa de persistencia SQLite

| Campo | Detalle |
|-------|---------|
| Responsabilidad | Crear/migrar 18 tablas, escribir datos de Zernio, leer datos para dashboard e ideas |
| Entradas | JSON de `zernio_client.py` |
| Salidas | Datos leídos como dicts/listas para otros módulos |
| Funciones principales | `init_db()`, `migrate_idempotent()`, writers por tabla, readers por tabla, `backup_before_delete()` |
| Dependencias | `sqlite3` stdlib, `json`, `datetime` |
| Riesgos técnicos | Migración no idempotente revienta en segunda ejecución (gotcha #3); iCloud puede evaporar cache.db si no está en `data.nosync/` |
| Pruebas necesarias | Test de migración idempotente (ejecutar `init_db()` dos veces sin error); test de upsert para `follower_history`; test de rolling delete para `comments` |

## Módulo 3: `refresh.py` — Orquestador de ingesta

| Campo | Detalle |
|-------|---------|
| Responsabilidad | Script CLI que llama todos los endpoints Zernio en orden y persiste en SQLite; registra en `refresh_log` |
| Entradas | Variables de entorno (API keys, account IDs, timezone) |
| Salidas | SQLite actualizado; log en `refresh_log` table |
| Funciones principales | `refresh_instagram()`, `refresh_youtube()`, `main()` |
| Dependencias | `zernio_client.py`, `cache.py`, `python-dotenv` |
| Riesgos técnicos | Falla parcial (algunos endpoints ok, otros 402/403) — debe continuar y loggear, no abortar todo |
| Pruebas necesarias | Test de ejecución completa; test de falla parcial (mock 402 en demographics, verificar que resto sigue) |

## Módulo 4: `idea_filters.py` — Pre-filtrado de comentarios/DMs

| Campo | Detalle |
|-------|---------|
| Responsabilidad | Filtrar comentarios y DMs triviales (adulación, bots, vacíos) antes de enviar a Claude |
| Entradas | Lista de strings (comentarios o DMs raw) |
| Salidas | Lista filtrada de strings sustantivos |
| Funciones principales | `is_substantive_comment(text, min_len=20)`, `is_substantive_dm(text, min_len=15)`, `is_likely_bot_message(text)` |
| Patrones literales | `ADORATION_PATTERNS` (52 entradas), `BOT_PATTERNS` (32+ entradas), `URL_RE`, `EMAIL_ONLY_RE` |
| Dependencias | `re` stdlib |
| Riesgos técnicos | Over-filtering puede dejar pocos comentarios válidos; under-filtering manda ruido a Claude (aumenta costo) |
| Pruebas necesarias | Test con cada patrón de ADORATION; test con BOT_PATTERNS; test con comentarios sustantivos reales (no deben filtrarse) |

## Módulo 5: `ideas.py` — Generación de ideas con IA

| Campo | Detalle |
|-------|---------|
| Responsabilidad | Llamadas a Claude Sonnet con prompt caching, manejo de 3 buckets, persistencia de ideas, loop de aprendizaje por descarte |
| Entradas | Datos del cache (posts, comentarios, DMs filtrados, demografía, descartes recientes) |
| Salidas | Lista de ideas con `evidence_quotes`, `why_good_idea`, `suggested_angle`, `basis_*_ids` |
| Funciones principales | `generate_all_ideas_ig()`, `generate_all_ideas_yt()`, `generate_bucket(platform, bucket)`, `discard_idea(idea_id, reason_quick, reason_text)` |
| Dependencias | `anthropic==0.97.0`, `cache.py`, `idea_filters.py`, `prompts/ideas_system.md` |
| Riesgos técnicos | Output >16K tokens si se piden 25 ideas (cap a `max_tokens=16000`); descartes en bloque cacheado invalidan cache (mantenerlos en bloque NO cacheado); ID leak en texto (strip defensivo en `app.py`) |
| Pruebas necesarias | Test de parse JSON válido; test de strip de IDs; test de que descartes van en bloque no cacheado; test de retry en 529 |

## Módulo 6: `app.py` — Dashboard Streamlit

| Campo | Detalle |
|-------|---------|
| Responsabilidad | Interfaz completa de 7 tabs + header + selector de plataforma; renderizado de ideas con cards de 3 bloques; modal de descarte |
| Entradas | SQLite cache (read); acciones del usuario (botones, radios, clicks) |
| Salidas | HTML/JS en `localhost:8501`; writes a SQLite via `cache.py` e `ideas.py` |
| Funciones principales | `render_header()`, `render_tab_resumen()`, `render_tab_tendencia()`, `render_tab_audiencia()`, `render_tab_posts()`, `render_tab_cuando_publicar()`, `render_tab_frecuencia()`, `render_tab_ideas()`, `render_idea_card()`, `render_discard_modal()` |
| Dependencias | Todos los demás módulos, `streamlit==1.39.0`, `plotly==5.24.0` |
| Riesgos técnicos | `use_container_width` en `st.image` no disponible en 1.39 (usar `use_column_width=True`); Streamlit rerun en cada interacción puede ser lento con SQLite grande |
| Pruebas necesarias | `AppTest` que verifica arranque sin excepciones; test de que botón "Refrescar" llama a refresh; test visual manual de checklist de aceptación |

## Módulo 7: `prompts/ideas_system.md` — System prompt

| Campo | Detalle |
|-------|---------|
| Responsabilidad | Contener LITERALMENTE el system prompt calibrado para generación de ideas |
| Entradas | N/A (archivo estático) |
| Salidas | Texto que se inyecta como system message en llamadas a Claude |
| Riesgos técnicos | Cualquier paráfrasis o modificación degrada la calidad de las ideas; archivo debe ser copiado verbatim del PDF |
| Pruebas necesarias | Diff contra el texto del PDF para verificar que no hay cambios |

---

# 6. Plan técnico por fases

## Fase 1: Setup inicial — Configuración de cuentas y entorno

### Objetivo técnico
Tener el entorno Python inicializado, las API keys configuradas en `.env`, y los `ZERNIO_ACCOUNT_ID` obtenidos automáticamente (sin que el usuario corra curl manualmente).

### Tareas de software

- [ ] Crear carpeta `dashboard-instagram/` en `~/Projects/`
- [ ] Crear `venv` en `.venv/` con `python -m venv .venv`
- [ ] Implementar función `fetch_account_id(api_key, platform)` en `zernio_client.py` que llama `GET /v1/accounts?platform={platform}` y extrae `_id` del primer resultado
- [ ] Preguntar al usuario: API key Zernio, API key Anthropic, timezone, ¿tiene YouTube?
- [ ] Auto-fetch `ZERNIO_ACCOUNT_ID` y `ZERNIO_ACCOUNT_ID_YOUTUBE` (si aplica)
- [ ] Crear `.env` con todos los valores
- [ ] Crear `.env.example` con valores placeholder
- [ ] Crear `.gitignore` con `.env`, `data.nosync/`, `__pycache__/`, `.venv/`
- [ ] Crear carpeta `data.nosync/` (vacía, para cache.db)
- [ ] Instalar dependencias: `pip install streamlit==1.39.0 plotly==5.24.0 requests==2.32.3 anthropic==0.97.0 httpx==0.28.1 python-dotenv==1.0.1`
- [ ] Crear `requirements.txt` con versiones pinned

### Archivos a crear

```
dashboard-instagram/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── data.nosync/        (carpeta vacía)
```

### Criterios de aceptación

- `.env` contiene `ZERNIO_API_KEY`, `ZERNIO_ACCOUNT_ID`, `ANTHROPIC_API_KEY`, `DASHBOARD_TZ`
- `ZERNIO_ACCOUNT_ID` fue obtenido automáticamente via API (no manual)
- `pip install -r requirements.txt` termina sin errores
- `.env` no aparece en git (verificado con `git status`)

### Pruebas necesarias

- **Manual**: Verificar que `.env` tiene los 4+ valores esperados
- **Manual**: `python -c "from dotenv import load_dotenv; load_dotenv(override=True); import os; print(os.getenv('ZERNIO_API_KEY'))"` devuelve la key
- **Integración**: `curl -H "Authorization: Bearer {ZERNIO_API_KEY}" https://api.zernio.com/v1/accounts?platform=instagram` devuelve 200 con `_id`

### Prompt para OpenCode

```
Tenemos un nuevo proyecto llamado dashboard-instagram. Tu primera tarea es:

1. Crear la carpeta ~/Projects/dashboard-instagram/ si no existe
2. Dentro, crear un venv en .venv/ con: python3 -m venv .venv
3. Implementar en zernio_client.py una función fetch_account_id(api_key, platform) que:
   - Llame GET https://api.zernio.com/v1/accounts?platform={platform}
   - Use header Authorization: Bearer {api_key}
   - Retorne el campo _id del primer elemento del JSON response
   - Si la respuesta no es 200, lance una excepción con el status code
4. Preguntar al usuario en el chat: su ZERNIO_API_KEY, ANTHROPIC_API_KEY, timezone (ej: Europe/Madrid), y si tiene YouTube en Zernio (sí/no)
5. Usando las keys proporcionadas, llamar fetch_account_id para instagram. Si tiene YT, llamarlo también para youtube.
6. Crear .env con:
   ZERNIO_API_KEY=<la que dio el usuario>
   ZERNIO_ACCOUNT_ID=<el que obtuviste automáticamente>
   ZERNIO_ACCOUNT_ID_YOUTUBE=<si aplica, vacío si no>
   ANTHROPIC_API_KEY=<la que dio el usuario>
   DASHBOARD_TZ=<la que dio el usuario>
7. Crear .env.example con los mismos campos pero valores placeholder
8. Crear .gitignore con: .env, data.nosync/, __pycache__/, .venv/
9. Crear requirements.txt con estas versiones exactas:
   streamlit==1.39.0
   plotly==5.24.0
   requests==2.32.3
   anthropic==0.97.0
   httpx==0.28.1
   python-dotenv==1.0.1
10. Instalar con: .venv/bin/pip install -r requirements.txt
11. Crear carpeta data.nosync/ vacía

Cuando termines, muéstrame el contenido de .env (con la API key truncada por seguridad) y confirma que pip install terminó sin errores.
```

---

## Fase 2: Estructura del proyecto — Scaffolding completo

### Objetivo técnico
Crear todos los archivos del proyecto con stubs vacíos o comentarios de placeholder, de modo que la estructura final exista desde el inicio y cada fase solo llene los archivos correspondientes.

### Tareas de software

- [ ] Crear `app.py` con imports y estructura de 7 tabs (stubs)
- [ ] Crear `refresh.py` con estructura principal (stub)
- [ ] Crear `zernio_client.py` con función `fetch_account_id` ya implementada + stubs para los 12 endpoints restantes
- [ ] Crear `cache.py` con stub de `init_db()`
- [ ] Crear `ideas.py` con stubs de las 3 funciones de generación
- [ ] Crear `idea_filters.py` con los patrones literales (ADORATION_PATTERNS y BOT_PATTERNS) como constantes — son el contenido más crítico
- [ ] Crear carpeta `prompts/` y archivo `prompts/ideas_system.md` con el system prompt LITERAL del PDF
- [ ] Crear `README.md` con placeholder

### Archivos a crear/modificar

```
dashboard-instagram/
├── app.py                    (stub con 7 tabs)
├── refresh.py                (stub)
├── zernio_client.py          (fetch_account_id implementado + stubs)
├── cache.py                  (stub init_db)
├── ideas.py                  (stubs generate_*)
├── idea_filters.py           (PATRONES LITERALES ya)
├── prompts/
│   └── ideas_system.md       (SYSTEM PROMPT LITERAL del PDF)
└── README.md                 (placeholder)
```

### Criterios de aceptación

- `python app.py` no lanza SyntaxError (aunque no haga nada aún)
- `prompts/ideas_system.md` contiene el system prompt sin modificaciones
- `idea_filters.py` contiene `ADORATION_PATTERNS` con las 52 entradas del PDF
- Estructura de carpetas completa

### Prompt para OpenCode

```
Vamos a crear el scaffolding completo de dashboard-instagram. No implementes la lógica todavía — solo crea los archivos con la estructura correcta:

1. app.py — Streamlit app con imports y 7 tabs vacíos:
   - Header (siempre visible)
   - Selector de plataforma (radio: Instagram | YouTube | Ambas)
   - Tab 1: Resumen
   - Tab 2: Tendencia
   - Tab 3: Audiencia
   - Tab 4: Posts
   - Tab 5: Cuándo publicar
   - Tab 6: Frecuencia
   - Tab 7: Ideas
   Cada tab puede tener un st.write("Tab X: en construcción") de placeholder.

2. refresh.py — Script con función main() que por ahora solo imprime "Refresh iniciado"

3. idea_filters.py — Este archivo ya debe tener los patrones COMPLETOS y LITERALES. Copia EXACTAMENTE estos patrones del PDF:
   [pega aquí el contenido de ADORATION_PATTERNS y BOT_PATTERNS del PDF]
   Implementa también las funciones is_substantive_comment, is_substantive_dm, is_likely_bot_message con la lógica descrita.

4. prompts/ideas_system.md — Copia LITERALMENTE el system prompt del PDF (la sección que empieza con "Eres un estratega de contenido senior..."). NO lo parafrasees ni lo modifiques en absoluto.

5. cache.py — Función init_db() que por ahora solo hace pass

6. ideas.py — Stubs de generate_all_ideas_ig(), generate_all_ideas_yt(), generate_bucket()

7. README.md — Placeholder con título "Dashboard Instagram" y sección "Cómo correr: pendiente"

Cuando termines, ejecuta: python -c "import app" y muéstrame que no hay SyntaxErrors.
```

---

## Fase 3: Cliente Zernio — Capa de acceso a datos externos

### Objetivo técnico
Implementar todos los endpoints de Zernio con retry/backoff exponencial. Validar cada endpoint contra la cuenta real del usuario antes de continuar.

### Tareas de software

- [ ] Implementar clase o módulo `ZernioClient` con autenticación Bearer
- [ ] Implementar función `_request(method, path, params)` con retry exponencial (2s, 3s, 5s, 9s) para 5xx y rate limits
- [ ] Implementar los 12 endpoints cross-platform:
  - `list_accounts(platform)` → `GET /accounts?platform=...`
  - `get_account_health(id)` → `GET /accounts/{id}/health`
  - `get_daily_metrics(account_id, platform)` → `GET /analytics/daily-metrics`
  - `get_best_time_to_post(account_id, platform)` → `GET /analytics/best-time` (**NO** `/best-time-to-post`)
  - `get_posting_frequency(account_id, platform)` → `GET /analytics/posting-frequency`
  - `get_content_decay(account_id, platform)` → `GET /analytics/content-decay`
  - `list_inbox_comments(account_id, platform)` → `GET /inbox/comments`
  - `get_post_comments(post_id, account_id)` → `GET /inbox/comments/{postId}?accountId=...`
  - `get_usage_stats(account_id)` → `GET /usage-stats` (**NO** `/usage`)
- [ ] Implementar los 5 endpoints Instagram-only:
  - `get_account_insights(account_id)` → `GET /analytics/instagram/account-insights`
  - `get_demographics(account_id)` → `GET /analytics/instagram/demographics`
  - `get_follower_history(account_id)` → `GET /analytics/instagram/follower-history`
  - `list_conversations(account_id)` → `GET /inbox/conversations`
  - `get_conversation_messages(conv_id, account_id)` → `GET /inbox/conversations/{id}/messages?accountId=...`
- [ ] Implementar los 3 endpoints YouTube-only (si el usuario tiene YT):
  - `get_youtube_channel_insights(account_id)` → `GET /analytics/youtube/channel-insights`
  - `get_youtube_demographics(account_id)` → `GET /analytics/youtube/demographics`
  - `get_youtube_daily_views(video_id, account_id)` → `GET /analytics/youtube/daily-views?videoId=...&accountId=...`
- [ ] Manejo específico de errores: 401 (key expirada), 402 (add-on requerido), 403 (inbox add-on), token IG expirado
- [ ] **NUNCA llamar**: `posts_create`, `posts_publish_now`, `messages_send_inbox_message` ni ningún endpoint de escritura
- [ ] **NUNCA llamar**: `/v1/analytics` directo (bug — devuelve 400)
- [ ] Validar cada endpoint con la cuenta real del usuario

### Criterios de aceptación

- Cada endpoint retorna JSON sin errores cuando los add-ons están activos
- Si un endpoint da 402/403, se muestra mensaje claro al usuario y se pausa (no se aborta todo)
- `_request()` hace retry automático en 5xx con backoff exponencial

### Prompt para OpenCode

```
Implementa zernio_client.py completo. Base URL: https://api.zernio.com/v1
Header en todas las requests: Authorization: Bearer {ZERNIO_API_KEY}

REGLA CRÍTICA: NO implementes ni menciones endpoints de escritura (posts_create, posts_publish_now, messages_send_inbox_message). Este cliente es 100% solo lectura.

OTRO BUG CRÍTICO: NO uses el path /v1/analytics — tiene un bug en Zernio y devuelve 400. Los paths correctos son los específicos como /analytics/daily-metrics, /analytics/instagram/account-insights, etc.

Implementa primero una función interna _request(method, path, params=None) con:
- Retry exponencial: espera 2s, 3s, 5s, 9s antes de reintentar en respuestas 5xx o 429
- Si recibe 401: lanza AuthError("API key expirada o inválida")
- Si recibe 402: lanza AddonRequiredError("Activa el add-on Analytics en zernio.com")
- Si recibe 403: lanza AddonRequiredError("Activa el add-on Inbox en zernio.com")
- Si recibe 200: retorna response.json()

Luego implementa estas funciones exactas (paths verificados del PDF):
[lista completa de 17 funciones con sus paths exactos]

Al final del archivo, añade una función validate_all_endpoints(zernio_api_key, account_id_ig, account_id_yt=None) que llame a cada endpoint y reporte cuáles funcionan y cuáles dan error. 

Carga las keys así (override=True obligatorio):
from dotenv import load_dotenv
load_dotenv(override=True)

Termina corriendo validate_all_endpoints con las keys del .env y muéstrame los resultados.
```

---

## Fase 4: Cache SQLite — Persistencia local

### Objetivo técnico
Implementar las 18 tablas con DDL correcto, migraciones idempotentes, y funciones read/write para cada tabla. Todo en `data.nosync/cache.db`.

### Tareas de software

- [ ] Implementar `init_db()` que crea las 18 tablas si no existen (usando `CREATE TABLE IF NOT EXISTS`)
- [ ] Implementar `migrate_idempotent()` que usa `PRAGMA table_info(tabla)` antes de cualquier `ALTER TABLE ADD COLUMN`
- [ ] Implementar `backup_before_delete(table_name)` que hace JSON dump antes de borrado destructivo
- [ ] Implementar writers para cada tabla según política de retención:
  - `posts`, `ideas`, `idea_discards`, `follower_history`: acumulativo con upsert
  - `comments`: rolling 90 días (DELETE WHERE date < now-90)
  - `messages`: rolling 30 días
  - `daily_metrics`: rolling 180 días
  - Resto: snapshot (DELETE + INSERT en cada refresh)
- [ ] DDL específico para `ideas` e `idea_discards` (dado literalmente en el PDF)
- [ ] DDL para las 16 tablas restantes basado en la descripción del PDF:
  - `meta`, `account_snapshot`, `account_health`, `account_insights_30d`, `youtube_channel_insights_daily`, `youtube_channel_totals_30d`, `daily_metrics`, `demographics_age`, `demographics_gender`, `demographics_country`, `demographics_city`, `posts`, `comments`, `conversations`, `messages`, `best_time`, `posting_frequency`, `content_decay`, `follower_history`, `refresh_log`, `transcriptions`

### Criterios de aceptación

- `init_db()` ejecutada 2 veces consecutivas sin error (idempotencia)
- `sqlite3 data.nosync/cache.db ".tables"` muestra las 18 tablas
- `ALTER TABLE ADD COLUMN` en segunda ejecución no falla gracias a PRAGMA check

### Prompt para OpenCode

```
Implementa cache.py con las 18 tablas de SQLite. La base de datos debe estar en data.nosync/cache.db

CRÍTICO — Gotcha #3 del PDF: Toda migración de columnas DEBE hacer PRAGMA table_info(tabla) primero y solo hacer ALTER TABLE ADD COLUMN si la columna no existe ya. Si no, la segunda ejecución falla.

CRÍTICO — Gotcha #4: Antes de cualquier DELETE masivo en migraciones, dump los datos a data.nosync/backup_{timestamp}.json

Las tablas críticas tienen DDL literal en el PDF:
[pega el DDL de ideas e idea_discards del PDF]

Para las demás tablas, inferirlas del contexto del PDF:
- meta: key TEXT PRIMARY KEY, value TEXT
- account_snapshot: id TEXT, platform TEXT, username TEXT, followers INTEGER, profile_pic_url TEXT, updated_at TEXT
- account_health: id TEXT, platform TEXT, status TEXT, checked_at TEXT
- daily_metrics: date TEXT, platform TEXT, reach INTEGER, views INTEGER, engagements INTEGER, ..., PRIMARY KEY (date, platform)
- posts: id TEXT PRIMARY KEY, platform TEXT, caption TEXT, permalink TEXT, thumbnail_url TEXT, likes INTEGER, comments_count INTEGER, saves INTEGER, shares INTEGER, reach INTEGER, timestamp TEXT
- comments: id TEXT PRIMARY KEY, post_id TEXT, platform TEXT, text TEXT, username TEXT, timestamp TEXT
- conversations: id TEXT PRIMARY KEY, account_id TEXT, last_message_at TEXT
- messages: id TEXT PRIMARY KEY, conversation_id TEXT, text TEXT, from_user TEXT, timestamp TEXT
- follower_history: date TEXT, platform TEXT, followers INTEGER, PRIMARY KEY (date, platform)
- refresh_log: id INTEGER PRIMARY KEY AUTOINCREMENT, started_at TEXT, finished_at TEXT, status TEXT, error TEXT
- [resto de tablas con estructura similar]

Políticas de retención por tabla:
- posts: todos (upsert)
- comments: rolling 90 días
- messages: rolling 30 días
- daily_metrics: rolling 180 días
- follower_history: acumulativo (upsert)
- ideas, idea_discards: acumulativo
- resto: snapshot (delete + insert en cada refresh)

Implementa writers y readers básicos para cada tabla. Al final, ejecuta init_db() dos veces y muestra que no hay error en la segunda ejecución.
```

---

## Fase 5: Refresh — Orquestación de ingesta

### Objetivo técnico
Script CLI y función reutilizable desde UI que actualiza todos los datos de Zernio en el cache local en ~30 segundos.

### Tareas de software

- [ ] Implementar `refresh_instagram(client, cache)` que llama todos los endpoints IG y persiste en SQLite
- [ ] Implementar `refresh_youtube(client, cache)` (si el usuario tiene YT)
- [ ] Implementar `main()` que orquesta ambos, registra en `refresh_log`, e imprime progreso
- [ ] Manejo de errores parciales: si un endpoint falla (402/403), loggear y continuar con los demás
- [ ] Usar `load_dotenv(override=True)` obligatorio
- [ ] Primer refresh real al finalizar esta fase

### Criterios de aceptación

- `python refresh.py` completa en <60s
- `sqlite3 data.nosync/cache.db "SELECT COUNT(*) FROM posts"` devuelve número >0
- `sqlite3 data.nosync/cache.db "SELECT COUNT(*) FROM comments"` devuelve número >0
- `refresh_log` tiene al menos 1 registro con status "ok"

### Prompt para OpenCode

```
Implementa refresh.py completo. Este script orquesta todas las llamadas a Zernio y persiste en SQLite.

OBLIGATORIO: load_dotenv(override=True) al inicio — explicación en gotcha #1 del PDF.

Estructura:
1. refresh_instagram(zernio_client, cache) — llama estos endpoints en orden:
   - get_account_health → guarda en account_health
   - get_account_insights → guarda en account_insights_30d  
   - get_daily_metrics → guarda con rolling 180d
   - get_demographics → guarda en demographics_age/gender/country/city
   - get_follower_history → upsert en follower_history
   - get_best_time_to_post → snapshot en best_time
   - get_posting_frequency → snapshot en posting_frequency
   - get_content_decay → snapshot en content_decay
   - list_inbox_comments → guarda en posts + comments con rolling 90d
   - list_conversations → guarda en conversations
   - Para cada conversación reciente: get_conversation_messages → guarda en messages con rolling 30d

2. refresh_youtube(zernio_client, cache) — solo si ZERNIO_ACCOUNT_ID_YOUTUBE no está vacío

3. main() que:
   - Marca inicio en refresh_log
   - Llama refresh_instagram, captura cualquier excepción por endpoint (loggea pero no aborta)
   - Si tiene YT: llama refresh_youtube
   - Marca fin en refresh_log con status ok o partial_error
   - Imprime resumen: X posts, Y comentarios, Z DMs actualizados

IMPORTANTE: Si un endpoint da 402/403, imprime el error al usuario y continúa con los demás (no abortar todo el refresh).

Al terminar la implementación, corre python refresh.py y muéstrame el output completo incluyendo los counts de filas en cada tabla.
```

---

## Fase 6: Pre-filtrado — Limpieza de señal

### Objetivo técnico
Tener `idea_filters.py` completamente funcional y validado contra los datos reales del usuario.

### Tareas de software

- [ ] Verificar que los patrones literales del PDF están copiados exactamente en `idea_filters.py`
- [ ] Implementar `is_substantive_comment(text, min_len=20)`:
  - False si solo emojis/puntuación
  - False si después de remover ADORATION queda <15 chars
  - True si tiene `?` o `¿`
- [ ] Implementar `is_substantive_dm(text, min_len=15)`:
  - Igual que comment pero min_len menor y filtro de bots
- [ ] Implementar `is_likely_bot_message(text)`:
  - True si match con BOT_PATTERNS
  - True si email-only (EMAIL_ONLY_RE)
  - True si URL con <20 chars adicionales
- [ ] Preguntar al usuario nombres de su bot y programas específicos para añadir a BOT_PATTERNS
- [ ] Test rápido sobre datos reales del usuario (imprimir % de comentarios filtrados)

### Criterios de aceptación

- Un comentario como "te amo eres mi ídola diosa" → False (filtrado)
- Un comentario como "¿cómo grabas el audio de tus reels?" → True (sustantivo)
- Un DM bot-like con "haz click aquí" → True para `is_likely_bot_message`
- Tasa de filtrado sobre datos reales entre 30-70% (si es >90% puede estar sobre-filtrando)

### Prompt para OpenCode

```
Vamos a validar y finalizar idea_filters.py. 

Primero, muéstrame los primeros 20 comentarios en la base de datos:
sqlite3 data.nosync/cache.db "SELECT text FROM comments LIMIT 20"

Luego ejecuta estos tests unitarios básicos:
from idea_filters import is_substantive_comment, is_likely_bot_message

# Deben dar False (filtrado):
print(is_substantive_comment("te amo eres mi ídola"))  # → False
print(is_substantive_comment("😍😍❤️❤️"))              # → False
print(is_substantive_comment("jajajaja"))               # → False

# Deben dar True (sustantivo):
print(is_substantive_comment("¿cómo grabas el audio?"))         # → True
print(is_substantive_comment("me gustaría aprender a editar de cero")) # → True

Ahora ejecuta el filtro sobre TODOS los comentarios reales de la base de datos e imprime:
- Total de comentarios
- Cuántos pasan el filtro (sustantivos)
- % de filtrado
- Ejemplos de los 5 comentarios filtrados más largos (para verificar no hay over-filtering)

Si el % filtrado es >90%, algo está mal. Muéstrame los comentarios filtrados para debuggear.

También pregunta al usuario: ¿Tu cuenta tiene algún bot de respuesta automática? Si sí, ¿cuál es el nombre y frases típicas que usa? Las añadiremos a BOT_PATTERNS.
```

---

## Fase 7: Dashboard UI — Interfaz Streamlit

### Objetivo técnico
Dashboard funcional con las 7 tabs mostrando datos reales del SQLite, navegable en el navegador.

### Tareas de software

- [ ] Implementar header (foto de perfil, username, followers, indicador de salud, botón refresh)
- [ ] Implementar selector de plataforma (radio: Instagram | YouTube | Ambas)
- [ ] Tab 1 "Resumen": KPIs IG (reach, views, engaged, interactions, likes, comments, saves, shares) + KPIs YT si aplica
- [ ] Tab 2 "Tendencia": gráfico Plotly de líneas con multi-select de métricas + crecimiento de seguidores
- [ ] Tab 3 "Audiencia": sub-pestañas IG/YT con 4 dimensiones (age/gender/country/city para IG, 3 para YT)
- [ ] Tab 4 "Posts": grid con thumbnails ordenable, click → modal con comentarios reales
- [ ] Tab 5 "Cuándo publicar": heatmaps con conversión UTC→TZ local del usuario
- [ ] Tab 6 "Frecuencia": scatter posts/semana vs engagement + content decay
- [ ] Tab 7 "Ideas": UI completa (descrita en Fase 8)
- [ ] Strip defensivo de IDs en app.py: `_ID_PATTERN_LONG`, `_ID_PATTERN_LABELED`, `_ID_PATTERN_BARE`
- [ ] `use_column_width=True` en `st.image` (NO `use_container_width` — gotcha #6)
- [ ] Test con `streamlit.testing.v1.AppTest` que verifica arranque sin excepciones

### Criterios de aceptación

- `streamlit run app.py` abre sin errores en `localhost:8501`
- Header muestra foto de perfil y número de followers real (comparar con Instagram)
- Cada tab muestra datos reales (no ceros, no placeholders)
- Grid de posts muestra thumbnails y click abre comentarios reales

### Prompt para OpenCode

```
Implementa app.py completo con las 7 tabs. Vamos tab por tab.

GOTCHA CRÍTICO #6: En st.image, usa use_column_width=True (NO use_container_width — ese parámetro entró en Streamlit 1.40 y aquí tenemos 1.39).

GOTCHA — Strip defensivo de IDs: En app.py, antes de renderizar cualquier texto de ideas, aplica estos patterns para remover IDs numéricos que Claude pueda haber colado:
_ID_PATTERN_LONG = re.compile(r"\b(post|comment|message)[\s_-]?id[:\s]*\d+\b", re.IGNORECASE)
_ID_PATTERN_LABELED = re.compile(r"\b(post|comment|message)\s+\d{10,}\b", re.IGNORECASE)
_ID_PATTERN_BARE = re.compile(r"\b\d{12,}\b")

GOTCHA — load_dotenv: load_dotenv(override=True) al inicio del archivo.

Implementa en este orden:
1. Header: foto de perfil (de account_snapshot), username, follower count, indicador de salud (verde/amarillo/rojo según account_health.status), "Última actualización: {refresh_log.finished_at}", botón "Refrescar datos" que llama refresh.main()

2. Selector global: st.radio("Plataforma:", ["Instagram", "YouTube", "Ambas"], horizontal=True)

3. Tab 1 — Resumen: KPIs en st.metric desde account_insights_30d para IG (reach, views, engaged, interactions, likes, comments, saves, shares). Si tiene YT: views, watch_hours, subs_neto.

4. Tab 2 — Tendencia: st.multiselect de métricas + gráfico Plotly líneas desde daily_metrics. Curva separada de follower_history.

5. Tab 3 — Audiencia: st.tabs(["Instagram", "YouTube"]). IG: 4 barras (age/gender/country/city). YT: 3 (sin city).

6. Tab 4 — Posts: grid de 3 columnas con thumbnails (st.image con use_column_width=True), botón "Ver comentarios" que abre st.expander con comentarios desde la tabla comments.

7. Tab 5 — Cuándo publicar: heatmap Plotly (day_of_week vs hour) desde best_time, con conversión UTC→TZ local via zoneinfo.

8. Tab 6 — Frecuencia: scatter Plotly posts/semana vs avg_engagement + barras de content_decay.

9. Tab 7 — Ideas: solo stub por ahora (st.write("Sistema de ideas — Fase 8"))

Al terminar, corre: python -m streamlit.testing.v1 app.py y muéstrame los resultados. Luego corre streamlit run app.py y dime la URL.
```

---

## Fase 8: Sistema de ideas — Generación con IA

### Objetivo técnico
Motor completo de generación de ideas con Claude Sonnet, prompt caching correcto, cards de 3 bloques, y loop de aprendizaje por descarte.

### Tareas de software

- [ ] Implementar `generate_all_ideas_ig()` — single call a Claude, distribución 10/5/10
- [ ] Implementar `generate_all_ideas_yt()` — single call, distribución 10/10 (sin DMs)
- [ ] Implementar `generate_bucket(platform, bucket)` — regenera un bucket específico
- [ ] Prompt caching correcto:
  - **Bloque cacheado** (`cache_control: ephemeral`): top posts, transcripts, comentarios sustantivos, DMs sustantivos, demografía, mejor hora
  - **Bloque NO cacheado**: instrucción específica + descartes recientes (últimos 50)
- [ ] `max_tokens=16000` (para 25 ideas con 3 bloques)
- [ ] Retry con backoff exponencial para 529 Overloaded
- [ ] Parse del JSON de respuesta de Claude
- [ ] Persistencia de ideas generadas en tabla `ideas`
- [ ] Función `discard_idea(idea_id, reason_quick, reason_text)`:
  - `INSERT INTO idea_discards`
  - `UPDATE ideas SET discarded=1`
- [ ] Carga del system prompt desde `prompts/ideas_system.md` (nunca hardcodeado)
- [ ] Contexto de descartes formateado para el bloque no cacheado
- [ ] UI en Tab 7:
  - Radio Instagram/YouTube
  - Botón "Generar todas las ideas de X"
  - 3 secciones expandibles por bucket con contador N/10
  - Cards con 3 bloques visuales (evidence_quotes, why_good_idea, suggested_angle)
  - Botón "✕ Descartar idea" → modal con razones
  - Sección "Últimos descartes" expandible

### Criterios de aceptación

- Click en "Generar todas las ideas de Instagram" produce ideas con los 3 bloques poblados
- Cada idea muestra cita verbatim, por qué es buena, y ángulo sugerido
- Descarte de una idea la hace desaparecer del panel
- Regenerar bucket no repite la idea descartada
- No aparecen IDs numéricos en el texto de las cards

### Prompt para OpenCode

```
Implementa ideas.py completo y el Tab 7 de app.py.

GOTCHA CRÍTICO #1: load_dotenv(override=True) al inicio de ideas.py.
GOTCHA CRÍTICO #5: usa anthropic==0.97.0 y httpx==0.28.1 (ya están en requirements.txt).
GOTCHA CRÍTICO #7: max_tokens=16000 para la llamada de 25 ideas.
GOTCHA CRÍTICO #8: retry con backoff 2s/3s/5s/9s para errores 5xx y 529 de Anthropic.

El system prompt se carga así (NO hardcodeado):
with open("prompts/ideas_system.md", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

Prompt caching — CRÍTICO:
- Bloque 1 (cacheado con cache_control ephemeral): contexto grande con top 20 posts con captions, últimos 500 comentarios sustantivos filtrados con idea_filters, últimos 200 DMs sustantivos, demografía top, mejor hora de publicación
- Bloque 2 (NO cacheado): instrucción "genera X ideas del bucket Y" + los últimos 50 descartes formateados como:
  ## Ideas que ya descartaste (NO repitas ni hagas variantes similares)
  - [bucket] "ángulo descartado" — razón: texto
  (esto va en el bloque NO cacheado para no invalidar el cache en cada descarte)

Implementa:
1. _build_cached_context(platform) → dict con contenido grande para cachear
2. _build_discard_context() → texto con últimos 50 descartes
3. generate_all_ideas_ig() → una llamada Claude, prompt para 10 comments + 5 dms + 10 top_content
4. generate_all_ideas_yt() → una llamada Claude, 10 comments + 10 top_content
5. generate_bucket(platform, bucket, n) → regenera un bucket específico
6. discard_idea(idea_id, reason_quick, reason_text) → INSERT + UPDATE

Para el Tab 7 en app.py, implementa:
- Radio plataforma
- Botón "Generar todas las ideas de Instagram" (o YouTube)
- Para cada bucket: st.expander(f"De comentarios — N ideas") con las cards
- Cada card muestra:
  st.markdown(f"**{idea['angle']}**")
  st.markdown("> " + "\n> ".join(idea['evidence_quotes']))
  st.markdown(f"**Por qué es buena idea:** {idea['why_good_idea']}")
  st.markdown(f"**Ángulo sugerido:** {idea['suggested_angle']}")
  if st.button(f"✕ Descartar", key=f"discard_{idea['id']}"):
      # abrir modal con razones
- Modal de descarte con opciones: "Tema cubierto / No me interesa / Muy básica / No es mi estilo / Otro"

Al terminar, ejecuta una generación real y muéstrame las primeras 3 ideas generadas.
```

---

## Fase 9: Validación end-to-end

### Objetivo técnico
Verificar el checklist completo de aceptación del PDF y resolver cualquier bug encontrado.

### Checklist de aceptación (del PDF, 12 puntos)

- [ ] El dashboard abre en http://localhost:8501 sin errores rojos
- [ ] En el header veo mi foto de perfil de IG
- [ ] El contador de followers es correcto (comparar con Instagram real)
- [ ] El indicador de salud está en verde
- [ ] Pestaña "Resumen 30 días" muestra números reales (no ceros)
- [ ] Pestaña "Posts" muestra grid con thumbnails de mis posts
- [ ] Click en "Ver comentarios" abre panel con comentarios reales
- [ ] Pestaña "Ideas" muestra radio "Instagram | YouTube"
- [ ] Botón "Generar todas las ideas" funciona sin errores
- [ ] Cada idea generada tiene 3 bloques: cita / por qué buena / ángulo sugerido
- [ ] Botón "✕ Descartar idea" abre modal con razones
- [ ] Después de descartar una idea, desaparece de la lista

### Prompt para OpenCode

```
Vamos a hacer la validación completa del dashboard. Lanza streamlit run app.py y verifica manualmente este checklist del PDF:

1. ¿Abre sin errores en localhost:8501?
2. ¿El header muestra foto de perfil?
3. ¿El contador de followers es correcto?
4. ¿El indicador de salud está en verde?
5. ¿La pestaña Resumen muestra números reales?
6. ¿La pestaña Posts muestra thumbnails?
7. ¿Click en "Ver comentarios" muestra comentarios reales?
8. ¿La pestaña Ideas tiene el radio Instagram/YouTube?
9. ¿El botón "Generar todas las ideas" funciona?
10. ¿Cada idea tiene los 3 bloques (cita / por qué buena / ángulo)?
11. ¿El botón "✕ Descartar" abre un modal?
12. ¿Después de descartar, la idea desaparece?

Para cada punto que falle: pega el error completo aquí y di "esto falló en el punto X".
Para errores de Streamlit: busca el traceback completo en la terminal donde corre el dashboard.
Para errores de API: busca en la consola del navegador (F12 → Console).

Cuando tengas todos los puntos en verde, dime "checklist completo" y pasamos a documentación.
```

---

## Fase 10: Documentación y CLAUDE.md

### Objetivo técnico
`README.md` funcional y `CLAUDE.md` que permite a Claude Code retomar el proyecto en futuras sesiones sin perder contexto.

### Tareas de software

- [ ] Escribir `README.md` con:
  - Prerrequisitos
  - Cómo instalar (paso a paso)
  - Cómo correr (`streamlit run app.py`)
  - Cómo refrescar datos (`python refresh.py` o botón UI)
  - Cómo generar ideas
  - Tabla de troubleshooting (del PDF)
- [ ] Escribir `CLAUDE.md` con:
  - Descripción del proyecto y su estado actual
  - Stack y versiones exactas
  - Gotchas críticos (los 8 del PDF)
  - Estructura de archivos con responsabilidad de cada uno
  - Endpoints Zernio verificados (los que funcionan y los que no)
  - Dónde está el system prompt y por qué no modificarlo
  - Historial de decisiones técnicas tomadas

### Prompt para OpenCode

```
Escribe README.md y CLAUDE.md para el proyecto dashboard-instagram.

README.md debe incluir:
- Qué es este proyecto (2-3 líneas)
- Prerrequisitos (Python 3.9+, cuenta Zernio con add-ons, API key Anthropic)
- Instalación paso a paso (clonar, crear venv, instalar, configurar .env)
- Cómo correr: .venv/bin/streamlit run app.py → abre localhost:8501
- Cómo refrescar datos: botón en UI o python refresh.py
- Cómo generar ideas: pestaña Ideas → botón Generar
- Tabla de troubleshooting exacta del PDF (los 7 errores con solución)
- Cómo personalizar con Claude Code (ejemplos del PDF)

CLAUDE.md es para que yo (Claude) recuerde el proyecto en próximas sesiones. Debe incluir:
- Propósito del proyecto
- Stack con versiones pinned
- Los 8 gotchas críticos (sin parafrasear, copiados tal cual del PDF o con sus soluciones implementadas)
- Estructura de archivos con una línea de descripción por archivo
- Endpoints Zernio: cuáles están verificados, cuáles tienen bugs conocidos (/v1/analytics), cuáles requieren add-ons
- Dónde está el system prompt (prompts/ideas_system.md) y la regla de NO modificarlo
- Política de retención de datos por tabla
- Última validación: fecha + checklist completado
```

---

# 7. Backlog técnico completo

| ID | Fase | Tarea | Descripción | Prioridad | Dependencias | Complejidad | Criterio de aceptación |
|----|------|-------|-------------|-----------|--------------|-------------|------------------------|
| T01 | F1 | Setup entorno | Crear venv, instalar dependencias con versiones pinned | Alta | Ninguna | Baja | `pip install -r requirements.txt` sin errores |
| T02 | F1 | Auto-fetch account IDs | Función que llama `/v1/accounts` y extrae `_id` sin intervención manual | Alta | T01 | Baja | `.env` tiene `ZERNIO_ACCOUNT_ID` populado automáticamente |
| T03 | F1 | Crear .env y .gitignore | Configurar archivos de secretos y exclusiones git | Alta | T02 | Baja | `.env` no aparece en `git status` |
| T04 | F2 | Scaffolding de archivos | Crear todos los archivos con stubs | Alta | T01 | Baja | `python -c "import app"` sin SyntaxError |
| T05 | F2 | Copiar patrones literales | `ADORATION_PATTERNS` y `BOT_PATTERNS` en `idea_filters.py` | Alta | T04 | Baja | Diff contra PDF = 0 cambios |
| T06 | F2 | Copiar system prompt literal | `prompts/ideas_system.md` = copia exacta del PDF | Alta | T04 | Baja | Diff contra PDF = 0 cambios |
| T07 | F3 | Cliente Zernio — función base | `_request()` con auth Bearer y retry exponencial | Alta | T03 | Media | Retry automático en 5xx verificado con mock |
| T08 | F3 | 9 endpoints cross-platform | Implementar paths verificados | Alta | T07 | Media | Cada endpoint retorna 200 con datos reales |
| T09 | F3 | 5 endpoints Instagram-only | Demographics, insights, follower history, conversations, messages | Alta | T07 | Media | Cada endpoint retorna 200 con datos reales |
| T10 | F3 | 3 endpoints YouTube-only | Solo si el usuario tiene YT | Media | T07 | Baja | Retorna 200 o se omite gracefully si no hay YT |
| T11 | F3 | Validación de endpoints | Función `validate_all_endpoints()` | Alta | T08, T09 | Baja | Reporte de qué endpoints funcionan y cuáles no |
| T12 | F4 | DDL 18 tablas | `init_db()` con todas las tablas | Alta | T03 | Alta | `sqlite3 .tables` muestra 18 tablas |
| T13 | F4 | Migración idempotente | PRAGMA check antes de ALTER TABLE | Alta | T12 | Media | `init_db()` x2 sin error |
| T14 | F4 | Writers con políticas de retención | Rolling deletes, upserts, snapshots | Alta | T12 | Media | Datos correctos después de 2 refreshes consecutivos |
| T15 | F4 | Backup antes de DELETE | JSON dump en `data.nosync/` | Alta | T12 | Baja | Backup JSON creado antes de cada migración destructiva |
| T16 | F5 | `refresh_instagram()` | Orquesta todos los endpoints IG y persiste | Alta | T08, T09, T14 | Media | `SELECT COUNT(*) FROM posts` > 0 |
| T17 | F5 | `refresh_youtube()` | Igual para YT (opcional) | Media | T10, T14 | Media | Solo si hay account_id_yt |
| T18 | F5 | Primer refresh real | Ejecutar y verificar datos | Alta | T16 | Baja | Datos reales en todas las tablas |
| T19 | F6 | `is_substantive_comment()` | Regex + min_len + preguntas | Alta | T05 | Media | Adulaciones filtradas, preguntas conservadas |
| T20 | F6 | `is_likely_bot_message()` | BOT_PATTERNS + URL/email check | Alta | T05 | Media | Mensajes bot detectados |
| T21 | F6 | Nombres bot del usuario | Preguntar y añadir a BOT_PATTERNS | Media | T19 | Baja | BOT_PATTERNS actualizado con contexto del usuario |
| T22 | F6 | Test de tasa de filtrado | Verificar % entre 30-70% | Alta | T19, T20 | Baja | % filtrado < 90% |
| T23 | F7 | Header Streamlit | Foto, username, followers, salud, botón refresh | Alta | T18 | Media | Header visible con datos reales |
| T24 | F7 | Tabs 1-6 | Resumen, Tendencia, Audiencia, Posts, Cuando publicar, Frecuencia | Alta | T18 | Alta | Cada tab muestra datos reales |
| T25 | F7 | Strip defensivo de IDs | `_ID_PATTERN_*` en `app.py` | Alta | T23 | Baja | IDs numéricos no aparecen en UI |
| T26 | F7 | Conversión UTC→TZ local | Para heatmaps con `zoneinfo` | Alta | T24 | Media | Heatmap en timezone del usuario |
| T27 | F7 | `AppTest` básico | Verificar arranque sin excepciones | Alta | T23 | Baja | `AppTest` pasa sin errores |
| T28 | F8 | `generate_all_ideas_ig()` | Single call Claude, 10/5/10 | Alta | T06, T19, T20 | Alta | 25 ideas con 3 bloques en JSON válido |
| T29 | F8 | Prompt caching correcto | Descartes en bloque NO cacheado | Alta | T28 | Media | Cache válido entre generaciones; descarte no invalida cache |
| T30 | F8 | `generate_bucket()` | Regenerar un bucket específico | Alta | T28 | Media | Bucket regenerado sin repetir descartados |
| T31 | F8 | Loop de descarte | INSERT idea_discards + UPDATE ideas | Alta | T28 | Media | Idea descartada desaparece de UI |
| T32 | F8 | Cards con 3 bloques | UI de cada idea con evidence_quotes, why, angle | Alta | T28 | Media | Cards visibles con los 3 secciones |
| T33 | F8 | Modal de descarte | Razones: Tema cubierto / No interesa / Muy básica / No mi estilo / Otro | Alta | T31 | Media | Modal funcional, razón persistida |
| T34 | F9 | Checklist de 12 puntos | Validación end-to-end manual | Alta | T32 | Baja | 12/12 puntos en verde |
| T35 | F10 | README.md | Instrucciones de uso | Alta | T34 | Baja | Nuevo usuario puede correr el proyecto solo con README |
| T36 | F10 | CLAUDE.md | Memoria para sesiones futuras de Claude Code | Alta | T34 | Baja | Claude Code puede retomar el proyecto leyendo solo CLAUDE.md |
| T37 | Opt. | Add-on transcripciones | yt-dlp + Whisper local | Baja | T34 | Alta | Solo si el usuario lo pide explícitamente |

---

# 8. Prompts internos para modelos locales

## Prompt 1: Generación de ideas (production prompt — literal del PDF)

| Campo | Detalle |
|-------|---------|
| **Nombre** | `ideas_system` |
| **Archivo** | `prompts/ideas_system.md` |
| **Objetivo** | Proponer ideas de contenido (reels, carruseles, YouTube) ancladas en data real de la cuenta |
| **Modelo** | `claude-sonnet-4-20250514` (claude-sonnet-4-5 según el PDF) |
| **Entrada** | Contexto cacheado: posts top + comentarios sustantivos + DMs sustantivos + demografía + mejor hora. Bloque no cacheado: instrucción + historial de descartes |
| **Salida esperada** | JSON con array de ideas, cada una con: `source_bucket`, `platforms`, `angle`, `format`, `evidence_quotes`, `why_good_idea`, `suggested_angle`, `rationale`, `basis_post_ids`, `basis_comment_ids`, `basis_message_ids` |
| **Formato de respuesta** | JSON estricto, sin texto antes ni después, sin backticks |
| **Reglas de seguridad** | No escribir IDs en campos de texto; no inventar evidencia; no escribir guiones completos; no generalidades |
| **Criterios de calidad** | Calidad > cantidad; mínimo 1 `basis_*_id` real por idea; mínimo 1 cita textual en `evidence_quotes`; no repetir ideas descartadas |
| **max_tokens** | 16000 |

> **El prompt completo está en `prompts/ideas_system.md`** — se copia LITERAL desde el PDF. Ver sección "System prompt de ideas (LITERAL)" en el documento fuente. No se reproduce aquí para evitar paráfrasis accidental.

---

## Prompt 2: Contexto de generación (user message — bloque cacheado)

| Campo | Detalle |
|-------|---------|
| **Nombre** | `ideas_user_context_cached` |
| **Objetivo** | Proveer el contexto grande de la cuenta a Claude para que pueda razonar sobre patrones |
| **Entrada** | Top 20 posts (caption + métricas), últimos 500 comentarios sustantivos, últimos 200 DMs sustantivos, demografía top (age/gender/country), mejor hora de publicación |
| **Formato** | Markdown estructurado por secciones, en bloque con `cache_control: ephemeral` |
| **Regla de oro** | Este bloque NO cambia entre generaciones dentro de la misma sesión → se cachea efectivamente |

```python
# Template del bloque cacheado (se construye dinámicamente en ideas.py)
cached_context = """
## Cuenta: {username} ({platform})
Followers: {followers} | Demografía dominante: {top_age_range}, {gender_split}

## Posts con mejor performance (top 20)
{for post in top_posts:}
### Post {i}: {post.timestamp[:10]}
Caption: {post.caption}
Métricas: {post.reach} alcance | {post.likes} likes | {post.comments_count} comentarios | {post.saves} guardados
{endfor}

## Comentarios sustantivos recientes
{for comment in substantive_comments:}
- [{comment.post_id_short}] {comment.text}
{endfor}

## Mensajes directos sustantivos (últimos 30 días)
{for dm in substantive_dms:}
- {dm.text}
{endfor}

## Mejor hora para publicar (IG)
{best_times_formatted}
"""
```

---

## Prompt 3: Instrucción por generación (user message — bloque NO cacheado)

| Campo | Detalle |
|-------|---------|
| **Nombre** | `ideas_user_instruction_uncached` |
| **Objetivo** | Instrucción específica + historial de descartes que varía por generación |
| **Entrada** | Tipo de generación (all/bucket), platform, bucket, últimos 50 descartes |
| **Formato** | Markdown con sección de descartes |
| **Regla crítica** | NUNCA poner descartes en el bloque cacheado — invalida el cache con cada descarte |

```python
# Template del bloque NO cacheado
uncached_instruction = """
Genera {n_ideas} ideas para {platform} del bucket "{bucket}".

{if discards:}
## Ideas que ya descartaste (NO repitas ni hagas variantes similares)
{for d in recent_discards:}
- [{d.source_bucket}] "{d.angle}" — razón: {d.reason_quick}{f": {d.reason_text}" if d.reason_text else ""}
{endfor}

Aprende de estos descartes: identifica el patrón (qué ángulos, formatos o temas no le gustan) y NO propongas variantes similares.
{endif}

Responde SOLO con el JSON. Sin texto antes ni después. Sin backticks.
"""
```

---

# 9. Estructura recomendada del repositorio

```
dashboard-instagram/
│
├── .env                          # API keys — GITIGNORED
├── .env.example                  # Template con placeholders
├── .gitignore                    # .env, data.nosync/, __pycache__/, .venv/
├── requirements.txt              # Versiones pinned (6 dependencias)
│
├── app.py                        # Streamlit app — punto de entrada UI
│                                 # 7 tabs + header + selector plataforma
│                                 # Strip defensivo de IDs numéricos
│
├── refresh.py                    # CLI: python refresh.py → actualiza cache
│                                 # También llamado por botón "Refrescar" en UI
│
├── zernio_client.py              # Wrapper REST para Zernio API
│                                 # 17 funciones + _request() con retry/backoff
│                                 # 100% solo lectura — sin endpoints de escritura
│
├── cache.py                      # SQLite I/O — 18 tablas
│                                 # init_db(), migrate_idempotent()
│                                 # Writers/readers por tabla
│                                 # Políticas de retención implementadas
│
├── ideas.py                      # Motor de generación con Anthropic API
│                                 # generate_all_ideas_ig/yt(), generate_bucket()
│                                 # discard_idea(), loop de aprendizaje
│
├── idea_filters.py               # Pre-filtrado de comentarios y DMs
│                                 # ADORATION_PATTERNS, BOT_PATTERNS (literales del PDF)
│                                 # is_substantive_comment/dm(), is_likely_bot_message()
│
├── prompts/
│   └── ideas_system.md           # System prompt LITERAL (calibrado con data real)
│                                 # NO modificar sin pruebas A/B
│
├── data.nosync/                  # Excluida de iCloud (.nosync = truco macOS)
│   ├── cache.db                  # SQLite database — GITIGNORED
│   └── backup_TIMESTAMP.json    # Backups automáticos pre-migración
│
├── README.md                     # Cómo instalar, correr, refrescar, generar ideas
│                                 # Tabla de troubleshooting
│
└── CLAUDE.md                     # Memoria para Claude Code
                                  # Gotchas críticos, stack, decisiones técnicas
                                  # Para retomar el proyecto en futuras sesiones
```

---

# 10. Flujo de ejecución del sistema

## Flujo A: Refresh de datos (~30 segundos)

```
1. TRIGGER
   └─ Usuario click "Refrescar datos" en UI → app.py llama refresh.main()
      ó Usuario corre: python refresh.py en Terminal

2. LOAD CONFIG
   └─ load_dotenv(override=True) → ZERNIO_API_KEY, ACCOUNT_IDs, DASHBOARD_TZ

3. VALIDACIÓN DE KEYS
   └─ zernio_client.get_account_health(account_id)
      ├─ 200: continuar
      ├─ 401: "API key Zernio expirada — genera nueva en zernio.com" → STOP
      └─ 402: "Activa add-on Analytics en Zernio" → continuar con endpoints disponibles

4. INGESTA POR TABLA (zernio_client → cache.py)
   ├─ account_snapshot: GET /accounts → UPDATE snapshot
   ├─ account_health: GET /accounts/{id}/health → UPDATE health
   ├─ account_insights_30d: GET /analytics/instagram/account-insights → REPLACE
   ├─ daily_metrics: GET /analytics/daily-metrics → UPSERT + DELETE rolling 180d
   ├─ demographics_*: GET /analytics/instagram/demographics → REPLACE
   ├─ follower_history: GET /analytics/instagram/follower-history → UPSERT acumulativo
   ├─ best_time: GET /analytics/best-time → REPLACE
   ├─ posting_frequency: GET /analytics/posting-frequency → REPLACE
   ├─ content_decay: GET /analytics/content-decay → REPLACE
   ├─ posts + comments: GET /inbox/comments → UPSERT posts + INSERT comments + DELETE rolling 90d
   └─ conversations + messages: GET /inbox/conversations → UPSERT + INSERT messages + DELETE rolling 30d

5. LOG
   └─ INSERT refresh_log(started_at, finished_at, status, error)

6. SALIDA
   └─ Cache SQLite actualizado
      UI muestra "Última actualización: hace X segundos"
```

## Flujo B: Generación de ideas (~15-30 segundos, ~$0.10-0.30 USD)

```
1. TRIGGER
   └─ Usuario click "Generar todas las ideas de Instagram"

2. PRE-FILTRADO (idea_filters.py)
   ├─ Leer comments de SQLite (últimos 90d)
   ├─ Leer messages de SQLite (últimos 30d)
   ├─ Aplicar is_substantive_comment() → lista filtrada
   ├─ Aplicar is_substantive_dm() + is_likely_bot_message() → lista filtrada
   └─ Resultado: [comentarios_sustantivos] + [dms_sustantivos]

3. CONSTRUCCIÓN DE CONTEXTO (ideas.py)
   ├─ Bloque CACHEADO: top 20 posts + comentarios sustantivos + DMs + demografía + mejor hora
   └─ Bloque NO CACHEADO: instrucción "genera 10/5/10 ideas" + últimos 50 descartes

4. LLAMADA A CLAUDE API (anthropic==0.97.0)
   ├─ Model: claude-sonnet-4-20250514
   ├─ max_tokens: 16000
   ├─ system: contenido de prompts/ideas_system.md
   ├─ messages[0].content[0]: contexto grande (cache_control: ephemeral)
   ├─ messages[0].content[1]: instrucción + descartes (sin cache)
   └─ En 529 Overloaded: retry backoff 2s→3s→5s→9s

5. PARSE Y VALIDACIÓN
   ├─ Parse JSON estricto de la respuesta
   ├─ Validar estructura de cada idea (campos obligatorios)
   ├─ Strip defensivo de IDs numéricos en campos de texto
   └─ En error de parse: mostrar mensaje de error al usuario

6. PERSISTENCIA
   └─ INSERT INTO ideas para cada idea válida (batch_id = UUID de la generación)

7. RENDERIZADO EN UI
   └─ 3 secciones expandibles (De comentarios / De DMs / De contenido top)
      └─ Cards con 3 bloques visuales por idea + botón "✕ Descartar"

8. LOGS Y TRAZABILIDAD
   └─ ideas.generated_at, ideas.batch_id registrados
      ideas.basis_*_ids permiten trazar cada idea a su evidencia original
```

## Flujo C: Descarte de idea (~1 segundo)

```
1. TRIGGER
   └─ Usuario click "✕ Descartar" en una card

2. MODAL
   └─ st.dialog() con radio de razones:
      [ ] Tema cubierto  [ ] No me interesa  [ ] Muy básica  [ ] No es mi estilo  [ ] Otro
      + Campo de texto opcional

3. CONFIRMACIÓN
   └─ Usuario selecciona razón + click "Confirmar descarte"

4. PERSISTENCIA
   ├─ INSERT INTO idea_discards (idea_id, angle, source_bucket, platform, reason_quick, reason_text, discarded_at)
   └─ UPDATE ideas SET discarded=1 WHERE id=?

5. FEEDBACK UI
   └─ Card desaparece del panel (st.rerun())

6. EFECTO EN PRÓXIMA GENERACIÓN
   └─ _build_discard_context() lee idea_discards (últimos 50)
      → Formateado como lista en bloque NO cacheado
      → Claude recibe el historial y evita variantes similares
```

---

# 11. Riesgos técnicos y decisiones pendientes

| Riesgo / Ambigüedad | Dónde aparece | Impacto | Recomendación | Urgencia | Pregunta a resolver |
|--------------------|--------------|---------|---------------|----------|---------------------|
| Add-ons Zernio no activos | Fase 3, troubleshooting | Alto — bloquea métricas y DMs | Verificar antes de construir. Si no están activos, Phase 3 detecta el 402 y pausa | Alta | ¿Tiene el usuario los add-ons Analytics e Inbox activos en Zernio? |
| Solo ~25 posts en dashboard | Troubleshooting del PDF | Medio — limitación conocida de Zernio | Documentar en README; no es un bug sino limitación de API | Baja | ¿El usuario tiene posts suficientes con comentarios? |
| Output tokens cap para 25 ideas | Gotcha #7 del PDF | Alto — respuesta truncada si >16K tokens | `max_tokens=16000` obligatorio; si Claude trunca, manejar el JSON incompleto con try/catch | Alta | ¿Está `max_tokens=16000` implementado en todas las llamadas? |
| `ANTHROPIC_API_KEY` vacía en entorno | Gotcha #1 del PDF | Alto — todo el sistema de ideas falla silenciosamente | `load_dotenv(override=True)` en todos los archivos que usen la key | Alta | ¿Todos los archivos que usan la API key tienen `override=True`? |
| iCloud Drive puede evaporar cache.db | Fase 2, gotcha #2 del PDF | Alto — pérdida de datos y ruptura de BD | Forzar `data.nosync/` para cache.db; documentar en README | Alta | ¿El usuario tiene el proyecto en iCloud Drive? |
| Token IG expirado | Troubleshooting del PDF | Alto — todos los endpoints fallan | Detectar en `zernio_client._request()`, mostrar mensaje claro de reconexión | Alta | N/A — implementar manejo específico |
| Versiones de anthropic + httpx | Gotcha #5 del PDF | Alto — errores de proxy en SDK antiguo | Pinear `anthropic==0.97.0` y `httpx==0.28.1` en requirements.txt | Alta | N/A — ya especificado |
| `/v1/analytics` con bug en Zernio | PDF sección endpoints | Alto — devuelve 400 con cualquier parámetro | Nunca usar ese path. Usar endpoints específicos | Alta | N/A — ya documentado |
| Calidad de ideas depende de volumen de datos | Sistema de ideas | Medio — con pocos posts/comentarios, las ideas son genéricas | Mínimo recomendado: 50 posts con comentarios, 100 comentarios sustantivos | Media | ¿Cuántos posts con comentarios tiene el usuario en Zernio? |
| BOT_PATTERNS genéricos pueden no cubrir el bot específico del usuario | Phase 6 del PDF | Medio — DMs de bot llegan a Claude y generan ideas falsas | Preguntar al usuario nombres de su bot y frases típicas | Media | ¿El usuario tiene un chatbot de respuesta automática en Instagram? |
| Over-filtering en idea_filters | Phase 6 del PDF | Medio — pocos comentarios llegan a Claude | Monitorear % de filtrado; si >90%, revisar ADORATION_PATTERNS | Media | Verificar tasa de filtrado con datos reales |
| Streamlit `use_container_width` en 1.39 | Gotcha #6 del PDF | Bajo — error de renderizado de imágenes | Usar `use_column_width=True` en toda llamada a `st.image` | Alta | N/A — ya documentado |
| YouTube opcional sin account_id | Phase 1 | Bajo — el usuario puede no tener YT | Verificar `ZERNIO_ACCOUNT_ID_YOUTUBE` antes de llamar cualquier endpoint YT | Baja | ¿El usuario tiene YouTube conectado en Zernio? |
| Backup antes de DELETE destructivo | Gotcha #4 del PDF | Bajo en producción, alto en desarrollo | Implementar `backup_before_delete()` en todas las migraciones | Media | N/A — implementar como parte de cache.py |
| TikTok: NO integrar | PDF explícito | N/A — es una restricción, no un riesgo | Nunca agregar TikTok aunque Zernio lo soporte | N/A | N/A — decisión tomada |

---

# 12. Roadmap de implementación

## MVP mínimo (Fases 1-5 + parcial 7)
**Objetivo**: Dashboard funcional que muestra datos reales, sin el sistema de ideas.
**Tiempo estimado**: 60-90 minutos de build con Claude Code.

- [x] Setup de entorno y API keys
- [x] Cliente Zernio con 9 endpoints cross-platform
- [x] Cache SQLite con las tablas principales
- [x] Primer refresh real con datos
- [x] Dashboard con tabs 1-4 (Resumen, Tendencia, Audiencia, Posts)
- [x] Header funcional con datos reales

**Criterio de salida**: El usuario puede ver sus métricas de Instagram en el browser.

---

## Versión funcional (Fases 1-8 completas)
**Objetivo**: Dashboard completo con generación de ideas operativa.
**Tiempo estimado**: 2-3 horas totales (incluyendo MVP).

- [x] Todo el MVP
- [x] Tabs 5-6 (Cuándo publicar, Frecuencia)
- [x] Tab 7 con generación de ideas completa
- [x] Sistema de descarte con aprendizaje
- [x] Pre-filtrado de comentarios/DMs

**Criterio de salida**: El usuario puede generar ideas y descartarlas; las próximas generaciones no repiten las descartadas.

---

## Versión robusta (Fases 1-10 completas)
**Objetivo**: Dashboard validado, documentado y listo para uso diario.
**Tiempo estimado**: 2.5-3 horas totales.

- [x] Todo lo anterior
- [x] Checklist de 12 puntos completado
- [x] README.md y CLAUDE.md escritos
- [x] Troubleshooting documentado
- [x] BOT_PATTERNS personalizados con el bot del usuario

**Criterio de salida**: El usuario puede usar el dashboard de forma autónoma y Claude Code puede retomar el proyecto en futuras sesiones.

---

## Versión productiva (opcional, post-validación)
**Objetivo**: Extensiones según necesidades del usuario.
**Tiempo estimado**: Variable, sesiones adicionales con Claude Code.

- [ ] Soporte YouTube completo (si no se hizo en las fases anteriores)
- [ ] Transcripciones de reels con yt-dlp + Whisper (solo si lo pide)
- [ ] Exportación de ideas a Notion (personalización)
- [ ] Email con ideas generadas (personalización)
- [ ] Backup automático de base de datos (personalización)

---

# 13. Checklist final para empezar a construir

## Lo primero que debes hacer para empezar con OpenCode

### Antes de abrir Claude Code

- [ ] **Crear la carpeta del proyecto**: `mkdir -p ~/Projects/dashboard-instagram`
  - ⚠️ NO en iCloud Drive (riesgo de pérdida de datos)
  - ✅ Recomendado: `~/Projects/dashboard-instagram/`

- [ ] **Tener a mano** (antes de que Claude te los pida):
  - [ ] API key de Zernio (empieza con `sk_...`) — obtenida en zernio.com/dashboard/api-keys
  - [ ] API key de Anthropic (empieza con `sk-ant-api03-...`) — obtenida en console.anthropic.com/settings/keys
  - [ ] Tu timezone exacta (ej: `Europe/Madrid`, `America/Mexico_City`, `America/Bogota`)
  - [ ] Saber si tienes YouTube conectado en Zernio (sí/no)
  - [ ] Verificar que los add-ons Analytics e Inbox están activos en Zernio

### En Claude Code

- [ ] **Abrir Claude Code en la carpeta del proyecto**:
  - Opción A: Terminal → `cd ~/Projects/dashboard-instagram && claude`
  - Opción B: App → "Open folder" → seleccionar `dashboard-instagram`

- [ ] **Adjuntar el PDF** al chat (drag-and-drop o comando de adjuntar)

- [ ] **Pegar el prompt de inicio** al chat:
```
Hola Claude. Te adjunto un PDF con instrucciones detalladas para construir un dashboard local de análisis de mi cuenta de Instagram. También te adjunto el Plan Técnico de Implementación que ya analicé del PDF. 

Úsalos ambos como referencia. Empieza por la Fase 1 del plan técnico: Setup inicial.

Cuando necesites mis API keys o información, pregúntamela. Soy principiante con Claude Code.
```

- [ ] **Responder las preguntas de Claude Code** cuando te las haga (keys, timezone, YouTube sí/no)

### Validaciones críticas antes de continuar a la siguiente fase

- [ ] Fase 1 → Verificar que `.env` tiene los 5 campos y que `ZERNIO_ACCOUNT_ID` fue obtenido automáticamente
- [ ] Fase 3 → Verificar que `validate_all_endpoints()` pasa para los endpoints principales
- [ ] Fase 5 → Verificar que `SELECT COUNT(*) FROM posts` en SQLite devuelve >0
- [ ] Fase 6 → Verificar que la tasa de filtrado es <90%
- [ ] Fase 7 → Verificar que el dashboard abre en `localhost:8501` con datos reales
- [ ] Fase 8 → Verificar que una generación produce ideas con los 3 bloques

### Si algo falla

- **Errores de API Zernio**: pega el error completo en Claude Code → dice exactamente qué hacer
- **Errores de dashboard**: busca el traceback en la terminal donde corre `streamlit run app.py`
- **Errores de ideas**: verifica que `ANTHROPIC_API_KEY` está en `.env` con `load_dotenv(override=True)`
- **Regla general**: pega el error completo en Claude Code y di "esto falló, arréglalo" — Claude lo arregla

---

*Plan técnico generado con nivel de confianza 95% basado en el documento "Cómo crear tu propio dashboard de análisis de contenido con Claude Code". Toda la información marcada sin indicador especial está extraída directamente del documento. Las marcas "supuesto técnico recomendado" y "pendiente de validación" se usan solo donde el documento no especifica.*
