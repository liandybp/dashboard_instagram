# Plan: Migrar Generación de Ideas a Qwen3.6-27B Local (llama.cpp)

## Contexto

Actualmente el dashboard usa Anthropic Claude API para generar ideas de contenido. 
El objetivo es migrar a un modelo local Qwen3.6-27B ejecutado con llama.cpp, 
configurado como un agente que será invocado por otro modelo orquestador.

## Arquitectura Propuesta

```
Dashboard (app.py) 
    -> ideas.py (llamada HTTP) 
        -> Modelo Orquestador (otro modelo local) 
            -> Agente Qwen3.6-27B (llama.cpp)
```

### Componentes

1. **llama.cpp Server**
   - Modelo: Qwen3.6-27B en formato GGUF
   - Endpoint: `http://localhost:8080` (puerto configurable)
   - API compatible con OpenAI

2. **Modelo Orquestador**
   - Recibe las peticiones del dashboard
   - Decide cuándo y cómo invocar al agente Qwen3.6-27B
   - Gestiona el contexto y las respuestas

3. **Agente Qwen3.6-27B**
   - Especializado en generación de ideas de contenido
   - Recibe contexto estructurado del orquestador
   - Devuelve ideas en formato JSON

## Modificaciones Necesarias

### 1. En `ideas.py`

- Reemplazar cliente Anthropic por llamadas HTTP al modelo orquestador
- Adaptar formato de mensajes para el nuevo flujo
- Mantener retry logic con backoff
- Actualizar parsing de respuestas JSON

### 2. En `.env`

```
# Configuración actual (mantener)
ZERNIO_API_KEY=...
ZERNIO_ACCOUNT_ID=...
ZERNIO_ACCOUNT_ID_YOUTUBE=...
ANTHROPIC_API_KEY=...
DASHBOARD_TZ=...

# Nueva configuración para modelo local
ORCHESTRATOR_ENDPOINT=http://localhost:8080/v1/chat/completions
ORCHESTRATOR_MODEL=<nombre_modelo_orquestador>
AGENT_ENDPOINT=http://localhost:8080/v1/chat/completions
AGENT_MODEL=qwen3.6-27b
AGENT_MAX_TOKENS=16000
```

### 3. En `prompts/ideas_system.md`

- Adaptar prompt para formato de agente
- Especificar claramente el rol del agente en el sistema
- Mantener estructura de respuesta JSON

## Implementación del Agente

### Prompt del Agente Qwen3.6-27B

```
Eres un agente especializado en generar ideas de contenido para redes sociales.
Recibirás contexto estructurado con datos de engagement, comentarios, y tendencias.
Tu tarea es generar ideas únicas y efectivas en formato JSON.

Formato de entrada:
- Contexto de la plataforma (Instagram/YouTube)
- Datos de engagement
- Comentarios filtrados
- Posts populares
- Ideas descartadas previamente

Formato de salida (JSON):
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

## Flujo de Ejecución

1. Dashboard solicita ideas a `ideas.py`
2. `ideas.py` envía petición al modelo orquestador
3. Orquestador prepara contexto y lo envía al agente Qwen3.6-27B
4. Agente genera ideas y las devuelve al orquestador
5. Orquestador formatea respuesta y la devuelve al dashboard
6. Dashboard muestra ideas al usuario

## Ventajas

- **Control total**: Modelo local sin dependencias externas
- **Privacidad**: Datos no salen del servidor
- **Personalización**: Prompt y comportamiento totalmente configurables
- **Escalabilidad**: Posibilidad de múltiples agentes especializados

## Consideraciones Técnicas

- **Requisitos de hardware**: Qwen3.6-27B necesita ~16-24GB VRAM
- **Quantización**: Usar Q4_K_M o Q5_K_M para balance calidad/memoria
- **Context window**: Configurar para manejar prompts largos (contexto + instrucciones)
- **Temperatura**: 0.7-0.9 para creatividad controlada

## Pruebas

1. Verificar que llama.cpp sirve correctamente el modelo
2. Probar llamadas directas al agente
3. Integrar con orquestador
4. Testear flujo completo desde dashboard
5. Comparar calidad de ideas vs versión Claude

## Timeline Estimado

1. **Configuración llama.cpp**: 1-2 horas
2. **Desarrollo del agente**: 2-3 horas  
3. **Integración con orquestador**: 2-3 horas
4. **Testing y ajuste**: 2-4 horas
5. **Documentación**: 1 hora

Total: ~8-12 horas de trabajo
