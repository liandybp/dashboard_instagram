# Actualización - Feature Audiencia

**Fecha Last Update:** 31-05-2026

## Cambio Realizado

En la pestaña **Audiencia / Instagram**, se realizó una actualización:

### Modificación
- **Tabla de países** movida a la columna **col4 (derecha)**
- Ahora muestra **Top 5 países** (fue Top 3)
- Mantiene la **misma altura** que los gráficos

### Antes
```
[Edad] [Género] [País + Tabla Top3 al pie] [Ciudad]
```

### Ahora
```
[Edad] [Género] [País] [Top 5 Tabla]
                       (en col4)
[Ciudad] (full width abajo)
```

### Archivo
- `src/components/tabs/audience_tab.py` - líneas 83-125

### Cambios Técnicos
- `col4` ahora contiene la tabla en lugar del gráfico de Ciudad
- Tabla usa `.head(5)` en lugar de mostrar toda la tabla
- Ciudad se muestra debajo en full width
- Mantiene toda la lógica de concentración/dispersión

### Beneficios
✅ Tabla al lado izquierdo (col4 = columna derecha)  
✅ Top 5 proporciona más contexto  
✅ Misma altura visual que otros gráficos  
✅ Mantiene todos los datos e interpretaciones  

---

**Ver documento completo:** `docs/CAMBIO_AUDIENCIA_TAB.md`


