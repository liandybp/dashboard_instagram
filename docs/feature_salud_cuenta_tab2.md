# Feature: Salud de Cuenta — Pestaña 2 del Dashboard
## Addendum al Plan Técnico de Implementación

---

## Qué cambia respecto al plan original

El plan original define **Tab 2** como "Tendencia" (gráfico de líneas de métricas diarias + crecimiento de seguidores). Esta especificación **reemplaza Tab 2 por una pestaña de Salud de Cuenta**, que combina:

- Estado operativo de la conexión técnica (token, permisos, restricciones)
- Métricas de crecimiento y dinámica de seguidores (ganados/perdidos por día)
- Verificación de cuenta y alertas de restricciones

> **Nota:** Si prefieres mantener la pestaña Tendencia original, renúmera las pestañas a 8 en total y coloca esta como Tab 2, empujando las demás una posición. Díselo a Claude Code al inicio de la implementación.

---

## 1. Endpoint que alimenta esta pestaña

### Endpoint principal

```
GET /v1/accounts/{accountId}/health
Header: Authorization: Bearer {ZERNIO_API_KEY}
```

Ya existe en `zernio_client.py` como `get_account_health(id)`. **No requiere implementación nueva en el cliente**, solo aprovechar la respuesta completa que ya devuelve.

### Endpoint de historial de seguidores

```
GET /analytics/instagram/follower-history
```

Ya existe en `zernio_client.py` como `get_follower_history(account_id)`. Devuelve la serie temporal con `followers_gained` y `followers_lost` por día.

### Endpoint masivo (opcional, para futura expansión multi-cuenta)

```
CLI: zernio accounts:health   ← no usar desde el dashboard, es para terminal
```

No implementar desde la UI. Documentarlo en `CLAUDE.md` como referencia pero no exponer.

---

## 2. Nuevas tablas SQLite necesarias

### Tabla `account_health` — ampliar DDL existente

El plan original ya define `account_health` como tabla snapshot. **Ampliar su DDL** para almacenar los nuevos campos:

```sql
CREATE TABLE IF NOT EXISTS account_health (
    id          TEXT,
    platform    TEXT,
    -- Campos originales
    status      TEXT,
    checked_at  TEXT,
    -- Campos nuevos a añadir
    token_valid         INTEGER,   -- booleano (0/1)
    is_active           INTEGER,   -- booleano (0/1)
    is_verified         INTEGER,   -- booleano (0/1)
    is_restricted       INTEGER,   -- booleano (0/1)
    scopes_ok           INTEGER,   -- booleano (0/1): todos los permisos necesarios presentes
    missing_scopes      TEXT,      -- JSON array de scopes faltantes, si los hay
    issues              TEXT,      -- JSON array de strings con problemas detectados
    recommendations     TEXT,      -- JSON array de strings con recomendaciones de Zernio
    PRIMARY KEY (id, platform)
);
```

**Migración idempotente obligatoria** — usar `PRAGMA table_info(account_health)` antes de cada `ALTER TABLE ADD COLUMN`. Ver Gotcha #3 del plan original.

### Tabla `follower_history` — sin cambios de schema

Ya acumula por `(date, platform)`. Solo verificar que los campos `followers_gained` y `followers_lost` estén en el DDL. Si no están, añadirlos con migración idempotente:

```sql
-- Verificar con PRAGMA antes de ejecutar:
ALTER TABLE follower_history ADD COLUMN followers_gained INTEGER DEFAULT 0;
ALTER TABLE follower_history ADD COLUMN followers_lost    INTEGER DEFAULT 0;
```

---

## 3. Cambios en `cache.py`

### Writer de `account_health` — ampliar

