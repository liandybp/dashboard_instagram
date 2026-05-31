# Plan de Enriquecimiento de Pestañas del Dashboard
## Qué añadir en cada pestaña usando la API de Zernio

**Referencia visual:** Dashboard actual → Métricas · Health · Audiencia · Posts · Mejor Horario · Frecuencia · Ideas

Este documento define **qué añadir de valor real** en cada pestaña basándose estrictamente en los endpoints de Zernio documentados. Todo lo marcado como ✅ usa endpoints ya implementados en `zernio_client.py`. Lo marcado ⚠️ requiere verificar si el endpoint devuelve ese campo concreto.

---

## Criterio de selección

Solo se incluye información que:
1. Viene de un endpoint Zernio verificado en el plan técnico original
2. Ayuda a tomar una **decisión concreta** como creadora (no es decoración)
3. No duplica algo que ya existe en otra pestaña

Se descarta todo lo relacionado con publicación, mensajería activa, ads y automatización — el dashboard es 100% solo lectura.

---

## Tab 1 — 📊 Métricas (era "Resumen")

### Qué tiene ahora
KPIs de los últimos 30 días: alcance, vistas, engagement, interacciones, likes, comentarios, guardados, shares.

### Qué añadir y por qué

**1. Variación respecto al período anterior** (calculado localmente con `daily_metrics`)
- Mostrar `+12%` o `−5%` debajo de cada KPI comparando los últimos 30 días vs los 30 anteriores
- No requiere endpoint nuevo — los datos ya están en `daily_metrics` (rolling 180 días)
- Por qué vale: de un vistazo sabes si vas creciendo o decreciendo, no solo el número absoluto

**2. Tasa de engagement calculada**
- Fórmula: `(likes + comments + saves + shares) / reach * 100`
- Se calcula localmente desde `account_insights_30d`
- Benchmark orientativo en caption: "IG promedio industria: 1-3%"
- Por qué vale: el reach solo no dice nada sin contexto de engagement

**3. Ratio guardados/likes**
- Guardados ÷ likes = indicador de contenido "valioso vs entretenido"
- Se calcula desde `account_insights_30d`
- Por qué vale: guardados altos relativo a likes = contenido que la gente quiere conservar (señal de autoridad)

**4. Mejor post del período** (desde `posts` en SQLite)
- Tarjeta pequeña con thumbnail + caption truncada + su métrica top
- Ordenado por `saves` primero (mejor señal de valor), luego por `reach`
- Link a permalink
- Por qué vale: ancla el resumen numérico a un ejemplo concreto

### Endpoint fuente
- `GET /analytics/instagram/account-insights` → tabla `account_insights_30d` (ya implementado)
- `daily_metrics` en SQLite (ya implementado, cálculo local)
- `posts` en SQLite (ya implementado)

### Cambios técnicos necesarios
- Solo lógica de cálculo en `app.py` — sin endpoints nuevos
- Añadir columna `delta_pct` calculada en el reader de métricas

---

## Tab 2 — 🩺 Health (ya especificada en doc anterior)

Ver `feature_salud_cuenta_tab2.md` — ya completamente definida.

**Resumen de lo que incluye:** estado del token, permisos activos, restricciones, issues/recomendaciones de Zernio, curva de seguidores totales, gráfico ganados/perdidos por día.

---

## Tab 3 — 👥 Audiencia

### Qué tiene ahora
Sub-pestañas IG/YT con barras de age/gender/country/city.

### Qué añadir y por qué

**1. Tabla de países con porcentaje acumulado**
- En lugar de solo barra, añadir la tabla debajo con: país, % de audiencia, bandera emoji
- Mostrar "Top 5 países = X% de tu audiencia total"
- Por qué vale: muchas creadoras no saben qué tan concentrada o dispersa está su audiencia geográficamente

**2. Indicador de alineación nicho/audiencia**
- Cálculo local: si el país #1 tiene >60% → audiencia concentrada (bueno para nichos locales)
- Si el país #1 tiene <30% → audiencia dispersa (considera si tu contenido es muy generalista o internacional)
- Renderizar como `st.info()` con interpretación en 1 línea
- Por qué vale: convierte datos brutos en una recomendación accionable

**3. Split de género con contexto**
- Ya existe como barra, mejorar añadiendo: "Tu audiencia es X% femenina / Y% masculina"
- Si el split es muy desbalanceado (>80/20), añadir nota: "¿Tu contenido habla explícitamente a este segmento?"
- Por qué vale: muchas creadoras descubren aquí que tienen más audiencia masculina de la que creen

