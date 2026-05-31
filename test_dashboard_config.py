#!/usr/bin/env python3
"""
Prueba del funcionamiento completo del dashboard con modelo local
"""

import sys
import os

# Añadir el directorio actual al path para poder importar correctamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar directamente las variables de entorno
from dotenv import load_dotenv
load_dotenv(override=True)

def test_config():
    """Test the configuration"""
    
    print("=== Configuración del Dashboard ===")
    
    # Variables de entorno del modelo local
    LOCAL_LLM_ENABLED = os.getenv("LOCAL_LLM_ENABLED", "false").lower() == "true"
    LOCAL_LLM_ENDPOINT = os.getenv("LOCAL_LLM_ENDPOINT")
    LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL")
    
    print(f"LOCAL_LLM_ENABLED: {LOCAL_LLM_ENABLED}")
    print(f"LOCAL_LLM_ENDPOINT: {LOCAL_LLM_ENDPOINT}")
    print(f"LOCAL_LLM_MODEL: {LOCAL_LLM_MODEL}")
    
    if LOCAL_LLM_ENABLED:
        print("✅ Modelo local está habilitado")
        if LOCAL_LLM_ENDPOINT and LOCAL_LLM_MODEL:
            print("✅ Configuración del modelo local completa")
        else:
            print("❌ Configuración incompleta del modelo local")
    else:
        print("❌ Modelo local no está habilitado")
    
    return True

if __name__ == "__main__":
    test_config()