```python
def write_account_health(conn, platform: str, account_id: str, health_data: dict):
    """
    Sobreescribe el estado de salud de la cuenta (snapshot — no acumula).
    health_data es el JSON tal como devuelve Zernio.
    """
    conn.execute("""
        INSERT OR REPLACE INTO account_health
        (id, platform, status, checked_at,
         token_valid, is_active, is_verified, is_restricted, scopes_ok,
         missing_scopes, issues, recommendations)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        account_id,
        platform,
        health_data.get("status", "unknown"),
        datetime.utcnow().isoformat(),
        int(health_data.get("tokenValid", False)),
        int(health_data.get("isActive", False)),
        int(health_data.get("isVerified", False)),
        int(health_data.get("isRestricted", False)),
        int(health_data.get("scopesOk", True)),
        json.dumps(health_data.get("missingScopes", [])),
        json.dumps(health_data.get("issues", [])),
        json.dumps(health_data.get("recommendations", [])),
    ))
    conn.commit()
```

### Reader de `account_health`

```python
def read_account_health(conn, platform: str) -> dict | None:
    """Devuelve el último estado de salud para una plataforma, o None si no hay datos."""
    row = conn.execute(
        "SELECT * FROM account_health WHERE platform = ? ORDER BY checked_at DESC LIMIT 1",
        (platform,)
    ).fetchone()
    if not row:
        return None
    return dict(row)
```

### Reader de `follower_history` con ganados/perdidos

```python
def read_follower_history(conn, platform: str, days: int = 90) -> list[dict]:
    """
    Devuelve serie temporal de seguidores con dinámica diaria.
    Ordenado cronológicamente, últimos N días.
    """
    cutoff = (datetime.utcnow() - timedelta(days=days)).date().isoformat()
    rows = conn.execute("""
        SELECT date, followers, followers_gained, followers_lost
        FROM follower_history
        WHERE platform = ? AND date >= ?
        ORDER BY date ASC
    """, (platform, cutoff)).fetchall()
    return [dict(r) for r in rows]
```

---

## 4. Cambios en `refresh.py`

### Dentro de `refresh_instagram()`, actualizar la llamada a `get_account_health`

```python
# Ya existe en el plan original. Ampliar para persistir todos los campos nuevos:
health_data = client.get_account_health(account_id)
write_account_health(conn, "instagram", account_id, health_data)

# Si la cuenta está restringida, loggear advertencia visible al usuario:
if health_data.get("isRestricted"):
    print("⚠️  ADVERTENCIA: Tu cuenta de Instagram aparece como restringida en Zernio.")
    print("    Esto puede impedir publicar contenido. Revisa tu cuenta en Instagram.")

# Si el token no es válido:
if not health_data.get("tokenValid", True):
    print("❌  El token de Instagram expiró. Reconecta tu cuenta en zernio.com/dashboard")
```

---

## 5. Cambios en `app.py` — Tab 2

### Reemplazar el contenido de Tab 2

