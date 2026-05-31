# Arquitectura del Dashboard Instagram

## Vista General

El Dashboard Instagram es una aplicación web interactiva construida con **Streamlit** que proporciona análisis detallados de métricas de Instagram mediante integración con la API de **Zernio**.

## Stack Tecnológico

### Dependencias Principales
- **Streamlit 1.39.0** - Framework para interfaces interactivas
- **Pandas 2.2.3** - Procesamiento y manipulación de datos
- **Plotly 5.24.0** - Visualización de gráficos interactivos
- **Anthropic 0.97.0** - Generación de ideas con Claude AI
- **Requests 2.32.3** - Cliente HTTP para API
- **Python-dotenv 1.0.1** - Manejo de variables de entorno
- **HTTPx 0.28.1** - Cliente HTTP asíncrono

### Requisitos del Sistema
- Python 3.9+
- Conexión a Internet
- Variables de entorno configuradas

## Estructura del Proyecto

```
dashboard_instagram/
├── app.py                          # Punto de entrada principal
├── cache.py                        # Gestión de caché local (SQLite)
├── requirements.txt                # Dependencias del proyecto
├── env                            # Variables de entorno (NO en git)
├── .env                           # Variables de entorno alternativas
│
├── src/
│   ├── api/
│   │   └── client.py              # Cliente Zernio API
│   │
│   ├── components/
│   │   ├── theme.py               # Tema visual y branding
│   │   ├── ideas.py               # Lógica de generación de ideas
│   │   ├── idea_filters.py        # Filtrado de spam/adoración
│   │   │
│   │   └── tabs/                  # Pestañas del dashboard
│   │       ├── __init__.py
│   │       ├── base_tab.py        # Clase abstracta base
│   │       ├── metrics_tab.py     # KPIs y resumen
│   │       ├── health_tab.py      # Salud de la cuenta
│   │       ├── audience_tab.py    # Audiencia y demografía
│   │       ├── posts_tab.py       # Posts y análisis
│   │       ├── best_time_tab.py   # Mejores horas para publicar
│   │       ├── frequency_tab.py   # Frecuencia de publicación
│   │       └── ideas_tab.py       # Generación de ideas con IA
│   │
│   └── data/
│       └── loader.py              # Carga de datos desde Zernio
│
├── prompts/
│   └── ideas_system.md            # Prompt del sistema para Claude
│
└── docs/
    ├── ARCHITECTURE.md             # Este archivo
    ├── SETUP.md                    # Instrucciones de instalación
    ├── API_GUIDE.md                # Guía de la API Zernio
    └── DEVELOPMENT.md              # Guía para desarrolladores
```

## Flujo de Datos

```
┌─────────────────┐
│  app.py inicia  │
└────────┬────────┘
         │
         ├─► load_dotenv() - Cargar variables de entorno
         │
         ├─► init_db() - Inicializar caché SQLite
         │
         ├─► load_account_data() - Cargar datos
         │   │
         │   └─► load_account_data_from_zernio_with_fallback()
         │       │
         │       ├─► ZernioClient.list_accounts()
         │       ├─► ZernioClient.get_analytics()
         │       ├─► ZernioClient.get_daily_metrics()
         │       ├─► ZernioClient.get_demographics()
         │       └─► ... (otros endpoints)
         │
         ├─► Normalización de datos
         │
         └─► Renderizar pestañas
             ├─► MetricsTab
             ├─► HealthTab
             ├─► AudienceTab
             ├─► PostsTab
             ├─► BestTimeTab
             ├─► FrequencyTab
             └─► IdeasTab
```

## Componentes Principales

### 1. Client API (src/api/client.py)
Interfaz hacia la API de Zernio con:
- **Retry logic** - Reintentos automáticos con backoff exponencial
- **Error handling** - Manejo específico de errores de autenticación y add-ons
- **Endpoints validados** - Mapping de todos los endpoints disponibles

**Métodos principales:**
- `list_accounts()` - Lista cuentas conectadas
- `get_analytics()` - Posts analíticos
- `get_daily_metrics()` - Métricas diarias
- `get_demographics()` - Datos demográficos
- `get_best_time_to_post()` - Horarios óptimos
- `get_posting_frequency()` - Frecuencia de posts
- `get_content_decay()` - Decaimiento de engagement

### 2. Data Loader (src/data/loader.py)
Carga y normaliza datos desde Zernio:
- **Fallback defensivo** - Retorna datos por defecto si la API falla
- **Normalización flexible** - Adaptación a múltiples formatos de respuesta
- **Extracción inteligente** - Identifica el tipo de dato en respuestas complejas

