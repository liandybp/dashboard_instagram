import os
import time
import json
from typing import Dict, List, Any
from anthropic import Anthropic
from anthropic.types import MessageCreateParams
import httpx
from dotenv import load_dotenv

# GOTCHA CRÍTICO #1: load_dotenv(override=True) al inicio
load_dotenv(override=True)

# GOTCHA CRÍTICO #5: usa anthropic==0.97.0 y httpx==0.28.1 (ya están en requirements.txt)
# Se asume que estas versiones están instaladas

# Cargar prompt system desde archivo
with open("prompts/ideas_system.md", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Configuración de clientes Claude
client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

def _build_cached_context(platform: str) -> Dict[str, Any]:
    """
    Construye el contexto grande para cacheo ephemeral (bloque 1)
    """
    # Mock data - en producción se conectaría a base de datos
    context = {
        "platform": platform,
        "top_posts": [
            {"id": i, "caption": f"Post {i} caption", "engagement_rate": 4.5 + i * 0.1}
            for i in range(20)
        ],
        "filtered_comments": [
            {"id": i, "text": f"Comentario {i} sobre post {i%5}", "sentiment": "positive"}
            for i in range(500)
        ],
        "filtered_dms": [
            {"id": i, "text": f"DM {i} con usuario", "sentiment": "neutral"}
            for i in range(200)
        ],
        "demographics": {
            "age_groups": ["18-24", "25-34", "35-44", "45-54", "55+"],
            "engagement_by_age": [35, 42, 38, 29, 16]
        },
        "best_publish_time": "15:00"
    }
    
    return context

def _build_discard_context() -> str:
    """
    Construye el contexto de descartes para no cachear (bloque 2)
    """
    # Mock data - en producción se conectaría a base de datos
    discards = [
        {"id": i, "bucket": f"bucket_{i%3}", "angle": f"Ángulo {i}", "reason": "Tema cubierto"}
        for i in range(50)
    ]
    
    discard_text = "## Ideas que ya descartaste (NO repitas ni hagas variantes similares)\n"
    for discard in discards:
        discard_text += f"- [{discard['bucket']}] \"{discard['angle']}\" — razón: {discard['reason']}\n"
    
    return discard_text

def generate_all_ideas_ig() -> List[Dict[str, Any]]:
    """
    Genera todas las ideas para Instagram (10 comments + 5 dms + 10 top_content)
    """
    # GOTCHA CRÍTICO #7: max_tokens=16000 para la llamada de 25 ideas
    cached_context = _build_cached_context("instagram")
    
    # Bloque 1 (cacheado con cache_control ephemeral)
    system_prompt_with_context = SYSTEM_PROMPT + "\n\n### Contexto para cacheo (no modificar):\n" + json.dumps(cached_context, ensure_ascii=False)
    
    # Bloque 2 (NO cacheado)
    discard_context = _build_discard_context()
    
    prompt = f"""
Genera 25 ideas de contenido para Instagram basadas en:
- {len(cached_context['filtered_comments'])} comentarios filtrados
- {len(cached_context['filtered_dms'])} DMs filtrados
- Top {len(cached_context['top_posts'])} posts con sus captions

{discard_context}

Instrucciones finales:
1. Genera ideas en 3 buckets principales: 
   - De comentarios (comentarios que generan ideas)
   - De contenido (bases de ideas sobre contenido popular)  
   - De tendencias (ideas basadas en tendencias actuales)

2. Para cada idea, proporciona:
   - angle: ángulo principal
   - evidence_quotes: citas relevantes del contexto
   - why_good_idea: por qué es buena idea
   - suggested_angle: ángulo sugerido para variación
   - bucket: bucket al que pertenece (de comentarios, de contenido, de tendencias)

3. Las ideas deben ser únicas y no repetir los descartes anteriores.
"""
    
    # GOTCHA CRÍTICO #8: retry con backoff 2s/3s/5s/9s para errores 5xx y 529 de Anthropic
    max_retries = 4
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                system=system_prompt_with_context,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=16000,  # GOTCHA CRÍTICO #7
                cache_control={"type": "ephemeral"}  # Bloque 1 - cacheado
            )
            
            # Procesar la respuesta de Claude
            response_text = message.content[0].text
            
            # Aquí se procesaría el JSON si Claude lo devuelve en formato JSON
            # Para este mock, simplemente retornamos estructura simulada
            ideas = []
            for i in range(25):
                ideas.append({
                    "id": f"idea_{i}",
                    "angle": f"Idea {i} de contenido para Instagram",
                    "evidence_quotes": [f"Cita de ejemplo {j}" for j in range(3)],
                    "why_good_idea": f"Buena idea porque tiene potencial de engagement",
                    "suggested_angle": f"Ángulo sugerido {i}",
                    "bucket": ["de comentarios", "de contenido", "de tendencias"][i % 3]
                })
            
            return ideas
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [500, 502, 503, 504, 529]:
                # GOTCHA CRÍTICO #8: retry con backoff
                wait_time = [2, 3, 5, 9][attempt]
                print(f"Error {e.response.status_code}, reintentando en {wait_time} segundos...")
                time.sleep(wait_time)
                continue
            else:
                raise
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise
    
    # Si llegamos aquí, todas las reintentos fallaron
    raise Exception("Todos los intentos de llamada a Claude fallaron")

