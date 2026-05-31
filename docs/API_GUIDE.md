# API de Zernio - Guía Completa

## Introducción

Zernio proporciona acceso a datos de redes sociales (Instagram, YouTube, TikTok) a través de su API REST. Este dashboard utiliza la API de Zernio para obtener analíticas, audiencia y contenido.

**Base URL:** `https://zernio.com/api/v1`

**Autenticación:** Bearer token en header `Authorization`

## Endpoints Utilizados

### Autenticación

```http
GET /accounts
Authorization: Bearer {ZERNIO_API_KEY}
```

Retorna lista de cuentas conectadas en la workspace.

**Respuesta:**
```json
{
  "accounts": [
    {
      "id": "acc_123abc",
      "_id": "acc_123abc",
      "platform": "instagram",
      "username": "@micuenta",
      "name": "Mi Nombre",
      "followers_count": 5000,
      "posts_count": 45,
      "verified": false
    }
  ]
}
```

### Analíticas Post-Level

```http
GET /analytics
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - platform: "instagram" | "youtube"
  - accountId: ID de la cuenta
  - fromDate: YYYY-MM-DD
  - toDate: YYYY-MM-DD
  - limit: número (por defecto 50)
  - page: número (por defecto 1)
  - sortBy: "date" | "engagement"
  - order: "asc" | "desc"
```

Retorna posts individuales con sus métricas.

**Respuesta:**
```json
{
  "posts": [
    {
      "id": "post_456def",
      "platform": "instagram",
      "content": "URL de la imagen/video",
      "caption": "Texto del post",
      "posted_at": "2024-05-30T14:30:00Z",
      "likes": 150,
      "comments": 23,
      "shares": 5,
      "saves": 12,
      "reach": 2000,
      "impressions": 2500,
      "engagement_rate": 4.5,
      "comment_sentiment": "positive"
    }
  ],
  "pagination": {
    "total": 245,
    "page": 1,
    "limit": 50,
    "pages": 5
  }
}
```

### Métricas Diarias Agregadas

```http
GET /analytics/daily-metrics
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - platform: "instagram"
  - accountId: ID de la cuenta
  - fromDate: YYYY-MM-DD
  - toDate: YYYY-MM-DD
```

Requiere **Analytics add-on** activado en Zernio.

**Respuesta:**
```json
{
  "metrics": [
    {
      "date": "2024-05-30",
      "reach": 5200,
      "impressions": 6100,
      "engagement": 340,
      "engagement_rate": 5.58,
      "saves": 45,
      "shares": 12,
      "clicks": 89,
      "video_views": 2100
    }
  ]
}
```

### Mejores Horarios para Publicar

```http
GET /analytics/best-time
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - platform: "instagram"
  - accountId: ID de la cuenta
```

Retorna slots horarios con engagement promedio.

**Respuesta:**
```json
{
  "best_time": [
    {
      "day_of_week": 0,  // 0 = Lunes, 6 = Domingo
      "hour": 14,         // 0-23 UTC
      "avg_engagement": 145.5,
      "posts_count": 12
    }
  ]
}
```

### Frecuencia de Publicación

```http
GET /analytics/posting-frequency
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - platform: "instagram"
  - accountId: ID de la cuenta
```

Correlación entre frecuencia y engagement.

**Respuesta:**
```json
{
  "data": [
    {
      "posts_per_week": 3.5,
      "avg_engagement_rate": 5.2,
      "weeks_count": 8
    }
  ]
}
```

### Decaimiento de Contenido

```http
GET /analytics/content-decay
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - platform: "instagram"
  - accountId: ID de la cuenta
```

Muestra cómo decae el engagement con el tiempo.

**Respuesta:**
```json
{
  "data": [
    {
      "bucket_label": "Primera hora",
      "avg_pct_of_final": 85.3
    },
    {
      "bucket_label": "Primeras 24h",
      "avg_pct_of_final": 65.2
    }
  ]
}
```

### Health Check de Cuenta

```http
GET /analytics/instagram/account-insights
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - accountId: ID de la cuenta
  - metricType: "timeseries" | "totalvalue"
  - since: YYYY-MM-DD
  - until: YYYY-MM-DD
```

Estado y salud de la cuenta de Instagram.

**Respuesta:**
```json
{
  "id": "acc_123abc",
  "platform": "instagram",
  "token_valid": true,
  "is_active": true,
  "is_verified": false,
  "is_restricted": false,
  "scopes_ok": true,
  "checked_at": "2024-05-31T10:30:00Z",
  "followers": 5000,
  "reach": 8500,
  "impressions": 10200,
  "engagement_rate": 5.4
}
```

### Demografía de Audiencia

```http
GET /analytics/instagram/demographics
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - accountId: ID de la cuenta
  - metric: "followerDemographics" | "engagedAudienceDemographics"
  - breakdown: "age" | "gender" | "country" | "city"
  - timeframe: "thisWeek" | "this_month"
```