**4. Rango de edad dominante destacado**
- Resaltar el bucket de edad con mayor %, no solo mostrarlo en barra
- Añadir: "Tu audiencia principal tiene entre X-Y años"
- Por qué vale: el copy y los hooks que funcionan son distintos para 18-24 que para 35-44

**5. (Solo YT) Métricas de canal separadas** ✅
- `get_youtube_demographics()` devuelve age/gender/country (sin city)
- Mostrar en sub-pestaña YT igual que IG pero sin la dimensión ciudad
- Endpoint: `GET /analytics/youtube/demographics`

### Endpoint fuente
- `GET /analytics/instagram/demographics` → tablas `demographics_age/gender/country/city` (ya implementado)
- `GET /analytics/youtube/demographics` → mismas tablas con `platform=youtube`
- Todo cálculo es local desde SQLite

### Cambios técnicos necesarios
- Reader de `demographics_country` que devuelve porcentajes
- Lógica de interpretación (strings condicionales) en `app.py`
- Sin endpoints nuevos

---

## Tab 4 — 📸 Posts

### Qué tiene ahora
Grid de 3 columnas con thumbnails, ordenable, click → expander con comentarios reales.

### Qué añadir y por qué

**1. Ordenación múltiple con selector**
- Añadir `st.selectbox("Ordenar por:", ["Guardados", "Alcance", "Likes", "Comentarios", "Ratio engagement"])` 
- Por defecto: guardados (mejor señal de valor)
- Por qué vale: ver los posts por guardados vs por likes puede dar listas completamente distintas y revelar qué contenido realmente resuena

**2. Badge de "tipo de formato" en cada card**
- Inferido del campo `format` si Zernio lo devuelve, o del permalink (contiene `/reel/` vs `/p/`)
- Badge visual: 🎬 Reel · 📑 Carrusel · 🖼 Imagen
- Por qué vale: permite identificar qué formato funciona mejor sin configuración extra

**3. Métricas de decaimiento por post** ⚠️
- `get_content_decay()` devuelve datos de rendimiento relativo al tiempo de vida del post
- Mostrar en la card un indicador simple: "🔥 Viral (primeras 48h)" / "📈 Largo alcance" / "📉 Decayó rápido"
- Por qué vale: identifica qué posts tienen "vida larga" vs cuáles dependen del impulso inicial

**4. Contexto de perfil del comentarista** ✅
- `list_inbox_comments()` y `get_post_comments()` devuelven metadata del remitente: si es seguidor, su follower count, si está verificado
- En el expander de comentarios, añadir badge: "👤 Seguidor" o "⭐ Verificado" junto a comentarios clave
- Por qué vale: un comentario de alguien con 50K seguidores que te pregunta algo es más valioso como insight que el mismo comentario de una cuenta nueva

**5. Contador de comentarios sustantivos vs totales**
- Mostrar: "12 comentarios · 4 sustantivos (los que generan ideas)"
- Calculado localmente con `idea_filters.is_substantive_comment()`
- Por qué vale: cierra el loop visual con el sistema de ideas — ves directamente qué posts tienen "materia prima" para ideas

### Endpoint fuente
- `GET /inbox/comments` → tabla `posts` + `comments` (ya implementado)
- `GET /inbox/comments/{postId}?accountId=...` → drilldown de comentarios (ya implementado)
- `GET /analytics/content-decay` → tabla `content_decay` (ya implementado)
- Metadata de perfil del comentarista: verificar si viene en el payload de `list_inbox_comments`

### Cambios técnicos necesarios
- Modificar reader de `comments` para incluir metadata de perfil si existe
- Selector de ordenación en la UI (solo lógica de `ORDER BY` en query SQLite)
- Inferencia de formato desde permalink (regex simple: `/reel/` → Reel)

---

## Tab 5 — ⏰ Mejor Horario

### Qué tiene ahora
Heatmap (día semana × hora) con datos de `best_time`, con conversión UTC → TZ local.

### Qué añadir y por qué

**1. Top 3 slots concretos en texto**
- Debajo del heatmap, extraer los 3 mejores slots y mostrarlos como: "🥇 Martes 19:00 · 🥈 Jueves 20:00 · 🥉 Miércoles 19:00"
- Se calcula ordenando la tabla `best_time` por score DESC
- Por qué vale: el heatmap es visual pero la creadora quiere saber exactamente cuándo programar — no quiere leer colores