def generate_all_ideas_yt() -> List[Dict[str, Any]]:
    """
    Genera todas las ideas para YouTube (10 comments + 10 top_content)
    """
    cached_context = _build_cached_context("youtube")
    
    # Bloque 1 (cacheado con cache_control ephemeral)
    system_prompt_with_context = SYSTEM_PROMPT + "\n\n### Contexto para cacheo (no modificar):\n" + json.dumps(cached_context, ensure_ascii=False)
    
    # Bloque 2 (NO cacheado)
    discard_context = _build_discard_context()
    
    prompt = f"""
Genera 25 ideas de contenido para YouTube basadas en:
- {len(cached_context['filtered_comments'])} comentarios filtrados
- Top {len(cached_context['top_posts'])} posts con sus captions

{discard_context}

Instrucciones finales:
1. Genera ideas en 3 buckets principales: 
   - De comentarios (comentarios que generan ideas)
   - De contenido (bases de ideas sobre contenido popular)  
   - De tendencias (ideas basadas en tendencias actuales)

2. Para cada idea, proporciona:
   - angle: ángulo principal
   - evidence_quotes: citas relevantes del contexto
   - why_good_idea: por qué es buena idea
   - suggested_angle: ángulo sugerido para variación
   - bucket: bucket al que pertenece (de comentarios, de contenido, de tendencias)

3. Las ideas deben ser únicas y no repetir los descartes anteriores.
"""
    
    # GOTCHA CRÍTICO #8: retry con backoff 2s/3s/5s/9s para errores 5xx y 529 de Anthropic
    max_retries = 4
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                system=system_prompt_with_context,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=16000,  # GOTCHA CRÍTICO #7
                cache_control={"type": "ephemeral"}  # Bloque 1 - cacheado
            )
            
            # Procesar la respuesta de Claude
            response_text = message.content[0].text
            
            # Aquí se procesaría el JSON si Claude lo devuelve en formato JSON
            # Para este mock, simplemente retornamos estructura simulada
            ideas = []
            for i in range(25):
                ideas.append({
                    "id": f"idea_{i}",
                    "angle": f"Idea {i} de contenido para YouTube",
                    "evidence_quotes": [f"Cita de ejemplo {j}" for j in range(3)],
                    "why_good_idea": f"Buena idea porque tiene potencial de engagement",
                    "suggested_angle": f"Ángulo sugerido {i}",
                    "bucket": ["de comentarios", "de contenido", "de tendencias"][i % 3]
                })
            
            return ideas
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [500, 502, 503, 504, 529]:
                # GOTCHA CRÍTICO #8: retry con backoff
                wait_time = [2, 3, 5, 9][attempt]
                print(f"Error {e.response.status_code}, reintentando en {wait_time} segundos...")
                time.sleep(wait_time)
                continue
            else:
                raise
        except Exception as e:
            print(f"Error inesperado: {e}")
            raise
    
    # Si llegamos aquí, todas las reintentos fallaron
    raise Exception("Todos los intentos de llamada a Claude fallaron")

def generate_bucket(platform: str, bucket: str, n: int = 5) -> List[Dict[str, Any]]:
    """
    Regenera un bucket específico con n ideas
    """
    # Este método usaría el mismo patrón pero filtrando por bucket
    # Mock implementation
    return [{"id": f"{bucket}_idea_{i}", "angle": f"Idea {i} en bucket {bucket}"} for i in range(n)]

def discard_idea(idea_id: str, reason_quick: str, reason_text: str) -> None:
    """
    Registra un descarte de idea (INSERT + UPDATE)
    """
    # Mock implementation - en producción conectaría a base de datos
    print(f"Descartando idea {idea_id}: {reason_quick} - {reason_text}")