Segmentación de audiencia por diferentes criterios.

**Respuesta (Age):**
```json
{
  "data": [
    {
      "label": "18-24",
      "count": 450,
      "percentage": 18.5
    },
    {
      "label": "25-34",
      "count": 920,
      "percentage": 37.8
    }
  ]
}
```

### Estadísticas de Seguidores

```http
GET /accounts/follower-stats
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - accountId: ID de la cuenta
  - platform: "instagram"
```

Historial de crecimiento de seguidores.

**Respuesta:**
```json
{
  "history": [
    {
      "date": "2024-05-30",
      "followers": 5000,
      "gained": 12,
      "lost": 3,
      "net_change": 9
    }
  ]
}
```

### Comentarios

```http
GET /inbox/comments
Authorization: Bearer {ZERNIO_API_KEY}
Parameters:
  - accountId: ID de la cuenta
  - platform: "instagram"
```

Últimos comentarios recibidos.

**Respuesta:**
```json
{
  "comments": [
    {
      "id": "comment_789ghi",
      "post_id": "post_456def",
      "author": "@usuario",
      "text": "¡Excelente contenido!",
      "timestamp": "2024-05-30T15:30:00Z",
      "likes": 5,
      "sentiment": "positive"
    }
  ]
}
```

## Manejo de Errores

### Códigos de Estado HTTP

| Código | Significado | Solución |
|--------|-------------|----------|
| 200 | OK | - |
| 400 | Bad Request | Validar parámetros |
| 401 | Unauthorized | Verificar API key |
| 402/403 | Add-on Required | Activar add-on en Zernio |
| 429 | Rate Limited | Esperar y reintentar |
| 500 | Server Error | Contactar Zernio support |

### Ejemplos de Error

**Error de autenticación:**
```json
{
  "error": "invalid_token",
  "message": "Authentication failed"
}
```

**Add-on requerido:**
```json
{
  "error": "addon_required",
  "message": "Analytics add-on is required for this endpoint",
  "addon": "analytics"
}
```

## Rate Limiting

- **Límite:** 60 requests/minuto
- **Header:** `X-RateLimit-Remaining`
- **Estrategia:** Backoff exponencial (2^attempt segundos)

## Add-ons Requeridos

| Endpoint | Add-on Requerido |
|----------|------------------|
| `/analytics` | Basic (incluido) |
| `/analytics/daily-metrics` | Analytics |
| `/analytics/best-time` | Analytics |
| `/analytics/posting-frequency` | Analytics |
| `/analytics/content-decay` | Analytics |
| `/analytics/instagram/account-insights` | Analytics |
| `/analytics/instagram/demographics` | Analytics |

## Normalizaciones en Este Dashboard

El loader (`src/data/loader.py`) normaliza respuestas inconsistentes de Zernio:

### Extracción Flexible
```python
# Busca el listado en varios campos posibles
_extract_list(response, ["data", "items", "rows", "results"])

# Personaliza formatos
_normalize_daily_metrics(items)  # Unifica campos de métricas
_normalize_demographics(items)   # Estandariza edad/género/país
```

### Fallback Defensivo
Si un endpoint falla:
1. Reintenta con backoff exponencial
2. Si persiste, retorna estructura vacía
3. Dashboard sigue funcionando parcialmente

## Testing de Endpoints

```bash
# Validar todos los endpoints
python src/api/client.py
```

Output:
```
✅ List Accounts: SUCCESS
✅ Post Analytics: SUCCESS
⚠️  Daily Metrics: ADD-ON REQUERIDO
❌ Demographics: ERROR - Invalid params
```

## Documentación Oficial

- [Docs Zernio](https://docs.zernio.com/platforms/instagram)
- [API Reference](https://docs.zernio.com/api/rest)
- [Add-ons Guide](https://docs.zernio.com/add-ons)

## Límites y Restricciones

- **Historial:** 90 días máximo
- **Seguidores:** Requiere 100+ seguidores para demografía
- **Delay:** Hasta 48 horas de atraso en algunos datos
- **Rate limit:** 60 req/min
- **Timeout:** 30 segundos por request

## Integración en el Dashboard

El flujo es:
1. `app.py` llama `load_account_data()`
2. `loader.py` usa `ZernioClient` para múltiples endpoints
3. Normaliza todas las respuestas
4. Retorna dict unificado a las tabs
5. Tabs renderizan datos con Streamlit

## Variables de Redacción

Para usar datos en la UI:
```python
data = load_account_data()

# Account info
username = data["account_snapshot"]["username"]
followers = data["account_snapshot"]["followers_count"]

# Trends
daily = data["daily_metrics"]  # List de dicts con date/reach/engagement_rate

# Demographics
age_data = data["demographics"]["instagram"]["age"]  # List de {label, count, pct}

# Posts
posts = data["posts"]  # List of posts with likes/comments/etc
```