**2. Frecuencia de publicación actual vs óptima**
- `get_posting_frequency()` devuelve la relación entre posts/semana y engagement
- Añadir un indicador: "Actualmente publicas X veces/semana. El mejor engagement lo tienes con Y veces/semana"
- Por qué vale: responde la pregunta "¿estoy publicando demasiado o muy poco?"

**3. Comparativa IG vs YT en el mismo heatmap** (si tiene YouTube)
- Mostrar dos heatmaps lado a lado o con toggle
- Endpoint: `GET /analytics/best-time?platform=youtube`
- Por qué vale: el mejor horario para IG y para YT suele ser distinto — las audiencias tienen hábitos distintos

**4. Nota sobre limitación de la métrica**
- Caption fijo debajo del heatmap: "Este análisis se basa en el historial de tus posts. Con más tiempo publicando, los datos serán más precisos."
- Por qué vale: transparencia — con pocos posts el heatmap puede ser poco representativo

### Endpoint fuente
- `GET /analytics/best-time` → tabla `best_time` (ya implementado)
- `GET /analytics/posting-frequency` → tabla `posting_frequency` (ya implementado)
- Cálculo de top 3 slots: lógica local en `app.py`

### Cambios técnicos necesarios
- Reader de `best_time` que devuelva ordenado por score
- Reader de `posting_frequency` que extraiga el bucket de mejor engagement
- Sin endpoints nuevos

---

## Tab 6 — 📅 Frecuencia

### Qué tiene ahora
Scatter posts/semana vs engagement + content decay.

### Qué añadir y por qué

**1. Curva de decaimiento con interpretación**
- `get_content_decay()` devuelve cómo rinde el contenido según su antigüedad
- El scatter actual solo muestra puntos. Añadir una línea de tendencia (Plotly `trendline="ols"` si pandas está instalado, o manual)
- Añadir interpretación en texto: "Tu contenido mantiene el X% del engagement inicial a los 7 días"
- Por qué vale: saber si tu contenido "aguanta" o muere en 24h cambia la estrategia de programación

**2. Ventana de rendimiento de tus posts**
- Calculado desde `posts` + `daily_metrics` en SQLite
- Para cada post, comparar su rendimiento en las primeras 24h vs su rendimiento acumulado total
- Mostrar: "El X% de tus posts generan el 80% de su alcance en las primeras 48h"
- Por qué vale: si el número es muy alto (>90%), publicar en el horario óptimo es crítico; si es bajo, tienes más margen

**3. Cadencia recomendada**
- Desde `posting_frequency`, mostrar el bucket donde tu engagement es máximo
- Visualizar como un segmento destacado en el scatter: "Zona óptima: 3-4 posts/semana"
- Por qué vale: convierte el scatter en una recomendación accionable, no solo un gráfico exploratorio

**4. Historial de tu cadencia real** (calculado localmente)
- Contar posts por semana desde la tabla `posts` y mostrar como barra apilada por semana
- Colorear las semanas donde publicaste en la "zona óptima" de verde, fuera de zona de amarillo/rojo
- Por qué vale: muchas creadoras creen que publican más seguido de lo que realmente hacen

### Endpoint fuente
- `GET /analytics/posting-frequency` → tabla `posting_frequency` (ya implementado)
- `GET /analytics/content-decay` → tabla `content_decay` (ya implementado)
- `posts` en SQLite para cadencia real (ya implementado)

### Cambios técnicos necesarios
- Lógica de cálculo de "ventana de rendimiento" desde SQLite (query + cálculo local)
- `trendline` en Plotly scatter (sin nueva dependencia si se calcula manualmente)
- Cálculo de semanas con `datetime` stdlib

---

## Tab 7 — 💡 Ideas

### Qué tiene ahora
Generación de 25 ideas (10 comments / 5 DMs / 10 top_content) con los 3 bloques, descarte con aprendizaje.

### Qué añadir y por qué

**1. Contexto de audiencia visible antes de generar**
- Mostrar un resumen colapsable antes del botón de generar:
  ```
  📊 Contexto que usará Claude:
  • 847 comentarios en los últimos 90 días (312 sustantivos)
  • 43 DMs en los últimos 30 días (18 sustantivos)
  • Top 20 posts incluidos
  • Demografía dominante: 25-34 años, 68% femenina, España
  ```
- Calculado localmente desde SQLite
- Por qué vale: la creadora entiende qué tan rica es su señal — si tiene 5 comentarios sustantivos, sabe que las ideas serán genéricas

**2. Indicador de costo estimado antes de generar**
- Calcular tokens aproximados del contexto cacheado y mostrar: "~$0.12 estimado"
- Fórmula aproximada: `(tokens_contexto * 0.000003) + (16000 * 0.000015)`
- Por qué vale: transparencia de costo antes de hacer click

