# Plan de Implementación: Migración a Qwen3.6-27B Local
> Basado en: `plan_qwen3.6_local.md`
> Agente ejecutor: `qwen3_coder` via OpenCode
> Infraestructura: llama-swap + llama.cpp + Tesla P40

---

## Contexto para el agente coder

El dashboard `greter/dashboard_instagram` usa actualmente Anthropic Claude API
para generar ideas de contenido en `ideas.py`. El objetivo es migrar a un modelo
local `qwen3.6_content_creator` corriendo en llama-swap (puerto 8080), manteniendo
la misma interfaz JSON de salida.

**Infraestructura ya disponible:**
- llama-swap corriendo en `http://localhost:8080`
- Modelo `qwen3.6_content_creator` registrado con alias `qwen3.6_content_creator`
- API compatible con OpenAI en `/v1/chat/completions`

---

## TAREA 1 — Variables de entorno

**Archivo:** `.env`
**Tipo:** Configuración
**Dependencias:** Ninguna — hacer primero

Añadir al `.env` existente sin eliminar las variables actuales:

```
# Modelo local (llama-swap)
LOCAL_LLM_ENDPOINT=http://localhost:8080/v1/chat/completions
LOCAL_LLM_MODEL=qwen3.6_content_creator
LOCAL_LLM_MAX_TOKENS=4096
LOCAL_LLM_TEMPERATURE=0.95
LOCAL_LLM_ENABLED=true
```

**Prompt para OpenCode:**
```
Lee el archivo .env actual del proyecto. Añade las variables de configuración
para el modelo local sin eliminar ninguna variable existente. Usa los valores
exactos del bloque de arriba. Añade un comentario de sección # Modelo local (llama-swap).
```

---

## TAREA 2 — Cliente HTTP local

**Archivo:** `app/local_llm_client.py` (nuevo)
**Tipo:** Módulo Python nuevo
**Dependencias:** TAREA 1

Cliente HTTP reutilizable que apunta a llama-swap. Debe:
- Leer configuración desde variables de entorno
- Manejar timeout y retry con backoff exponencial
- Parsear respuesta JSON del modelo
- Lanzar excepción específica `LocalLLMError` si falla
- Type hints completos

**Prompt para OpenCode:**
```
Crea el archivo app/local_llm_client.py con un cliente HTTP para llama-swap.
Lee la configuración desde variables de entorno (LOCAL_LLM_ENDPOINT, LOCAL_LLM_MODEL,
LOCAL_LLM_MAX_TOKENS, LOCAL_LLM_TEMPERATURE). Implementa retry con backoff exponencial
(máximo 3 intentos). Define la excepción LocalLLMError. Type hints completos.
Usa httpx async, no requests.
```

---

## TAREA 3 — Prompt del agente de contenido

**Archivo:** `prompts/ideas_local_system.md` (nuevo)
**Tipo:** Prompt markdown
**Dependencias:** Ninguna — puede hacerse en paralelo con TAREA 2

Prompt especializado para `qwen3.6_content_creator`. Debe:
- Definir el rol del agente claramente
- Especificar el formato JSON de salida exacto del plan original
- Incluir instrucciones de idioma (español)
- Ser conciso — el modelo tiene contexto limitado

**Formato JSON de salida requerido:**
```json
[
  {
    "id": "string",
    "angle": "string",
    "evidence_quotes": ["string"],
    "why_good_idea": "string",
    "suggested_angle": "string",
    "bucket": "de comentarios|de contenido|de tendencias"
  }
]
```

**Prompt para OpenCode:**
```
Crea el archivo prompts/ideas_local_system.md con el system prompt para el agente
de generación de ideas. El agente recibe contexto de Instagram (engagement, comentarios,
posts populares, ideas descartadas) y devuelve ideas en el JSON especificado arriba.
Responde siempre en español. Sé conciso — máximo 400 palabras en el prompt.
```

---

## TAREA 4 — Adaptar ideas.py

