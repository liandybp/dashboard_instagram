# Guía de integración con la API de Zernio
### Para el dashboard de análisis de Instagram (`dashboard_instagram`)

> Basada en la documentación oficial: https://docs.zernio.com  
> Base URL real de la API: `https://zernio.com/api/v1`

---

## ⚠️ Corrección importante respecto al PDF original

El PDF de referencia menciona `https://api.zernio.com/v1` como base URL y endpoints como
`/analytics/instagram/demographics` o `/analytics/daily-metrics` que **no existen** en la
API real. La URL y los endpoints correctos son los que aparecen en esta guía.

---

## Paso 1 — Crear cuenta y obtener API Key

1. Ve a [zernio.com](https://zernio.com) y crea una cuenta
2. En el dashboard, ve a **Settings → API Keys**
3. Haz clic en **Create API Key** y ponle un nombre (ej: `dashboard-instagram`)
4. **Copia la key inmediatamente** — solo se muestra una vez
   - Formato: `sk_` + 64 caracteres hexadecimales (67 en total)
5. Guárdala en un lugar temporal seguro hasta configurar el `.env`

> Si necesitas los add-ons de **Analytics** e **Inbox**, actívalos desde el panel de Zernio
> antes de continuar. Sin ellos verás errores `402` al llamar esos endpoints.

---

## Paso 2 — Configurar el `.env`

En la raíz del proyecto `dashboard_instagram/`, crea o edita el archivo `.env`:

```env
ZERNIO_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ZERNIO_ACCOUNT_ID=           # se rellena en el Paso 4
ZERNIO_ACCOUNT_ID_YOUTUBE=   # opcional, vacío si no tienes YouTube
ANTHROPIC_API_KEY=sk-ant-api03-...
DASHBOARD_TZ=Europe/Madrid
```

Y asegúrate de que `.gitignore` incluye `.env` para no subir las keys a git.

---

## Paso 3 — Instalar el SDK de Python

Con el entorno virtual activado:

```bash
# Activar el venv si no está activo
source .venv/bin/activate

# Instalar el SDK oficial de Zernio
pip install zernio-sdk

# Verificar instalación
python -c "from zernio import Zernio; print('OK')"
```

> El SDK lee `ZERNIO_API_KEY` del entorno automáticamente cuando usas `Zernio()` sin argumentos.

---

## Paso 4 — Obtener tu Account ID (fetch automático)

Este script obtiene tu `account_id` de Instagram (y YouTube si aplica) y lo imprime para
que puedas pegarlo en el `.env`. Ejecuta una sola vez.

```python
# scripts/fetch_account_ids.py
import os
from dotenv import load_dotenv

load_dotenv(override=True)  # override=True es OBLIGATORIO

from zernio import Zernio

client = Zernio()  # usa ZERNIO_API_KEY del entorno

# Listar todas las cuentas conectadas
result = client.accounts.list_accounts()

print("=== Cuentas conectadas en Zernio ===")
for account in result.accounts:
    print(f"  Plataforma : {account['platform']}")
    print(f"  Username   : {account.get('username', 'N/A')}")
    print(f"  Account ID : {account['_id']}")
    print()

# Filtrar solo Instagram
ig_accounts = [a for a in result.accounts if a['platform'] == 'instagram']
yt_accounts = [a for a in result.accounts if a['platform'] == 'youtube']

if ig_accounts:
    print(f"→ Pega esto en tu .env:")
    print(f"  ZERNIO_ACCOUNT_ID={ig_accounts[0]['_id']}")

if yt_accounts:
    print(f"  ZERNIO_ACCOUNT_ID_YOUTUBE={yt_accounts[0]['_id']}")
```

Ejecútalo:

```bash
python scripts/fetch_account_ids.py
```

Copia los IDs al `.env`.

---

## Paso 5 — Implementar `zernio_client.py`

Este es el módulo central que usarás en todo el proyecto. Copia este código como punto de
partida:

```python
# zernio_client.py
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)  # SIEMPRE override=True

BASE_URL = "https://zernio.com/api/v1"


class AuthError(Exception):
    pass


class AddonRequiredError(Exception):
    pass


class ZernioClient:
    def __init__(self):
        self.api_key = os.getenv("ZERNIO_API_KEY")
        if not self.api_key:
            raise AuthError("ZERNIO_API_KEY no está en .env o está vacío")
        self.account_id = os.getenv("ZERNIO_ACCOUNT_ID", "")
        self.account_id_yt = os.getenv("ZERNIO_ACCOUNT_ID_YOUTUBE", "")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _request(self, method: str, path: str, params: dict = None) -> dict:
        """Hace la request con retry exponencial en 5xx y 429."""
        url = f"{BASE_URL}{path}"
        delays = [2, 3, 5, 9]
        last_error = None

        for attempt, delay in enumerate([0] + delays):
            if delay:
                time.sleep(delay)
            try:
                resp = requests.request(
                    method,
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=30,
                )
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 202:
                    return resp.json()  # sync pendiente, OK igualmente
                elif resp.status_code == 401:
                    raise AuthError("API key expirada o inválida. Genera una nueva en zernio.com")
                elif resp.status_code == 402:
                    raise AddonRequiredError("Activa el add-on Analytics en zernio.com")
                elif resp.status_code == 403:
                    raise AddonRequiredError("Activa el add-on Inbox en zernio.com")
                elif resp.status_code in (429, 500, 502, 503, 529):
                    last_error = f"HTTP {resp.status_code}"
                    continue  # reintenta
                else:
                    resp.raise_for_status()
            except (AuthError, AddonRequiredError):
                raise
            except Exception as e:
                last_error = str(e)
                continue

        raise RuntimeError(f"Fallo después de {len(delays)+1} intentos: {last_error}")

    # ── Analytics ─────────────────────────────────────────────────────────────

    def get_analytics(self, platform: str = "instagram", account_id: str = None,
                      from_date: str = None, to_date: str = None,
                      sort_by: str = "engagement", limit: int = 50) -> dict:
        """GET /v1/analytics — métricas de posts con paginación."""
        params = {
            "platform": platform,
            "accountId": account_id or self.account_id,
            "sortBy": sort_by,
            "limit": limit,
        }
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        return self._request("GET", "/analytics", params)

    def get_best_time_to_post(self, account_id: str = None, platform: str = "instagram") -> dict:
        """GET /v1/analytics/best-time — mejor hora para publicar."""
        params = {
            "accountId": account_id or self.account_id,
            "platform": platform,
        }
        return self._request("GET", "/analytics/best-time", params)

    def get_daily_analytics(self, account_id: str = None, platform: str = "instagram",
                            from_date: str = None, to_date: str = None) -> dict:
        """GET /v1/analytics/daily — engagement día a día."""
        params = {
            "accountId": account_id or self.account_id,
            "platform": platform,
        }
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        return self._request("GET", "/analytics/daily", params)

    def get_follower_stats(self, account_id: str = None, platform: str = "instagram") -> dict:
        """GET /v1/accounts/follower-stats — historial de seguidores."""
        params = {
            "accountId": account_id or self.account_id,
            "platform": platform,
        }
        return self._request("GET", "/accounts/follower-stats", params)

    # ── Accounts ──────────────────────────────────────────────────────────────

    def list_accounts(self) -> dict:
        """GET /v1/accounts — lista todas las cuentas conectadas."""
        return self._request("GET", "/accounts")

    def get_account_health(self, account_id: str = None) -> dict:
        """GET /v1/accounts/{id}/health — estado de la cuenta."""
        aid = account_id or self.account_id
        return self._request("GET", f"/accounts/{aid}/health")

    # ── Inbox: Comentarios ────────────────────────────────────────────────────

    def list_comments(self, account_id: str = None, platform: str = "instagram",
                      limit: int = 100) -> dict:
        """GET /v1/comments — comentarios de todos los posts."""
        params = {
            "accountId": account_id or self.account_id,
            "platform": platform,
            "limit": limit,
        }
        return self._request("GET", "/comments", params)

    def get_post_comments(self, post_id: str, account_id: str = None) -> dict:
        """GET /v1/comments/{postId} — comentarios de un post específico."""
        params = {"accountId": account_id or self.account_id}
        return self._request("GET", f"/comments/{post_id}", params)

    # ── Inbox: DMs / Conversaciones ───────────────────────────────────────────

    def list_conversations(self, account_id: str = None, platform: str = "instagram",
                           limit: int = 50) -> dict:
        """GET /v1/messages — lista conversaciones DM (solo Instagram)."""
        params = {
            "accountId": account_id or self.account_id,
            "platform": platform,
            "limit": limit,
        }
        return self._request("GET", "/messages", params)

    def get_conversation_messages(self, conversation_id: str,
                                  account_id: str = None) -> dict:
        """GET /v1/messages/{conversationId} — mensajes de una conversación."""
        params = {"accountId": account_id or self.account_id}
        return self._request("GET", f"/messages/{conversation_id}", params)

    # ── Posts ─────────────────────────────────────────────────────────────────

    def list_posts(self, account_id: str = None, platform: str = "instagram",
                   limit: int = 50) -> dict:
        """GET /v1/analytics — posts con métricas (fuente: analytics endpoint)."""
        return self.get_analytics(
            platform=platform,
            account_id=account_id,
            sort_by="engagement",
            limit=limit,
        )

    # ── YouTube ───────────────────────────────────────────────────────────────

    def get_youtube_analytics(self, from_date: str = None, to_date: str = None) -> dict:
        """GET /v1/analytics — posts de YouTube con métricas."""
        if not self.account_id_yt:
            return {"posts": []}
        return self.get_analytics(
            platform="youtube",
            account_id=self.account_id_yt,
            from_date=from_date,
            to_date=to_date,
        )
```

---

## Paso 6 — Verificar la conexión

Ejecuta este script para confirmar que todo está funcionando:

```python
# scripts/validate_connection.py
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from zernio_client import ZernioClient, AddonRequiredError, AuthError

def validate():
    print("=== Validando conexión con Zernio ===\n")
    try:
        client = ZernioClient()
    except AuthError as e:
        print(f"✗ Error de autenticación: {e}")
        return

    checks = [
        ("Cuentas conectadas",    lambda: client.list_accounts()),
        ("Analytics posts",       lambda: client.get_analytics()),
        ("Mejor hora publicar",   lambda: client.get_best_time_to_post()),
        ("Comentarios inbox",     lambda: client.list_comments()),
        ("DMs / conversaciones",  lambda: client.list_conversations()),
        ("Follower history",      lambda: client.get_follower_stats()),
    ]

    for name, fn in checks:
        try:
            result = fn()
            print(f"  ✓ {name}")
        except AddonRequiredError as e:
            print(f"  ⚠ {name}: {e}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")

    print("\n✓ = OK   ⚠ = necesita add-on   ✗ = error")

if __name__ == "__main__":
    validate()
```

```bash
python scripts/validate_connection.py
```

Resultado esperado:
```
=== Validando conexión con Zernio ===

  ✓ Cuentas conectadas
  ✓ Analytics posts
  ✓ Mejor hora publicar
  ✓ Comentarios inbox
  ✓ DMs / conversaciones
  ✓ Follower history
```

Si ves `⚠`, activa el add-on correspondiente en el panel de Zernio y repite.

---

## Paso 7 — Endpoints disponibles (referencia rápida)

Todos sobre `https://zernio.com/api/v1` con header `Authorization: Bearer {ZERNIO_API_KEY}`.

| Función en `zernio_client.py` | Método | Path | Add-on requerido |
|-------------------------------|--------|------|-----------------|
| `list_accounts()` | GET | `/accounts` | No |
| `get_account_health()` | GET | `/accounts/{id}/health` | No |
| `get_follower_stats()` | GET | `/accounts/follower-stats` | Analytics |
| `get_analytics()` | GET | `/analytics` | Analytics |
| `get_daily_analytics()` | GET | `/analytics/daily` | Analytics |
| `get_best_time_to_post()` | GET | `/analytics/best-time` | Analytics |
| `list_comments()` | GET | `/comments` | Inbox |
| `get_post_comments(post_id)` | GET | `/comments/{postId}` | Inbox |
| `list_conversations()` | GET | `/messages` | Inbox |
| `get_conversation_messages(conv_id)` | GET | `/messages/{id}` | Inbox |

> **IMPORTANTE — solo lectura.** Este dashboard nunca llama endpoints de escritura
> (`POST /posts`, `POST /messages`, etc.). El cliente de arriba no los implementa adrede.

---

## Paso 8 — Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `AuthError: API key expirada` | Key inválida o caducada | Genera nueva en `zernio.com/dashboard/api-keys` |
| `AddonRequiredError: Analytics` | Add-on Analytics no activo | Actívalo en el panel de Zernio |
| `AddonRequiredError: Inbox` | Add-on Inbox no activo | Actívalo en el panel de Zernio |
| `ZERNIO_API_KEY no está en .env` | `load_dotenv` sin `override=True` | Usa siempre `load_dotenv(override=True)` |
| `ConnectionError` / timeout | Red o API caída | El cliente reintenta automáticamente 4 veces |
| Account ID vacío | `.env` sin `ZERNIO_ACCOUNT_ID` | Ejecuta `scripts/fetch_account_ids.py` |
| Solo veo ~25 posts | Limitación de Zernio | Normal — solo expone posts con comentarios |

---

## Resumen de diferencias con el PDF original

| PDF (incorrecto) | API real |
|------------------|----------|
| Base URL: `https://api.zernio.com/v1` | Base URL: `https://zernio.com/api/v1` |
| `GET /analytics/daily-metrics` | `GET /analytics/daily` |
| `GET /analytics/instagram/account-insights` | `GET /analytics` con `?platform=instagram` |
| `GET /analytics/instagram/demographics` | No existe como endpoint separado |
| `GET /inbox/conversations` | `GET /messages` |
| `GET /inbox/comments` | `GET /comments` |
| `GET /analytics/instagram/follower-history` | `GET /accounts/follower-stats` |
| `GET /usage-stats` | `GET /usage` (sección Settings & Admin) |

---

*Documentación generada a partir de `https://docs.zernio.com` — mayo 2026.*
