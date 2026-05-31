# Layout Final - Pestaña Audiencia (Instagram)

**Fecha:** 31 de Mayo de 2026  
**Archivo:** `src/components/tabs/audience_tab.py` (líneas 83-127)  
**Status:** ✅ Completado

---

## Estructura Visual

```
Página: 👥 Audiencia → Instagram

═══════════════════════════════════════════════════════════════════

1. MÉTRICA DE EDAD DOMINANTE (antes de los gráficos)
   Rango de edad dominante: 25-34 años (30.0%)

2. INFORMACIÓN DE GÉNERO (antes de los gráficos)
   Tu audiencia es 60.0% Mujer / 40.0% Hombre

3. FILA DE 4 GRÁFICOS IGUALES (st.columns(4))
   
   ┌──────────────┬──────────────┬──────────────┬──────────────┐
   │    Edad      │   Género     │     País     │    Ciudad    │
   │  (gráfico)   │  (gráfico)   │  (gráfico)   │  (gráfico)   │
   │   de               de              de             de       │
   │ distribución  distribución   distribución   distribución   │
   └──────────────┴──────────────┴──────────────┴──────────────┘

      COL1            COL2           COL3           COL4
   (sin tabla)    (sin tabla)   (con tabla)    (sin tabla)

4. TABLA DENTRO DE COL3 (debajo del gráfico País)

   ┌──────────────────────────────┐
   │ Top 5 = 90.0% de tu audiencia │
   ├────────────┬─────────────────┤
   │   País     │  % audiencia    │
   ├────────────┼─────────────────┤
   │ España     │     40.0%       │
   │ México     │     35.0%       │
   │ EE.UU.     │     25.0%       │
   │ Colombia   │     20.0%       │
   │ Argentina  │     15.0%       │
   └────────────┴─────────────────┘
      (5 filas)

5. INFORMACIÓN DE CONCENTRACIÓN/DISPERSIÓN (después de COL3)

   Audiencia concentrada: tu país #1 supera el 60%.
   Buen escenario para un nicho local.
   
   ← O también puede ser:
   "Audiencia balanceada: tienes una mezcla sana..."
   "Audiencia dispersa: tu país #1 está por debajo..."
```

---

## Código Técnico

### Estructura

```python
# Línea 83: Setup de 4 columnas
col1, col2, col3, col4 = st.columns(4)

# Líneas 85-88: COL1 - Gráfico de Edad (sin tabla)
with col1:
    st.subheader("Edad")
    st.plotly_chart(fig_age, ...)

# Líneas 90-93: COL2 - Gráfico de Género (sin tabla)
with col2:
    st.subheader("Género")
    st.plotly_chart(fig_gender, ...)

# Líneas 95-111: COL3 - Gráfico de País + Tabla debajo
with col3:
    st.subheader("País")
    st.plotly_chart(fig_country, ...)
    
    # Tabla Top 5 DENTRO de col3
    if not df_country.empty:
        df_country_sorted = df_country.sort_values("pct", ascending=False)
        top5_pct = df_country_sorted.head(5)["pct"].sum()
        st.caption(f"Top 5 = {top5_pct:.1f}% de tu audiencia")
        st.dataframe(
            df_country_sorted.head(5)[["label", "pct"]].rename(
                columns={"label": "País", "pct": "% audiencia"}
            ),
            use_container_width=True,
            hide_index=True,
        )

# Líneas 113-116: COL4 - Gráfico de Ciudad (sin tabla)
with col4:
    st.subheader("Ciudad")
    st.plotly_chart(fig_city, ...)

# Líneas 118-127: Info de concentración/dispersión (fuera de cols)
if not df_country.empty:
    df_country_sorted = df_country.sort_values("pct", ascending=False)
    top_country_pct = float(df_country_sorted.iloc[0]["pct"])
    if top_country_pct > 60:
        st.info("Audiencia concentrada...")
    elif top_country_pct < 30:
        st.info("Audiencia dispersa...")
    else:
        st.info("Audiencia balanceada...")
```

---

## Detalles Clave

| Elemento | Ubicación | Contenido |
|----------|-----------|----------|
| **Métrica Edad** | Antes de gráficos | "Rango de edad dominante: X años (Y%)" |
| **Info Género** | Antes de gráficos | "Tu audiencia es X% Mujer / Y% Hombre" |
| **Fila Gráficos** | st.columns(4) | 4 gráficos en línea horizontal |
| **Col1 (Edad)** | Gráfico solo | Sin tabla debajo |
| **Col2 (Género)** | Gráfico solo | Sin tabla debajo |
| **Col3 (País)** | Gráfico + Tabla | Tabla Top 5 debajo del gráfico |
| **Col4 (Ciudad)** | Gráfico solo | Sin tabla debajo |
| **Tabla Top 5** | Dentro de col3 | 5 filas, columnas: País, % audiencia |
| **Info Concentración** | Después de cols | st.info() con interpretación |

---

## Tabla Top 5 - Especificaciones

- **Ubicación:** Dentro de `col3`, después de `st.plotly_chart()`
- **Indentación:** Dentro del bloque `with col3:`
- **Rows:** Exactamente 5 (`.head(5)`)
- **Columnas:**
  - "País" (de "label")
  - "% audiencia" (de "pct")
- **Encabezado:** `st.caption(f"Top 5 = {top5_pct:.1f}% de tu audiencia")`
- **Índice:** Oculto (`hide_index=True`)
- **Ancho:** `use_container_width=True`

---

## Validación

✓ **4 gráficos en una línea**
  - st.columns(4) en línea 83
  - Todos dentro del mismo nivel de indentación

✓ **Tabla solo en Col3**
  - `with col3:` contiene gráfico + tabla (líneas 100-111)
  - Otros col contienen solo gráfico

✓ **Tabla muestra Top 5**
  - `.head(5)` limita a 5 filas
  - Suma de 5 porcentajes en caption

✓ **Información de concentración**
  - Al final, después de cerrar todos los `with`
  - Interpreta correctamente >60%, <30%, 30-60%

✓ **Código válido**
  - Indentación correcta
  - Sin errores de sintaxis
  - Estructura anidada válida

---

## Cómo Probar

```bash
streamlit run app.py
```

Navegación:
1. Ir a pestaña: **👥 Audiencia**
2. Hacer clic en sub-pestaña: **Instagram**

Verificar:
- [ ] Métrica de edad dominante visible (arriba)
- [ ] Información de género visible (arriba)
- [ ] 4 gráficos en una línea horizontal
- [ ] Tabla Top 5 Países debajo del gráfico País
- [ ] Tabla muestra exactamente 5 filas
- [ ] Tabla tiene columnas: "País" y "% audiencia"
- [ ] Encima de tabla: "Top 5 = X%"
- [ ] Info de concentración/dispersión visible (abajo)
- [ ] Otras columnas (Edad, Género, Ciudad) sin tabla

---

**Change ID:** AUD_4COLS_TOP5_IN_COL3_20260531  
**Status:** ✅ Ready for Production

