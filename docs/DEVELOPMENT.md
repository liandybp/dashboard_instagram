# Guía para Desarrolladores

## Configuración del Entorno de Desarrollo

### Requirements adicionales

```bash
pip install pytest pytest-mock black mypy
```

### IDE Recomendado

- **PyCharm** (Community o Professional)
- **VS Code** con extensiones:
  - Python (Microsoft)
  - Pylance
  - Black Formatter

## Estructura de Código

### Convenciones de Nombres

```python
# Variables
account_id = "acc_123"           # snake_case
followers_count = 5000

# Funciones/métodos
def load_account_data():         # snake_case
    pass

def _private_helper():           # prefijo _ para privadas
    pass

# Clases
class ZernioClient:              # PascalCase
    pass

class BaseTab(ABC):
    pass

# Constantes
BASE_URL = "https://..."         # UPPER_CASE
MAX_RETRIES = 3
```

### Tipos y Docstrings

```python
from typing import Dict, List, Optional

def normalize_metrics(items: List[Dict]) -> List[Dict]:
    """
    Normaliza métricas diarias desde API de Zernio.
    
    Args:
        items: Lista de dicts con métricas raw de Zernio
        
    Returns:
        Lista de dicts normalizados con keys: date, reach, engagement_rate
        
    Raises:
        TypeError: Si items no es lista
        
    Example:
        >>> raw = [{"date": "2024-05-30", "reach": 5000}]
        >>> result = normalize_metrics(raw)
        >>> result[0]["reach"]
        5000
    """
    if not isinstance(items, list):
        raise TypeError("items debe ser una lista")
    # ...
```

## Agregar una Nueva Pestaña

### 1. Crear archivo de pestaña

`src/components/tabs/my_tab.py`:
```python
import streamlit as st
from src.components.tabs.base_tab import BaseTab

class MyTab(BaseTab):
    @property
    def label(self) -> str:
        return "📊 Mi Pestaña"
    
    def render(self) -> None:
        """Renderiza el contenido de la pestaña."""
        st.header("Mi Pestaña")
        
        # Acceso a datos
        data = self.data
        posts = data.get("posts", [])
        
        # Renderizar
        st.write(f"Total posts: {len(posts)}")
        
        # Gráfico con key único
        st.plotly_chart(fig, use_column_width=True, key="my_tab_chart_1")
```

### 2. Importar en `__init__.py`

`src/components/tabs/__init__.py`:
```python
from src.components.tabs.my_tab import MyTab

__all__ = [
    "MetricsTab",
    "HealthTab",
    "MyTab",  # Nueva
    # ...
]
```

### 3. Agregar a `app.py`

```python
from src.components.tabs import (
    MetricsTab,
    HealthTab,
    # ...
    MyTab,  # Nueva
)

# En main():
tab_objects = [
    MetricsTab(data),
    HealthTab(data),
    # ...
    MyTab(data),  # Nueva
]
```

## Agregar un Nouvelle Endpoint Zernio

### 1. Añadir método al cliente

`src/api/client.py`:
```python
def get_my_data(self, account_id=None, platform="instagram"):
    """
    GET /v1/analytics/my-endpoint
    Descripción de datos retornados.
    """
    account_id = account_id or self.account_id_instagram
    params = {"platform": platform}
    if account_id:
        params["accountId"] = account_id
    return self._request("GET", "/analytics/my-endpoint", params=params)
```

### 2. Normalizar en loader

`src/data/loader.py`:
```python
# En load_account_data_from_zernio_with_fallback():

try:
    my_data_result = client.get_my_data(account_id=account_id)
except AddonRequiredError as e:
    print(f"Add-on requerido: {e}")
    my_data_result = {"data": []}
except Exception as e:
    print(f"Error cargando datos: {e}")
    my_data_result = {"data": []}

# Normalizar
my_data = _normalize_my_data(
    _extract_list(my_data_result, ["data", "items", "rows"])
)

# En return final:
return {
    # ... otros datos ...
    "my_data": my_data,
}

# Nueva función normalizadora:
def _normalize_my_data(items: list):
    """Normaliza respuesta de mi endpoint."""
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        # Mapeo flexible de campos
        normalized.append({
            "field1": item.get("field1"),
            "field2": _to_float(item.get("field2"), 0),
        })
    return normalized
```

### 3. Usar en tab nueva

```python
def render(self) -> None:
    my_data = self.data.get("my_data", [])
    st.write(my_data)
```

## Testing

### Unit Tests