**3. Historial de generaciones anteriores**
- Añadir sección colapsable "Generaciones anteriores" con las últimas 3 sesiones de ideas (por `batch_id`)
- Mostrar: fecha + cuántas ideas generó + cuántas descartó
- Por qué vale: permite revisar ideas de ayer sin volver a generar

**4. Panel de descartes más informativo**
- En la sección "Últimos descartes", mostrar el patrón aprendido:
  - "Has descartado X ideas del bucket 'comments'" → "Claude evitará ese tipo de ángulos"
  - "Has descartado Y ideas por 'Muy básica'" → resaltar en negrita
- Por qué vale: hace visible el aprendizaje que el sistema ya tiene — muchas usuarias no saben que el descarte "enseña" algo

**5. Link directo al post fuente desde la card**
- Si la idea tiene `basis_post_ids`, el permalink ya está en `posts.permalink`
- Renderizar como `[Ver post original →](permalink)` en la card
- Por qué vale: permite ir directo al post que generó la idea sin buscar manualmente

### Endpoint fuente
- Todo desde SQLite — sin endpoints nuevos
- `posts.permalink` (ya en cache)
- `ideas` y `idea_discards` (ya implementadas)

### Cambios técnicos necesarios
- Query de conteo de comentarios sustantivos en `app.py` (aplicar `idea_filters` al conteo)
- Cálculo local de estimación de costo (constantes hardcodeadas)
- Reader de `ideas` agrupado por `batch_id` con `COUNT()`

---

## Resumen de cambios por archivo

| Archivo | Cambios | Complejidad |
|---------|---------|-------------|
| `cache.py` | Readers nuevos para: delta de métricas, top posts por métrica, country con %, best_time ordenado, posting_frequency con zona óptima, ideas agrupadas por batch | Media |
| `app.py` | Lógica de cálculo e interpretación para cada tab, selectores de ordenación, estimador de costo, cards mejoradas | Media-Alta |
| `idea_filters.py` | Función `count_substantive(comments_list)` para mostrar conteo en Tab 7 | Baja |
| `zernio_client.py` | Sin cambios — todos los endpoints ya están implementados | Ninguna |
| `refresh.py` | Sin cambios — ya ingesta todos los datos necesarios | Ninguna |
| `requirements.txt` | `pandas==2.2.3` (si no está ya) | Ninguna |

---

## Endpoints Zernio utilizados en este plan

| Endpoint | Tabla SQLite | Tabs que lo usan |
|----------|-------------|------------------|
| `GET /analytics/instagram/account-insights` | `account_insights_30d` | Tab 1 |
| `GET /analytics/daily-metrics` | `daily_metrics` | Tab 1, Tab 6 |
| `GET /analytics/instagram/demographics` | `demographics_*` | Tab 3 |
| `GET /analytics/youtube/demographics` | `demographics_*` | Tab 3 |
| `GET /inbox/comments` | `posts`, `comments` | Tab 4 |
| `GET /inbox/comments/{postId}` | `comments` | Tab 4 |
| `GET /analytics/best-time` | `best_time` | Tab 5 |
| `GET /analytics/posting-frequency` | `posting_frequency` | Tab 5, Tab 6 |
| `GET /analytics/content-decay` | `content_decay` | Tab 4, Tab 6 |
| `GET /accounts/{id}/health` | `account_health` | Tab 2 |
| `GET /analytics/instagram/follower-history` | `follower_history` | Tab 2 |

**Ningún endpoint nuevo** — todo lo descrito en este plan usa datos ya en cache después del refresh normal.

---

## Lo que se descartó conscientemente y por qué

| Capacidad Zernio | Por qué no se incluye |
|-----------------|----------------------|
| Webhooks en tiempo real | El dashboard es local y se usa 1 vez al día. La complejidad de mantener un servidor de webhooks no tiene ROI para el caso de uso |
| Datos de Inbox (enviar mensajes, marcar leído) | Dashboard es 100% solo lectura — restricción explícita del plan original |
| Campañas de Ads | Fuera del scope — el dashboard es de contenido orgánico |
| Comment-to-DM workflows | Es publicación/automatización — no lectura |
| Contexto de audiencia del remitente (follower count del comentarista) | ⚠️ Requiere verificar si `list_inbox_comments` devuelve este campo. Si no lo devuelve, no hay forma de obtenerlo sin llamadas adicionales por cada comentarista |
| `GET /usage-stats` | Solo muestra consumo de API de Zernio — no aporta valor de contenido a la creadora |