**Archivo:** `ideas.py` (modificar)
**Tipo:** Modificación de módulo existente
**Dependencias:** TAREA 1, TAREA 2, TAREA 3

Esta es la tarea central. Debe:
- Leer `LOCAL_LLM_ENABLED` para decidir qué cliente usar
- Si `LOCAL_LLM_ENABLED=true` → usar `local_llm_client.py`
- Si `LOCAL_LLM_ENABLED=false` → mantener cliente Anthropic actual (fallback)
- Mantener la misma interfaz de salida JSON que usa el dashboard
- Mantener el retry logic existente
- No romper nada del flujo actual

**Prompt para OpenCode:**
```
Lee el archivo ideas.py completo. Modifícalo para que cuando LOCAL_LLM_ENABLED=true
use el cliente local de app/local_llm_client.py en lugar del cliente Anthropic.
Cuando LOCAL_LLM_ENABLED=false debe seguir funcionando exactamente igual que antes.
Mantén la misma interfaz de salida. No elimines el cliente Anthropic — solo añade
la bifurcación. Muéstrame el diff antes de aplicar cambios.
```

---

## TAREA 5 — Test de integración

**Archivo:** `tests/test_local_llm.py` (nuevo)
**Tipo:** Tests pytest
**Dependencias:** TAREA 2, TAREA 4

Tests que verifican:
- El cliente local conecta correctamente a llama-swap
- La respuesta JSON tiene el schema correcto
- El fallback a Anthropic funciona cuando `LOCAL_LLM_ENABLED=false`
- El retry logic funciona cuando llama-swap no responde

**Prompt para OpenCode:**
```
Crea tests/test_local_llm.py con tests pytest para el cliente local.
Usa httpx MockTransport para mockear las llamadas a llama-swap sin necesitar
el servidor real. Testea: conexión exitosa, respuesta JSON válida, fallback
cuando LOCAL_LLM_ENABLED=false, y retry cuando el servidor devuelve 503.
```

---

## TAREA 6 — Test end-to-end manual

**Tipo:** Verificación manual
**Dependencias:** TODAS las anteriores

Secuencia de verificación:

```bash
# 1. Verificar que llama-swap está corriendo
curl -s http://localhost:8080/v1/models | python3 -m json.tool

# 2. Test directo al modelo content_creator
curl -s http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.6_content_creator",
    "messages": [{"role": "user", "content": "Dame 2 ideas de reels para una cuenta de IA local"}],
    "max_tokens": 500
  }' | python3 -m json.tool

# 3. Test con LOCAL_LLM_ENABLED=true
LOCAL_LLM_ENABLED=true python3 -c "from ideas import generate_ideas; print(generate_ideas(test_context))"

# 4. Verificar que el fallback funciona
LOCAL_LLM_ENABLED=false python3 -c "from ideas import generate_ideas; print(generate_ideas(test_context))"
```

---

## Orden de ejecución en OpenCode

```
1. /agent coder → TAREA 1 (.env)
2. /agent coder → TAREA 3 (prompt markdown) — puede ir en paralelo con TAREA 2
3. /agent coder → TAREA 2 (local_llm_client.py)
4. /agent coder → TAREA 4 (ideas.py) — la más crítica, pedir diff antes de aplicar
5. /agent coder → TAREA 5 (tests)
6. TAREA 6 — verificación manual con los comandos de arriba
```

## Rollback si algo falla

```bash
# Si ideas.py se rompe, revertir con git
git diff ideas.py          # ver cambios
git checkout ideas.py      # revertir al original
```

---

## Notas importantes para el agente coder

- El modelo en llama-swap se llama `qwen3.6_content_creator` — usar ese alias exacto
- llama-swap está en `http://localhost:8080` — no cambiar el puerto
- La API es compatible con OpenAI — usar el mismo formato de messages
- Temperature ya está configurada en llama-swap (0.95) — no sobreescribir en el cliente
- El dashboard espera el JSON con los campos exactos definidos en TAREA 3
