# Dashboard Instagram

Este proyecto es un dashboard interactivo para analizar métricas de Instagram utilizando Streamlit. Permite visualizar KPIs, tendencias, audiencia, posts, horarios de publicación y generar ideas de contenido con inteligencia artificial.

## Prerrequisitos

- Python 3.9+
- Cuenta Zernio con add-ons activados
- API key de Anthropic (claude-3-5-sonnet)
- Archivo `env` en la raíz del proyecto con las credenciales de Zernio (o `.env` equivalente)

## Instalación

1. Clonar el repositorio:
```bash
git clone <repo-url>
cd dashboard-instagram
```

2. Crear entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install streamlit pandas plotly python-dotenv anthropic httpx
```

4. Configurar variables de entorno:
```bash
# Editar el archivo `env` (o `.env`) con tus claves API
```

## Cómo ejecutar

```bash
source .venv/bin/activate
streamlit run app.py --server.port=8501
```

El dashboard estará disponible en http://localhost:8501

### Controles principales

- **🔄 Refrescar datos**: invalida la caché y vuelve a consultar la API.
- **🌙 / ☀️**: alterna entre theme oscuro y claro.

## Refrescado de datos

- Botón "🔄 Refrescar datos" en la interfaz de usuario
- Ejecutar manualmente: `python refresh.py`

## Generación de ideas

1. Ir a la pestaña "Ideas"
2. Seleccionar plataforma (Instagram, YouTube o Ambas)
3. Clic en el botón "Generar ideas"
4. Ver ideas generadas en el panel central
5. Descartar ideas con el botón "Descartar" y proporcionando razón

## Troubleshooting

| Error | Solución |
|-------|----------|
| ValueError: ZERNIO_API_KEY must be provided | Configurar ZERNIO_API_KEY en .env |
| StreamlitDuplicateElementId | Añadido unique keys a todos los plotly_chart |
| anthropic.APIError | Verificar API key de Anthropic y conexión a internet |
| KeyError: 'audience_ig' | Verificar que las rutas de datos estén configuradas correctamente |
| ModuleNotFoundError: 'streamlit' | Verificar que el entorno virtual esté activo |
| plotly.exceptions.PlotlyError | Revisar estructura de datos para gráficos |
| FileNotFoundError: [Errno 2] No such file or directory | Asegurar que las rutas a archivos existen |

## Documentación Completa

Este proyecto incluye documentación exhaustiva en la carpeta `docs/`:

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitectura general, flujos de datos, componentes
- **[docs/SETUP.md](docs/SETUP.md)** - Instalación paso a paso, configuración, troubleshooting
- **[docs/API_GUIDE.md](docs/API_GUIDE.md)** - Guía completa de endpoints Zernio, ejemplos de respuesta
- **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Para desarrolladores: testing, conventions, agregar features
- **[docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** - Referencia rápida, comandos, snippets

## Personalización

Los siguientes ejemplos muestran cómo personalizar el sistema:
- Modificar prompt en `prompts/ideas_system.md`
- Cambiar reglas de filtrado de comentarios en `src/components/idea_filters.py`
- Adaptar métricas para diferentes plataformas en `src/data/loader.py`
- Crear nuevas pestañas heredando de `BaseTab`
- Agregar nuevos endpoints del cliente Zernio