```python
# tests/test_loader.py
import pytest
from src.data.loader import _normalize_daily_metrics

def test_normalize_daily_metrics():
    raw = [
        {
            "date": "2024-05-30",
            "reach": 5000,
            "engagements": 150,
            "engagement_rate": 3.0
        }
    ]
    result = _normalize_daily_metrics(raw)
    
    assert len(result) == 1
    assert result[0]["reach"] == 5000
    assert result[0]["engagement_rate"] == 3.0

def test_normalize_empty_list():
    result = _normalize_daily_metrics([])
    assert result == []

def test_normalize_invalid_types():
    result = _normalize_daily_metrics(["not", "a", "dict"])
    assert result == []
```

### Ejecutar tests

```bash
pytest tests/ -v
pytest tests/test_loader.py::test_normalize_daily_metrics -v
pytest tests/ --cov=src --cov-report=html
```

## Debugging

### Logs de Streamlit

```bash
streamlit run app.py --logger.level=debug
```

### Print debugging

```python
import sys
print("Debug info", file=sys.stderr)  # No interfiere con Streamlit
```

### Browser DevTools

```python
# En una pestaña
st.write(data)  # Expande data en el navegador
```

### Validar API

```bash
python src/api/client.py
```

## Performance

### Caché Streamlit

```python
@st.cache_data(ttl=300)
def load_expensive_data():
    # Solo se ejecuta cada 5 minutos
    return expensive_operation()

# Invalidar
load_expensive_data.clear()
```

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... código a medir ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative").print_stats(10)
```

## Code Style

### Black formatting

```bash
# Format archivo
black src/api/client.py

# Format todo el proyecto
black .

# Dry run
black --check src/
```

### Mypy type checking

```bash
# Check tipos
mypy src/

# Configurar en mypy.ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
```

## Documentación de Código

### Docstring format (Google style)

```python
def calculate_engagement_rate(like_count: int, reach: int) -> float:
    """
    Calcula tasa de engagement como porcentaje.
    
    Args:
        like_count: Número de likes
        reach: Alcance del post
        
    Returns:
        Tasa de engagement como % (0-100)
        
    Raises:
        ValueError: Si reach es <= 0
        
    Example:
        >>> calculate_engagement_rate(100, 5000)
        2.0
    """
    if reach <= 0:
        raise ValueError("Reach debe ser > 0")
    return (like_count / reach) * 100
```

## Git Workflow

### Branches

```bash
# feature branch
git checkout -b feature/new-tab

# Fix branch
git checkout -b fix/bug-description

# Release
git checkout -b release/1.0.0
```

### Commits

```bash
# Commits semánticos
git commit -m "feat: agregar nueva pestaña de analytics"
git commit -m "fix: corregir error de caché"
git commit -m "docs: actualizar README"
git commit -m "refactor: mejorar normalización de datos"
git commit -m "test: agregar tests para loader"
```

### Pull Request Template

```markdown
## Descripción
Breve descripción de cambios

## Tipo de Cambio
- [ ] Feature (nueva funcionalidad)
- [ ] Fix (corrección de bug)
- [ ] Refactor (mejora de código)
- [ ] Docs (documentación)

## Testing
- [ ] Tests unitarios pasados
- [ ] Dashboard funciona localmente
- [ ] Sin errores en consola

## Checklist
- [ ] Código formateado con Black
- [ ] Tipos chequeados con Mypy
- [ ] Docstrings actualizados
- [ ] No hay credenciales en el código
```

## Problemas Comunes en Desarrollo

### ImportError
```python
# ❌ Incorrecto - ruta relativa
from data.loader import load_account_data

# ✅ Correcto - desde raíz del proyecto
from src.data.loader import load_account_data
```

### StreamlitDuplicateElementId
```python
# ❌ Incorrecto - sin key única
st.plotly_chart(fig)
st.plotly_chart(fig2)

# ✅ Correcto - con keys distintas
st.plotly_chart(fig, key="chart_1")
st.plotly_chart(fig2, key="chart_2")
```

### Cache invalidation
```python
# ❌ No limpia
st.cache_data.clear()

# ✅ Especifica función
load_account_data.clear()
```

## Mejoras de Código Sugeridas

1. **Logging** - Agregar logging estructurado con `logging` module
2. **Tipos** - Migrar a TypedDict para estructuras de datos
3. **Tests** - Coverage > 80%
4. **Async** - Usar `httpx` asincrónico para múltiples requests paralelos
5. **CLI** - Agregar CLI con `click` para operaciones administrativas

## Referencias

- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Python](https://plotly.com/python)
- [Pandas Docs](https://pandas.pydata.org/docs)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