**Función principal:**
```python
load_account_data_from_zernio_with_fallback() -> dict
```

### 3. Pestañas (src/components/tabs/)
Arquitectura basada en herencia de `BaseTab`:
- Cada pestaña implementa `label` y `render()`
- Acceso eficiente a datos compartidos
- Renderización independiente en Streamlit

**Pestañas disponibles:**
1. **MetricsTab** - KPIs clave (seguidores, engagement, reach)
2. **HealthTab** - Estado de la cuenta (tokens, scopes, restricciones)
3. **AudienceTab** - Demografía (edad, género, país, ciudad)
4. **PostsTab** - Lista de posts con estadísticas
5. **BestTimeTab** - Heatmap de mejores horas/días
6. **FrequencyTab** - Relación entre frecuencia y engagement
7. **IdeasTab** - Generación de ideas con Claude

### 4. Ideas with AI (src/components/ideas.py)
Generación de contenido usando Claude:
- Integración con Anthropic API
- Fallback ideas si API no está disponible
- Filtrado de comentarios spam/adoración

### 5. Caché Local (cache.py)
Persistencia de datos en SQLite:
- Almacenamiento de health check
- Reducción de llamadas a API
- Recuperación de datos offline

## Mapeo de Datos

### account_snapshot
Resumen instantáneo de la cuenta:
```python
{
    "id": str,                      # ID de la cuenta
    "platform": str,                # "instagram"
    "username": str,                # @username
    "follower_count": int,          # Número de seguidores
    "followers_count": int,         # Duplicado para compatibilidad
    "posts_count": int,             # Número de posts
    "engagement_rate": float,       # % de engagement
    "reach": int,                   # Alcance en última métrica
    "profile_image": str,           # URL de foto
    "updated_at": str,              # ISO timestamp
}
```

### daily_metrics
Métricas diarias normalizadas:
```python
[
    {
        "date": str,                # YYYY-MM-DD
        "reach": int,               # Cuentas alcanzadas
        "engagements": int,         # Interacciones totales
        "engagement_rate": float,   # %
    },
    ...
]
```

### demographics
Segmentación de audiencia:
```python
{
    "instagram": {
        "age": [{"label": "18-24", "count": 150, "pct": 25.0}, ...],
        "gender": [{"label": "Female", "count": 300, "pct": 50.0}, ...],
        "country": [...],
        "city": [...],
    },
    "youtube": {
        "age": [...],
        "gender": [...],
        "country": [...],
    }
}
```

## Gestión de Errores

### Niveles de resiliencia

1. **API Call** - Retry automático con backoff exponencial (3 intentos)
2. **Data Normalization** - Extracción flexible de múltiples formatos
3. **Fallback Data** - Estructura por defecto si todo falla
4. **UI Rendering** - Componentes adaptativos a datos vacíos

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AuthError` | API key inválida | Verificar `ZERNIO_API_KEY` |
| `AddonRequiredError` | Endpoint requiere add-on | Activar en Zernio console |
| `KeyError` | Estructura de datos inesperada | Verificar normalización en loader |
| `StreamlitDuplicateElementId` | Múltiples gráficos sin key | Añadir `key=` a st.plotly_chart |

## Performance y Caché

### Caché Streamlit
- **TTL**: 300 segundos (5 minutos)
- **Clave**: `load_account_data()`
- **Invalidación**: Botón "🔄 Refrescar"

### Caché SQLite
- Almacena health checks
- Facilita visualización offline
- No es caché primaria

## Vista de Usuario

```
┌─────────────────────────────────────────────┐
│  📊 Dashboard de Instagram  🔄 🌙/☀️       │
│  Última sincronización: 2024-05-31 14:30    │
├─────────────────────────────────────────────┤
│ Tabs: [Métricas] [Salud] [Audiencia] ... |
├─────────────────────────────────────────────┤
│                                             │
│  Contenido de pestaña activa               │
│  - Gráficos con Plotly                    │
│  - Tablas con datos                       │
│  - Controles interactivos                 │
│                                             │
└─────────────────────────────────────────────┘
```

## Configuración de Entorno

Archivo `env` o `.env`:
```bash
# API Zernio
ZERNIO_API_KEY=sk_...
ZERNIO_ACCOUNT_ID=acc_...
ZERNIO_ACCOUNT_ID_YOUTUBE=acc_...

# API Anthropic (para generación de ideas)
ANTHROPIC_API_KEY=sk-ant-...
```

## Mejoras Futuras

- [ ] Caché distribuido (Redis)
- [ ] Dashboard export a PDF
- [ ] Predicción con ML
- [ ] Integración con Google Analytics
- [ ] Programación de posts
- [ ] Análisis competitive

