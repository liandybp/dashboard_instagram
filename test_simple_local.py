#!/usr/bin/env python3
"""
Prueba rápida del cliente local LLM
"""

import sys
import os
import asyncio

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar variables de entorno para usar modelo local
os.environ["LOCAL_LLM_ENABLED"] = "true"
os.environ["LOCAL_LLM_ENDPOINT"] = "http://localhost:8080/v1/chat/completions"
os.environ["LOCAL_LLM_MODEL"] = "qwen3.6_content_creator"
os.environ["LOCAL_LLM_MAX_TOKENS"] = "4096"
os.environ["LOCAL_LLM_TEMPERATURE"] = "0.95"

from app.local_llm_client import LocalLLMClient

async def test_local_client():
    """Test the local LLM client directly"""
    
    print("=== Prueba del Cliente Local LLM ===")
    
    try:
        # Crear cliente
        client = LocalLLMClient(
            endpoint="http://localhost:8080/v1/chat/completions",
            model="qwen3.6_content_creator",
            max_tokens=4096,
            temperature=0.95
        )
        
        print("✅ Cliente local creado correctamente")
        
        # Probar conexión simple
        messages = [
            {"role": "user", "content": "Hola, ¿cómo estás?"}
        ]
        
        print("Enviando mensaje al modelo local...")
        response = await client.generate_text(messages)
        print("✅ Respuesta recibida:")
        print(response[:200] + "..." if len(response) > 200 else response)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_local_client())
    if success:
        print("\n🎉 Prueba de cliente local completada con éxito!")
    else:
        print("\n💥 Prueba fallida")