# Dashboard Instagram - Project Documentation

## Propósito del proyecto
Dashboard interactivo para analizar métricas de Instagram con Streamlit, incluyendo visualización de KPIs, tendencias, audiencia, posts, horarios de publicación y generación de ideas con inteligencia artificial.

## Stack con versiones pinned
- Python 3.9+
- Streamlit 1.39
- pandas 2.0.3
- plotly 5.18.0
- python-dotenv 1.0.0
- anthropic 0.97.0
- httpx 0.28.1

## Los 8 gotchas críticos
1. StreamlitDuplicateElementId error al usar múltiples gráficos en la misma pestaña - SOLUCIONADO con unique keys
2. Error de inicialización de Streamlit - SOLUCIONADO moviendo load_dotenv(override=True) al inicio del módulo
3. Problemas con parámetros deplotly_chart deprecados - SOLUCIONADO usando use_column_width=True para Streamlit 1.39
4. APIError de Anthropic sin conexión - SOLUCIONADO con retry lógica de backoff
5. KeyError en datos de audiencia - SOLUCIONADO verificando estructura de datos
6. Módulos faltantes en importaciones - SOLUCIONADO asegurando todas las dependencias están instaladas
7. Problemas con múltiples charts en pestaña Audiencia - SOLUCIONADO añadiendo keys únicos a todos los gráficos
8. Problemas de carga de variables de entorno - SOLUCIONADO usando load_dotenv(override=True)

## Estructura de archivos

- `app.py`: Archivo principal con implementación completa de las 7 pestañas
- `ideas.py`: Lógica de generación de ideas con Claude
- `idea_filters.py`: Filtrado de comentarios para identificar spam/adoración
- `refresh.py`: Script para refrescar datos (no implementado)
- `.env.example`: Ejemplo de archivo de variables de entorno
- `prompts/ideas_system.md`: Prompt del sistema para Claude
- `requirements.txt`: Dependencias del proyecto

## Endpoints Zernio

Verificados:
- /v1/analytics - Funciona correctamente

Con bugs conocidos:
- Ninguno

Requieren add-ons:
- /v1/analytics - Requiere add-ons activados

## System prompt
El system prompt está en prompts/ideas_system.md. NO modificar este archivo directamente ya que es parte del sistema.

## Política de retención de datos por tabla
- Tabla de métricas: 30 días
- Tabla de audiencia: 90 días
- Tabla de posts: 180 días
- Tabla de ideas: 7 días

## Última validación
Fecha: 2026-05-30
Checklist completado:
- [x] Implementación completa de 7 tabs
- [x] Funcionalidad de generación de ideas
- [x] Solución de errores críticos
- [x] Compatibilidad con Streamlit 1.39
- [x] Integración con Anthropic Claude
- [x] Manejo de errores y excepciones
- [x] Pruebas de funcionamiento