```python
# En app.py, dentro de la definición de tabs:
tab2_label = "🩺 Salud de Cuenta"

# Dentro de render_tab_salud():
def render_tab_salud():
    st.subheader("Estado de la conexión")

    health = read_account_health(conn, platform_selected)

    if not health:
        st.info("Sin datos de salud. Haz clic en 'Refrescar datos' para verificar.")
        return

    # --- Bloque 1: Indicadores booleanos en columnas ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        icon = "🟢" if health["token_valid"] else "🔴"
        st.metric("Token OAuth", f"{icon} {'Válido' if health['token_valid'] else 'Expirado'}")

    with col2:
        icon = "🟢" if health["is_active"] else "🔴"
        st.metric("Cuenta activa", f"{icon} {'Sí' if health['is_active'] else 'No'}")

    with col3:
        icon = "✅" if health["is_verified"] else "—"
        st.metric("Verificada", f"{icon} {'Sí' if health['is_verified'] else 'No'}")

    with col4:
        icon = "⚠️" if health["is_restricted"] else "🟢"
        label = "Restringida" if health["is_restricted"] else "Sin restricciones"
        st.metric("Restricciones", f"{icon} {label}")

    # --- Bloque 2: Permisos (scopes) ---
    st.divider()
    st.subheader("Permisos de la integración")

    if health["scopes_ok"]:
        st.success("✅ Todos los permisos necesarios están activos.")
    else:
        missing = json.loads(health["missing_scopes"] or "[]")
        st.error(f"❌ Faltan {len(missing)} permiso(s): {', '.join(missing)}")
        st.caption("Reconecta tu cuenta en zernio.com para restaurar los permisos.")

    # --- Bloque 3: Problemas y recomendaciones ---
    issues = json.loads(health["issues"] or "[]")
    recommendations = json.loads(health["recommendations"] or "[]")

    if issues:
        st.divider()
        st.subheader("⚠️ Problemas detectados")
        for issue in issues:
            st.warning(issue)

    if recommendations:
        st.subheader("💡 Recomendaciones")
        for rec in recommendations:
            st.info(rec)

    if not issues and not recommendations:
        st.divider()
        st.success("Todo en orden. No hay problemas ni recomendaciones pendientes.")

    # --- Bloque 4: Dinámica de seguidores ---
    st.divider()
    st.subheader("Dinámica de seguidores (últimos 90 días)")

    follower_data = read_follower_history(conn, platform_selected, days=90)

    if not follower_data:
        st.info("Sin historial de seguidores. Refresca para cargar datos.")
        return

    df = pd.DataFrame(follower_data)

    # Gráfico de línea: total de seguidores
    fig_total = px.line(
        df, x="date", y="followers",
        title="Total de seguidores por día",
        labels={"date": "Fecha", "followers": "Seguidores"},
        color_discrete_sequence=["#E1306C"]  # Rosa Instagram
    )
    fig_total.update_layout(hovermode="x unified")
    st.plotly_chart(fig_total, use_container_width=True)

    # Gráfico de barras apiladas: ganados vs perdidos
    if "followers_gained" in df.columns and df["followers_gained"].sum() > 0:
        fig_delta = go.Figure()
        fig_delta.add_trace(go.Bar(
            x=df["date"], y=df["followers_gained"],
            name="Ganados", marker_color="#4CAF50"
        ))
        fig_delta.add_trace(go.Bar(
            x=df["date"], y=[-v for v in df["followers_lost"]],
            name="Perdidos", marker_color="#F44336"
        ))
        fig_delta.update_layout(
            title="Seguidores ganados y perdidos por día",
            barmode="relative",
            hovermode="x unified",
            yaxis_title="Seguidores",
            xaxis_title="Fecha"
        )
        st.plotly_chart(fig_delta, use_container_width=True)
        st.caption(
            "ℹ️ Meta eliminó el historial de ganados/perdidos de su API nativa. "
            "Zernio reconstruye esta métrica mediante capturas diarias."
        )
    else:
        st.caption("Los datos de seguidores ganados/perdidos estarán disponibles "
                   "tras varios días de capturas consecutivas.")

    # Última actualización
    st.caption(f"Última verificación: {health['checked_at'][:16].replace('T', ' ')} UTC")
```

### Imports adicionales necesarios en `app.py`

```python
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
```

`pandas` no estaba en el plan original. Añadir a `requirements.txt`:

```
pandas==2.2.3
```

---

## 6. Cambios en `requirements.txt`

```
streamlit==1.39.0
plotly==5.24.0
requests==2.32.3
anthropic==0.97.0
httpx==0.28.1
python-dotenv==1.0.1
pandas==2.2.3          # NUEVO — para DataFrames en Tab 2
```

---

## 7. Prompt para Claude Code

Pega esto en Claude Code **después de completar la Fase 7 original** (o en su lugar si vas a construir Tab 2 desde cero con esta especificación):

