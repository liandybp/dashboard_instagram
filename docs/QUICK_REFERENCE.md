# Quick Reference - Referencia Rápida

## Comandos Más Usados

```bash
# Ejecutar dashboard
streamlit run app.py

# Con puerto custom
streamlit run app.py --server.port=8502

# Validar endpoints API
python src/api/client.py

# Verificar variables de entorno
python show_env.py
```

## Estructura de Datos Principal

```python
# Objeto data retornado por load_account_data()
{
    "account_snapshot": {       # Info de cuenta actual
        "id": str,
        "username": str,
        "followers_count": int,
        "posts_count": int,
        "engagement_rate": float,
        "reach": int,
        "updated_at": str,
    },
    
    "account_health": {         # Estado de la cuenta
        "status": str,
        "token_valid": bool,
        "is_active": bool,
        "issues": list,
    },
    
    "daily_metrics": [          # Métricas por día
        {
            "date": str,        # YYYY-MM-DD
            "reach": int,
            "engagements": int,
            "engagement_rate": float,
        }
    ],
    
    "demographics": {           # Audiencia
        "instagram": {
            "age": [{"label": "18-24", "count": 150, "pct": 25.0}],
            "gender": [...],
            "country": [...],
            "city": [...],
        }
    },
    
    "best_time_to_post": [      # Horarios óptimos
        {
            "day_of_week": str,  # "Lunes"
            "hour": int,         # 0-23
            "value": float,      # engagement avg
        }
    ],
    
    "posting_frequency": [      # Frecuencia vs engagement
        {
            "posts_per_week": float,
            "avg_engagement_rate": float,
        }
    ],
    
    "posts": [                  # Posts individuales
        {
            "id": str,
            "caption": str,
            "likes": int,
            "comments": int,
            "reach": int,
            "engagement_rate": float,
        }
    ],
    
    "comments": [               # Comentarios recientes
        {
            "author": str,
            "text": str,
            "timestamp": str,
        }
    ],
}
```

## Variables de Entorno

```bash
# Requerido
ZERNIO_API_KEY=sk_live_xxxxx
ZERNIO_ACCOUNT_ID=acc_xxxxx

# Opcional
ZERNIO_ACCOUNT_ID_YOUTUBE=acc_xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## Pestañas del Dashboard

| Pestaña | Archivo | Función |
|---------|---------|---------|
| 📈 Métricas | `metrics_tab.py` | KPIs principales |
| 🏥 Salud | `health_tab.py` | Status de cuenta |
| 👥 Audiencia | `audience_tab.py` | Demografía |
| 📱 Posts | `posts_tab.py` | Lista de posts |
| ⏰ Mejor Hora | `best_time_tab.py` | Heatmap horario |
| 📊 Frecuencia | `frequency_tab.py` | Posts/week vs engagement |
| 💡 Ideas | `ideas_tab.py` | IA generación de contenido |

## Métodos del Cliente Zernio

```python
from src.api.client import ZernioClient

client = ZernioClient()

# Cuentas
client.list_accounts()

# Analíticas
client.get_analytics()                          # Posts con métricas
client.get_daily_metrics()                      # Métricas diarias
client.get_best_time_to_post()                  # Mejores horarios
client.get_posting_frequency()                  # Frecuencia
client.get_content_decay()                      # Decaimiento engagement

# Instagram específico
client.get_instagram_account_insights()         # Health check
client.get_demographics(breakdown="age")        # Audiencia

# Seguidores y comentarios
client.get_follower_stats()                    # Historial
client.list_inbox_comments()                   # Comentarios
```

## Normalización de Datos

```python
from src.data.loader import (
    _normalize_daily_metrics,
    _normalize_demographics,
    _normalize_best_time,
    _normalize_posting_frequency,
    _extract_list,
)

