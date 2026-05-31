#!/usr/bin/env python3
"""
Script de prueba integrada con Zernio conectado
Este script ejecuta una prueba completa de la aplicación con datos reales de Zernio
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(override=True)

# Importar módulos necesarios
from zernio_client import ZernioClient
import ideas
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def test_zernio_connection():
    """Test de conexión con Zernio"""
    print("🔍 Test de conexión con Zernio...")
    
    try:
        # Crear cliente Zernio
        client = ZernioClient()
        
        # Validar todos los endpoints
        results = client.validate_all_endpoints()
        
        # Mostrar resultados
        success_count = sum(1 for r in results.values() if r["status"] == "SUCCESS")
        total_count = len(results)
        
        print(f"✅ {success_count}/{total_count} endpoints funcionando correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en conexión con Zernio: {e}")
        return False

def test_ideas_generation():
    """Test de generación de ideas con Zernio"""
    print("🧠 Test de generación de ideas...")
    
    try:
        # Generar ideas para Instagram
        import asyncio
        ideas_list = asyncio.run(ideas.generate_all_ideas_ig())
        
        print(f"✅ Generadas {len(ideas_list)} ideas para Instagram")
        
        # Mostrar algunas ideas
        for i, idea in enumerate(ideas_list[:3]):
            print(f"  Idea {i+1}: {idea['angle']}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error en generación de ideas: {e}")
        return False

def test_data_loading():
    """Test de carga de datos desde Zernio"""
    print("📊 Test de carga de datos...")
    
    try:
        # Crear cliente Zernio
        client = ZernioClient()
        
        # Obtener algunos datos de ejemplo
        account_insights = client.get_account_insights()
        daily_metrics = client.get_daily_metrics()
        demographics = client.get_demographics()
        
        print("✅ Datos cargados correctamente desde Zernio")
        print(f"  - Insights: {len(account_insights)} campos")
        print(f"  - Métricas diarias: {len(daily_metrics)} registros")
        print(f"  - Demografía: {len(demographics)} registros")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en carga de datos: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("🧪 PRUEBA INTEGRADA CON ZERNIO CONECTADO")
    print("=" * 60)
    
    # Verificar que las variables de entorno estén configuradas
    required_vars = ["ZERNIO_API_KEY", "ZERNIO_ACCOUNT_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("Por favor configure las variables en .env o en el entorno")
        return False
    
    # Ejecutar tests
    tests = [
        test_zernio_connection,
        test_data_loading,
        test_ideas_generation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Error en {test.__name__}: {e}")
            results.append(False)
            print()
    
    # Mostrar resultados finales
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"📊 RESULTADOS FINALES: {passed}/{total} tests pasados")
    
    if passed == total:
        print("🎉 TODOS LOS TESTS PASARON - LA APLICACIÓN ESTÁ LISTA PARA USO")
        return True
    else:
        print("⚠️  ALGUNOS TESTS FALLARON - REVISAR CONFIGURACIÓN")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)