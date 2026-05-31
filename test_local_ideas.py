#!/usr/bin/env python3
"""
Prueba completa de generación de ideas con modelo local
"""

import sys
import os

# Añadir el directorio actual al path para poder importar correctamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.local_llm_client import LocalLLMClient
import asyncio

async def test_ideas_generation():
    """Test idea generation with local LLM"""
    
    # Configuración del cliente local
    client = LocalLLMClient(
        endpoint="http://localhost:8080/v1/chat/completions",
        model="qwen3.6_content_creator",
        max_tokens=4096,
        temperature=0.95
    )
    
    # Test simple de generación de ideas
    try:
        messages = [
            {"role": "system", "content": "Eres un experto en creación de contenido para Instagram. Genera ideas innovadoras y atractivas."},
            {"role": "user", "content": "Genera 3 ideas de publicaciones para una cuenta de viajes"}
        ]
        
        print("Generando ideas con modelo local...")
        response = await client.generate_text(messages)
        print("✅ Respuesta recibida:")
        print(response[:200] + "..." if len(response) > 200 else response)
        return True
    except Exception as e:
        print(f"❌ Error en la generación de ideas: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_ideas_generation())