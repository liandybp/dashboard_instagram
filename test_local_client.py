#!/usr/bin/env python3
"""
Prueba del cliente local de LLM
"""

import sys
import os
import asyncio

# Añadir el directorio actual al path para poder importar correctamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.local_llm_client import LocalLLMClient

async def test_local_client():
    """Test the local LLM client"""
    
    # Configuración del cliente local
    client = LocalLLMClient(
        endpoint="http://localhost:8080/v1/chat/completions",
        model="qwen3.6_content_creator",
        max_tokens=4096,
        temperature=0.95
    )
    
    # Test simple
    try:
        messages = [
            {"role": "user", "content": "Hola, ¿cómo estás?"}
        ]
        response = await client.generate_text(messages)
        print("Respuesta del cliente local:", response)
        return True
    except Exception as e:
        print(f"Error en el cliente local: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_local_client())