---

## Prompt para Claude Code (implementación completa)

Pega esto en Claude Code cuando el dashboard base esté funcionando (Fase 9 completada):

```
Vamos a enriquecer las pestañas del dashboard con más valor. El dashboard base ya funciona
y todas las tablas SQLite están pobladas. NO necesitas llamar nuevos endpoints de Zernio.
Toda la información nueva se calcula desde los datos que ya están en cache.db.

Implementa estos cambios por orden de impacto:

--- TAB 1 (Métricas) ---
1. Bajo cada KPI, añade un delta % comparando últimos 30 días vs 30 días anteriores.
   Usa daily_metrics con rolling 180d que ya tenemos. Verde si sube, rojo si baja.
2. Calcula y muestra tasa de engagement = (likes+comments+saves+shares)/reach*100.
   Benchmark en caption: "Promedio IG: 1-3%"
3. Muestra el ratio guardados/likes con label "Índice de valor".
4. Añade una tarjeta "Mejor post del período" (el de más saves) con thumbnail pequeño
   y link al permalink.

--- TAB 3 (Audiencia) ---
5. Bajo el gráfico de países, añade tabla con país, % y bandera emoji.
   Añade texto: "Top 3 países = X% de tu audiencia"
6. Añade un st.info() que interprete si la audiencia es concentrada o dispersa
   (>60% en un país = concentrada; <30% = dispersa).
7. Resalta el rango de edad dominante con st.metric grande arriba de las barras.

--- TAB 4 (Posts) ---
8. Añade st.selectbox para ordenar por: Guardados / Alcance / Likes / Comentarios.
9. En cada card de post, infiere el formato desde el permalink:
   "/reel/" → 🎬 Reel | no contiene "/reel/" → 🖼 Post
10. En el expander de comentarios, muestra "X total · Y sustantivos" usando
    idea_filters.is_substantive_comment() para el conteo.

--- TAB 5 (Mejor Horario) ---
11. Debajo del heatmap, extrae los 3 mejores slots y muéstralos en texto:
    "🥇 Martes 19:00 · 🥈 Jueves 20:00 · 🥉 Miércoles 19:00"
12. Añade un indicador de cadencia: lee posting_frequency y muestra el bucket
    con mejor engagement como "Zona óptima: X-Y posts/semana".

--- TAB 6 (Frecuencia) ---
13. Añade línea de tendencia al scatter (calcúlala manualmente, sin scipy).
14. Añade barra semanal de cadencia real desde la tabla posts (contar posts por semana).
    Colorea verde las semanas que caen en la "zona óptima" de posting_frequency.

--- TAB 7 (Ideas) ---
15. Antes del botón de generar, muestra un st.expander "📊 Contexto disponible" con:
    - Conteo de comentarios totales y sustantivos (últimos 90d)
    - Conteo de DMs totales y sustantivos (últimos 30d)
    - Demografía dominante (edad y género top)
16. En cada card de idea, si tiene basis_post_ids, añade link:
    "[Ver post original →](permalink)" buscando el permalink en la tabla posts.

Después de cada tab, verifica en el browser que se ve correctamente antes de continuar
con el siguiente. Muéstrame screenshot o describe lo que ves.
```

---

## Checklist de aceptación del enriquecimiento

- [ ] Tab 1: los deltas % aparecen con color verde/rojo según dirección
- [ ] Tab 1: la tasa de engagement muestra un número razonable (1-10% para IG típico)
- [ ] Tab 1: la tarjeta "Mejor post" muestra thumbnail real y link funcional
- [ ] Tab 3: la tabla de países muestra porcentajes que suman 100% (o cerca)
- [ ] Tab 3: el st.info() de concentración/dispersión aparece con texto coherente
- [ ] Tab 4: el selector de ordenación cambia el orden del grid correctamente
- [ ] Tab 4: el badge 🎬/🖼 aparece en las cards según el permalink
- [ ] Tab 4: el conteo "X total · Y sustantivos" es coherente (Y ≤ X siempre)
- [ ] Tab 5: los 3 mejores slots en texto coinciden visualmente con el heatmap
- [ ] Tab 5: la cadencia óptima mostrada tiene sentido (entre 1 y 7 posts/semana)
- [ ] Tab 6: la línea de tendencia va en la dirección esperada según los puntos
- [ ] Tab 6: las barras semanales tienen al menos algunas semanas en verde
- [ ] Tab 7: el conteo de contexto muestra números reales (no ceros)
- [ ] Tab 7: el link "Ver post original" en ideas lleva al permalink de Instagram
