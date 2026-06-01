# Diagnóstico: Datos Vacíos en Algunas Pestañas

**Fecha:** 31 de Mayo de 2026  
**Issue:** Pestaña Posts y otras muestran datos vacíos

---

## Análisis del Problema

### Estado Actual
- ✅ Credenciales de Zernio configuradas en `env`
- ✅ Cliente API implementado (`src/api/client.py`)
- ✅ Loader de datos implementado (`src/data/loader.py`)
- ❌ Posts pestaña muestra contenedor vacío
- ❌ Otras pestañas pueden tener datos parciales o vacíos

---

## Causas Posibles

### 1. **Endpoint de Posts No Funciona Correctamente**
   - **Archivo:** `src/api/client.py` línea 136 (`get_analytics()`)
   - **Problema:** El endpoint `/analytics` puede requerir parámetros específicos
   - **Solución:** Verificar respuesta real de la API

### 2. **Los Datos se Cargan pero el Formato es Incorrecto**
   - **Archivo:** `src/data/loader.py` línea 474 (`get_analytics()`)
   - **El loader intenta extraer:**
     ```python
     posts = _extract_list(posts_result, ["posts", "data", "items", "analytics"])
     ```
   - **Problema:** Si la respuesta tiene otra estructura, no se extraen los datos

### 3. **Falta de Add-ons Activos en Zernio**
   - Muchos endpoints requieren add-ons pagos
   - Si no están activados, la API retorna status 402 ó 403
   - Fallback automático a datos vacíos

### 4. **Account ID Incorrecto o Sin Permisos**
   - El `ZERNIO_ACCOUNT_ID` puede ser inválido
   - La cuenta conectada puede no tener permisos suficientes

---

## Soluciones Paso a Paso

### **Solución 1: Verificar Respuesta Real de la API**

Ejecutar este test:

```bash
cd /Users/t022458/PycharmProjects/personal/dashboard_instagram
python3 << 'EOF'
import os
from src.api.client import ZernioClient
from dotenv import load_dotenv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / "env", override=True)

try:
    client = ZernioClient()
    print("✓ Cliente inicializado")
    
    # Test 1: List accounts
    print("\n1. ACCOUNTS:")
    accounts = client.list_accounts()
    print(f"  Respuesta keys: {list(accounts.keys()) if isinstance(accounts, dict) else 'lista'}")
    if isinstance(accounts, dict) and 'data' in accounts:
        print(f"  Data items: {len(accounts['data'])}")
    
    # Test 2: Get analytics (posts)
    account_id = os.getenv("ZERNIO_ACCOUNT_ID")
    if account_id:
        print(f"\n2. ANALYTICS (Account: {account_id[:8]}...):")
        try:
            posts = client.get_analytics(platform="instagram", account_id=account_id)
            print(f"  Respuesta keys: {list(posts.keys())}")
            if isinstance(posts, dict) and 'data' in posts:
                print(f"  Posts encontrados: {len(posts['data'])}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test 3: Get demographics
    print(f"\n3. DEMOGRAPHICS:")
    try:
        demo = client.get_demographics(account_id=account_id, breakdown="country")
        print(f"  Respuesta keys: {list(demo.keys())}")
        if isinstance(demo, dict) and 'data' in demo:
            print(f"  Países encontrados: {len(demo['data'])}")
    except Exception as e:
        print(f"  Error: {e}")
        
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

---

### **Solución 2: Actualizar Fallback Data para Posts**

Si la API no retorna posts, al menos mostrar datos demo:

**Archivo:** `src/data/loader.py` línea 23

Actualizar `_build_fallback_data()` para incluir posts de demostración:

```python
def _build_fallback_data(reason: str = ""):
    # ... código existente ...
    return {
        # ... otros campos ...
        "posts": [
            {
                "id": "post_1",
                "caption": "Post de ejemplo 1",
                "likes_count": 150,
                "comments_count": 25,
                "saves": 12,
                "reach": 1200,
                "thumbnail_url": "https://via.placeholder.com/300",
                "permalink": "https://instagram.com/p/placeholder1",
            },
            {
                "id": "post_2",
                "caption": "Post de ejemplo 2",
                "likes_count": 240,
                "comments_count": 45,
                "saves": 18,
                "reach": 2100,
                "thumbnail_url": "https://via.placeholder.com/300",
                "permalink": "https://instagram.com/p/placeholder2",
            },
            # ... más posts ...
        ],
        # ... otros campos ...
    }
```

---

### **Solución 3: Diagnosticar Add-ons Requeridos**

Verificar qué endpoints requieren add-ons:

```bash
cd /Users/t022458/PycharmProjects/personal/dashboard_instagram
python3 src/data/loader.py 2>&1 | grep -i "addon"
```

Si ves mensajes como:
```
Addon required for posts: Add-on requerido para: /analytics
```

Significa que ese endpoint requiere un add-on de pago en Zernio.

---

### **Solución 4: Verificar Account ID**

```bash
cd /Users/t022458/PycharmProjects/personal/dashboard_instagram
python3 << 'EOF'
import os
from src.api.client import ZernioClient
from dotenv import load_dotenv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / "env", override=True)

client = ZernioClient()
accounts = client.list_accounts()

if isinstance(accounts, dict) and 'data' in accounts:
    print("Cuentas disponibles:")
    for acc in accounts['data']:
        print(f"  - {acc.get('username')} ({acc.get('platform')}) ID: {acc.get('_id') or acc.get('id')}")
else:
    print(f"Respuesta inesperada: {type(accounts)}")
EOF
```

---

## Checklist para Diagnosticar

- [ ] Ejecutar test de API (Solución 1)
- [ ] Ver qué endpoints retornan datos
- [ ] Ver qué endpoints dan error 402/403 (addon required)
- [ ] Verificar account IDs correctos
- [ ] Si todo falla, implementar fallback data (Solución 2)

---

## Resultado Esperado

Si el diagnóstico muestra que la API retorna datos vacíos, deberías:

1. **Contactar a Zernio** para verificar:
   - Si los add-ons están activos en tu cuenta
   - Si la cuenta está correctamente conectada
   - Si hay datos disponibles para este account ID

2. **Implementar fallback data** para que al menos haya datos demo en el dashboard

3. **Documentar qué endpoints funcionan y cuáles no** para futuro desarrollo

---

## Archivos Relacionados

- `src/api/client.py` - Cliente de API
- `src/data/loader.py` - Cargador de datos
- `env` - Variables de entorno (ZERNIO_API_KEY, ZERNIO_ACCOUNT_ID)

---

**Status:** 🔴 Requiere investigación y acción

