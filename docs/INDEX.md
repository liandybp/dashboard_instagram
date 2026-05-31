# Documentación del Dashboard Instagram - Índice Master

## 📚 Guías Principales

### 🎉 Status del Proyecto
0. **[docs/IMPLEMENTACION_RESUMEN.md](docs/IMPLEMENTACION_RESUMEN.md)** ← ✅ 100% Completado
   - Resumen ejecutivo de todas las features implementadas
   - Checklist validado (14/14 tests pasados)
   - Mapa de cambios por archivo
   - Listo para producción

### Usuarios Nuevos
1. **[docs/SETUP.md](docs/SETUP.md)** ← Empieza aquí
   - Instalación paso a paso
   - Configuración de variables de entorno
   - Troubleshooting de instalación

2. **[docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** ← Referencia rápida
   - Comandos más usados
   - Estructura de datos
   - Errores comunes y soluciones

### Arquitectos / Desarrolladores
3. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** ← Diseño general
   - Estructura del proyecto
   - Flujos de datos
   - Componentes principales
   - Performance y caché

4. **[docs/API_GUIDE.md](docs/API_GUIDE.md)** ← Integración Zernio
   - Endpoints disponibles
   - Ejemplos de respuesta
   - Manejo de errores
   - Add-ons requeridos

5. **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** ← Para code
   - Convenciones de código
   - Cómo agregar pestañas
   - Testing y debugging
   - CI/CD setup

### Operaciones
6. **[CLAUDE.md](CLAUDE.md)** ← Notas técnicas
   - 8 gotchas críticos solucionados
   - Política de retención de datos
   - Validaciones completadas

---

## 🎯 Por Caso de Uso

### "Quiero ejecutar el dashboard"
```
1. docs/SETUP.md → instalación
2. streamlit run app.py
3. docs/QUICK_REFERENCE.md → si hay problemas
```

### "Necesito entender cómo funciona"
```
1. docs/ARCHITECTURE.md → visión general
2. docs/API_GUIDE.md → endpoints
3. docs/DEVELOPMENT.md → detalles técnicos
```

### "Quiero agregar una nueva pestaña"
```
1. docs/ARCHITECTURE.md → componentes
2. docs/DEVELOPMENT.md → tutorial
3. docs/QUICK_REFERENCE.md → snippets de código
```

### "Tengo un error / quiero debuggear"
```
1. docs/QUICK_REFERENCE.md → tabla de errores
2. docs/SETUP.md → troubleshooting
3. docs/DEVELOPMENT.md → debugging tools
```

### "Necesito integrar otro endpoint"
```
1. docs/API_GUIDE.md → endpoints disponibles
2. docs/DEVELOPMENT.md → cómo agregar endpoint
3. docs/ARCHITECTURE.md → normalización de datos
```

---

## 📊 Mapa de Archivos del Proyecto

```
dashboard_instagram/
├── README.md                    ← Información general (este)
├── CLAUDE.md                    ← Notas técnicas del proyecto
├── requirements.txt             ← Dependencias Python
├── app.py                       ← Punto de entrada Streamlit
├── cache.py                     ← Caché local SQLite
│
├── src/                         ← Código fuente
│   ├── api/
│   │   └── client.py           ← ZernioClient (ver API_GUIDE.md)
│   │
│   ├── components/
│   │   ├── theme.py            ← Branding y tema
│   │   ├── ideas.py            ← Generación con Claude
│   │   ├── idea_filters.py     ← Filtros de comentarios
│   │   └── tabs/               ← 7 pestañas del dashboard
│   │       ├── base_tab.py
│   │       ├── metrics_tab.py
│   │       ├── health_tab.py
│   │       ├── audience_tab.py
│   │       ├── posts_tab.py
│   │       ├── best_time_tab.py
│   │       ├── frequency_tab.py
│   │       └── ideas_tab.py
│   │
│   └── data/
│       └── loader.py           ← Carga y normalización de datos
│
├── prompts/
│   └── ideas_system.md         ← Prompt para Claude AI
│
└── docs/                       ← DOCUMENTACIÓN
    ├── ARCHITECTURE.md         ← Arquitectura (leer primero!)
    ├── SETUP.md               ← Instalación
    ├── API_GUIDE.md           ← Endpoints Zernio
    ├── DEVELOPMENT.md         ← Para desarrolladores
    ├── QUICK_REFERENCE.md     ← Referencia rápida
    └── INDEX.md               ← Este archivo
```

---

## 🔗 Referencias Cruzadas Rápidas

### Si quiero... encontré en...
| Necesidad | Documento |
|-----------|-----------|
| Instalar el proyecto | SETUP.md |
| Entender flujo general | ARCHITECTURE.md |
| Ver estructura datos | ARCHITECTURE.md, QUICK_REFERENCE.md |
| Usar API Zernio | API_GUIDE.md |
| Debuggear un error | QUICK_REFERENCE.md, SETUP.md |
| Agregar pestaña | DEVELOPMENT.md, QUICK_REFERENCE.md |
| Agregar endpoint | DEVELOPMENT.md, API_GUIDE.md |
| Testing | DEVELOPMENT.md |
| Deploy | SETUP.md, DEVELOPMENT.md |
| Gotchas conocidos | CLAUDE.md |
| Convenciones código | DEVELOPMENT.md |

---

## 🚀 Quick Start (3 pasos)

### 1. Instalar
```bash
cp env.example env  # Editar con tus APIs
pip install -r requirements.txt
```

### 2. Ejecutar
```bash
streamlit run app.py
```

### 3. Leer  
👉 **[docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** para comandos y atajos

---

## 📞 Support & Troubleshooting

### Error al instalar
→ [docs/SETUP.md - Troubleshooting de Instalación](docs/SETUP.md#troubleshooting-de-instalaci%C3%B3n)

### Error al ejecutar
→ [docs/QUICK_REFERENCE.md - Errores Comunes](docs/QUICK_REFERENCE.md#errores-comunes)

### No carga datos
→ [docs/SETUP.md - Problemas de Conectividad](docs/SETUP.md#problemas-de-conectividad)

### Quiero desarrollar
→ [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

### Pregunta sobre endpoints
→ [docs/API_GUIDE.md](docs/API_GUIDE.md)

---

## 📋 Checklist para Nuevos Desarrolladores

- [ ] Leer [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - 15 min
- [ ] Ejecutar instalación [docs/SETUP.md](docs/SETUP.md) - 10 min
- [ ] Probar dashboard localmente - 5 min
- [ ] Revisar [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) - 5 min
- [ ] Leer [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) para contribuir - 20 min
- [ ] Ejecutar `python src/api/client.py` para validar APIs

**Tiempo total: ~1 hora**

---

## 🏗️ Arquitectura en 60 Segundos

```
┌─────────────────────────────────────┐
│       Streamlit UI (app.py)         │
│  7 Pestañas: Métricas, Salud, ...  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Data Layer (src/data/loader.py)   │
│  - Carga desde API Zernio          │
│  - Normaliza múltiples formatos    │
│  - Fallback defensivo              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Client API (src/api/client.py)    │
│  - Zernio API wrapper              │
│  - Retry/backoff automático        │
│  - Error handling robusta          │
└──────────────┬──────────────────────┘
               │
               ▼
      ┌─────────────────┐
      │ Zernio API      │
      │ Datos reales    │
      └─────────────────┘
```

---

## 📊 Stack Tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Frontend | Streamlit | 1.39.0 |
| Visualización | Plotly | 5.24.0 |
| Data Processing | Pandas | 2.2.3 |
| API Client | Requests | 2.32.3 |
| AI/NLP | Anthropic | 0.97.0 |
| Environment | python-dotenv | 1.0.1 |

---

## 📝 Convenciones

- **Archivos de documentación:** Markdown (.md)
- **Código Python:** PEP 8, Black formatted
- **Nombres archivos:** snake_case.py
- **Nombres clases:** PascalCase
- **Nombres variables:** snake_case
- **Docstrings:** Google style

---

## 🔐 Seguridad

⚠️ **IMPORTANTE:**
- NUNCA commitear archivos `env` o `.env`
- NUNCA mostrar API keys en código
- Usar `os.getenv()` para credenciales
- Verificar `.gitignore` incluya credenciales

Ver [SETUP.md - Configurar variables](docs/SETUP.md#configurar-variables-de-entorno)

---

## 📈 Roadmap

Mejoras planificadas:
- [ ] Caché distribuido (Redis)
- [ ] Export a PDF/PNG
- [ ] ML predictions
- [ ] Google Analytics integration
- [ ] Programación de posts
- [ ] Análisis competitive

---

## 📞 Contacto & Help

- **Issues técnicos:** Ver [docs/SETUP.md](docs/SETUP.md) primero
- **Questions arquitectura:** Ver [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Development help:** Ver [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
- **API questions:** Ver [docs/API_GUIDE.md](docs/API_GUIDE.md)

---

**Última actualización: 31 de Mayo, 2024**  
**Documentación rev: 2.0**