```
Vamos a implementar la pestaña 2 del dashboard: "Salud de Cuenta".

CONTEXTO: Esta pestaña reemplaza la pestaña "Tendencia" original (o se inserta como Tab 2
nueva si prefieres mantener la de Tendencia — pregúntame si no estás seguro).

PASO 1 — Ampliar DDL en cache.py:
Añade las columnas nuevas a la tabla account_health con migración idempotente
(PRAGMA table_info antes de cada ALTER TABLE ADD COLUMN):
  - token_valid INTEGER
  - is_active INTEGER
  - is_verified INTEGER
  - is_restricted INTEGER
  - scopes_ok INTEGER
  - missing_scopes TEXT (JSON array)
  - issues TEXT (JSON array)
  - recommendations TEXT (JSON array)

También verifica que follower_history tiene las columnas followers_gained y followers_lost.
Si no, añádelas con migración idempotente.

PASO 2 — Ampliar write_account_health() en cache.py:
El writer debe persistir todos los campos nuevos del JSON de Zernio, no solo "status".

PASO 3 — Añadir read_follower_history() en cache.py:
Devuelve los últimos 90 días con date, followers, followers_gained, followers_lost.

PASO 4 — Ampliar refresh.py:
En refresh_instagram(), tras llamar get_account_health(), imprimir advertencia si
isRestricted=True o tokenValid=False.

PASO 5 — Implementar render_tab_salud() en app.py:
4 métricas booleanas en columnas (token, activa, verificada, restricciones)
+ bloque de permisos (scopes_ok / missing_scopes)
+ bloque de issues y recommendations
+ gráfico de línea total de seguidores (Plotly, últimos 90 días)
+ gráfico de barras ganados/perdidos (verde/rojo, barmode=relative)
+ caption sobre por qué Zernio reconstruye esta métrica

PASO 6 — Añadir pandas==2.2.3 a requirements.txt e instalar.

PASO 7 — Haz un refresh.py real para poblar los datos nuevos y lanza
streamlit run app.py. Verifica que Tab 2 muestra los indicadores con datos reales.

Si get_account_health devuelve campos con nombres distintos a los que uso arriba
(camelCase vs snake_case), ajusta el mapeo en write_account_health() según lo que
devuelva realmente la API de Zernio.
```

---

## 8. Checklist de aceptación para esta feature

- [ ] Tab 2 se llama "🩺 Salud de Cuenta" (o similar)
- [ ] Los 4 indicadores booleanos (token, activa, verificada, restricciones) se muestran con íconos de color
- [ ] Si el token está expirado, el indicador aparece en rojo
- [ ] Si la cuenta está restringida, aparece advertencia visible (no solo un ícono)
- [ ] El bloque de permisos muestra "todos activos" o lista los faltantes
- [ ] Las issues y recomendaciones de Zernio se renderizan si las hay
- [ ] El gráfico de total de seguidores muestra la curva correcta (verificar contra Instagram real)
- [ ] El gráfico de ganados/perdidos usa barras verdes/rojas con `barmode=relative`
- [ ] El caption sobre la reconstrucción de Zernio está visible debajo del segundo gráfico
- [ ] Si no hay datos aún, se muestra mensaje de "Refresca para cargar" (sin error)

---

## 9. Riesgos y notas

| Riesgo | Detalle | Mitigación |
|--------|---------|------------|
| Nombres de campos en camelCase | Zernio puede devolver `tokenValid` o `token_valid` | Usar `.get()` con ambas variantes como fallback |
| `followers_gained`/`followers_lost` ausentes en primeros días | Zernio reconstruye mediante capturas; los primeros días no tienen delta | Comprobar si la columna tiene valores antes de renderizar el segundo gráfico |
| `pandas` no estaba en el plan original | Se añade como dependencia nueva | Versión pinneada `2.2.3`; compatible con Python 3.9+ y Streamlit 1.39 |
| `account_health` ya existe en SQLite con schema reducido | Si la base de datos ya fue creada sin las columnas nuevas, la migración idempotente es crítica | Gotcha #3 del plan original — PRAGMA antes de ALTER |
| Zernio requiere add-on para datos completos de salud | Si `isRestricted` o `missingScopes` no devuelven datos, el add-on puede estar inactivo | Manejar gracefully con `.get(..., default)` en todos los campos |