# Ejemplo
raw_data = client.get_daily_metrics()
metrics = _normalize_daily_metrics(
    _extract_list(raw_data, ["data", "metrics"])
)
```

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: ZERNIO_API_KEY...` | Variable no configurada | Crear archivo `env` o `.env` |
| `StreamlitDuplicateElementId` | Múltiples gráficos sin key | Agregar `key=` a st.plotly_chart |
| `AddonRequiredError` | Endpoint requiere add-on | Activar en [Zernio console](https://app.zernio.com) |
| `AuthError` | API key inválida | Verificar key en Zernio dashboard |
| `ConnectionError` | Sin conexión a internet | Verificar conexión y proxy |

## Añadir Gráfico Plotly

```python
import plotly.express as px
import streamlit as st

# Crear figura
fig = px.line(
    data_frame=df,
    x="date",
    y="reach",
    title="Alcance Diario"
)

# Renderizar con key única
st.plotly_chart(fig, use_column_width=True, key="reach_chart")
```

## Usar Variables de Sesión

```python
import streamlit as st

# Guardar
st.session_state["mi_variable"] = valor

# Recuperar
mi_valor = st.session_state.get("mi_variable", default)

# Editar
if st.button("Actualizar"):
    st.session_state["mi_variable"] = nuevo_valor
    st.rerun()
```

## Caché en Streamlit

```python
import streamlit as st

# Cache de 5 minutos
@st.cache_data(ttl=300)
def load_data():
    return expensive_operation()

# Usable
data = load_data()

# Limpiar caché
load_data.clear()
st.rerun()
```

## Agregar Nueva Pestaña (5 min)

1. Crear `src/components/tabs/my_tab.py`:
```python
from src.components.tabs.base_tab import BaseTab

class MyTab(BaseTab):
    @property
    def label(self) -> str:
        return "📊 Mi Pestaña"
    
    def render(self) -> None:
        st.header("Mi Pestaña")
        st.write(self.data)
```

2. Importar en `src/components/tabs/__init__.py`:
```python
from src.components.tabs.my_tab import MyTab
__all__ = [..., "MyTab"]
```

3. Usar en `app.py`:
```python
from src.components.tabs import MyTab
# En main(): tab_objects = [..., MyTab(data)]
```

## Agregar Nuevo Endpoint (10 min)

1. Agregar método en `src/api/client.py`:
```python
def get_my_data(self, account_id=None):
    account_id = account_id or self.account_id_instagram
    return self._request("GET", "/my-endpoint", params={"accountId": account_id})
```

2. Cargar en `src/data/loader.py`:
```python
try:
    my_result = client.get_my_data()
except:
    my_result = {}

my_data = _normalize_my_data(_extract_list(my_result, ["data"]))
```

3. Retornar en datos:
```python
return {
    # ...
    "my_data": my_data,
}
```

## Streamlit CLI

```bash
# Ejecutar con opciones
streamlit run app.py \
  --server.port=8501 \
  --server.headless=true \
  --logger.level=info \
  --client.toolbarMode=minimal

# Configurar servidor
streamlit config show
streamlit config show --all
```

## Variables CSS/Tema

En `src/components/theme.py`:
```python
BRAND_COLORS = {
    "primary": "#FF355C",
    "secondary": "#00A4FF",
    "success": "#2ECC71",
    "warning": "#F39C12",
    "danger": "#E74C3C",
}
```

## Testing de Endpoints

```bash
# Validar todos funcionan
python src/api/client.py

# Output esperado:
# ✅ List Accounts: SUCCESS
# ✅ Post Analytics: SUCCESS
# ⚠️  Daily Metrics: ADD-ON REQUERIDO
```

## Deploy a Streamlit Cloud

1. Push a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar repo
4. Secrets en Settings:
```
ZERNIO_API_KEY=sk_live_xxx
ZERNIO_ACCOUNT_ID=acc_xxx
ANTHROPIC_API_KEY=sk-ant-xxx
```

## Documentación Completa

- **ARCHITECTURE.md** - Diseño y flujos
- **SETUP.md** - Instalación paso a paso
- **API_GUIDE.md** - Endpoints de Zernio
- **DEVELOPMENT.md** - Guía para desarrolladores
- **CLAUDE.md** - Notas del proyecto (en raíz)

## Soporte Rápido

```bash
# Verificar todo está OK
python src/api/client.py    # APIs
python src/data/loader.py   # Data loading
streamlit run app.py                # UI

# Debug
streamlit run app.py --logger.level=debug
```

