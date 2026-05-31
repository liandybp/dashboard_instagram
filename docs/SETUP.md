# Guía de Instalación y Configuración

## Requisitos Previos

- **Python 3.9 o superior**
- **pip** (gestor de paquetes de Python)
- **Git** (opcional pero recomendado)
- Cuentas con APIs:
  - Zernio (con add-ons activados)
  - Anthropic Claude (para generación de ideas)

## Instalación Step-by-Step

### 1. Clonar o descargar el proyecto

```bash
# Con Git
git clone <url-del-repo>
cd dashboard_instagram

# O descargar ZIP y extraer
unzip dashboard_instagram.zip
cd dashboard_instagram
```

### 2. Crear entorno virtual Python

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
# Opción A: Desde requirements.txt
pip install -r requirements.txt

# Opción B: Instalar manualmente
pip install streamlit==1.39.0
pip install pandas==2.2.3
pip install plotly==5.24.0
pip install anthropic==0.97.0
pip install requests==2.32.3
pip install python-dotenv==1.0.1
pip install httpx==0.28.1
```

### 4. Configurar variables de entorno

#### Opción A: Archivo `env` (recomendado)

Crear archivo `env` en la raíz del proyecto:

```bash
# API Zernio
ZERNIO_API_KEY=sk_live_xxxxxxxxxxxxx
ZERNIO_ACCOUNT_ID=acc_xxxxxxxxxxxxx
ZERNIO_ACCOUNT_ID_YOUTUBE=acc_xxxxxxxxxxxxx

# API Anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

#### Opción B: Archivo `.env`

Similar al anterior, pero nombrado `.env` en lugar de `env`.

#### Opción C: Variables de entorno del sistema

```bash
# macOS / Linux
export ZERNIO_API_KEY="sk_live_xxxxxxxxxxxxx"
export ZERNIO_ACCOUNT_ID="acc_xxxxxxxxxxxxx"
export ZERNIO_ACCOUNT_ID_YOUTUBE="acc_xxxxxxxxxxxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxx"

# Windows (PowerShell)
$env:ZERNIO_API_KEY="sk_live_xxxxxxxxxxxxx"
$env:ZERNIO_ACCOUNT_ID="acc_xxxxxxxxxxxxx"
```

### 5. Verificar instalación

```bash
# Probar importación de módulos
python -c "import streamlit; print('✅ Streamlit OK')"
python -c "import pandas; print('✅ Pandas OK')"
python -c "import plotly; print('✅ Plotly OK')"
python -c "import anthropic; print('✅ Anthropic OK')"

# Validar conexión a APIs
python src/api/client.py
```

### 6. Ejecutar la aplicación

```bash
# Comando básico
streamlit run app.py

# Con puerto específico
streamlit run app.py --server.port=8501

# Con configuración adicional
streamlit run app.py \
  --server.port=8501 \
  --server.headless=true \
  --logger.level=info
```

La aplicación estará disponible en: **http://localhost:8501**

## Acceso a API Keys

### Zernio API Key

1. Ir a [Zernio Dashboard](https://app.zernio.com)
2. Settings → API Keys
3. Crear nueva key o copiar existente
4. Formato: `sk_live_...` (producción) o `sk_test_...` (desarrollo)

### Anthropic API Key

1. Ir a [Anthropic Console](https://console.anthropic.com)
2. API Keys → Create Key
3. Copiar key con prefijo `sk-ant-...`

## Troubleshooting de Instalación

### Error: "No module named 'streamlit'"

```bash
# Verificar entorno virtual está activo
which python  # Debería mostrar ruta dentro de venv/

# Reinstalar
pip install --upgrade streamlit==1.39.0
```

### Error: "ZERNIO_API_KEY must be provided"

```bash
# Verificar variable de entorno
echo $ZERNIO_API_KEY  # macOS/Linux
echo %ZERNIO_API_KEY%  # Windows

# O crear archivo env
cat > env << EOF
ZERNIO_API_KEY=sk_live_xxx
ZERNIO_ACCOUNT_ID=acc_xxx
EOF
```

### Error: "plotly.exceptions.PlotlyError"

```bash
# Actualizar Plotly
pip install --upgrade plotly==5.24.0

# Verificar versión
python -c "import plotly; print(plotly.__version__)"
```

### Puertos ocupados

```bash
# Si 8501 está en uso, usar otro puerto
streamlit run app.py --server.port=8502

# O matar proceso anterior
lsof -ti :8501 | xargs kill -9  # macOS/Linux
```

## Problemas de Conectividad

### Error: "Connection timeout"

```bash
# Verificar conexión a internet
ping api.zernio.com
ping console.anthropic.com

# Probar con cliente directo
python -c "
from src.api.client import ZernioClient
client = ZernioClient()
accounts = client.list_accounts()
print(accounts)
"
```

### Error: "SSL certificate verify failed"

```bash
# Opción A: Actualizar certificados
pip install --upgrade certifi

# Opción B: Desactivar verificación (NO RECOMENDADO en producción)
export REQUESTS_CA_BUNDLE=""
```

## Estructura de Directorios tras Instalación

```
dashboard_instagram/
├── venv/                   # Entorno virtual
├── src/                    # Código fuente
├── docs/                   # Documentación
├── prompts/               # Prompts de IA
├── data.nosync/           # Datos locales (caché)
│   └── cache.db
├── app.py                 # Punto de entrada
├── cache.py              # Manejo de caché
├── requirements.txt      # Dependencias
├── env                   # Variables de entorno ⚠️ NO en git
├── .env                  # Alternativa de variables
└── .gitignore           # Debe incluir: env, .env, venv/, *.db
```

## Configuración Avanzada

### Streamlit Config

Crear `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF355C"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = false
runOnSave = true
```

### Logging

```bash
# Habilitar debug logging
streamlit run app.py --logger.level=debug

# Guardar logs en archivo
streamlit run app.py 2>&1 | tee logs.txt
```

## Scripts Auxiliares

### Validar Endpoints API

```bash
python src/api/client.py
```

Valida todos los endpoints de Zernio e indica cuáles funcionan.

### Verificar Variables de Entorno

```bash
python show_env.py
```

Revisa qué variables están cargadas (sin mostrar valores sensibles).

## Actualización de Dependencias

```bash
# Verificar qué puede actualizarse
pip list --outdated

# Actualizar dependencia específica
pip install --upgrade streamlit

# Actualizar todo (NO RECOMENDADO en producción)
pip install -r requirements.txt --upgrade
```

## Despliegue en Producción

### Streamlit Cloud

1. Push del código a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar repo y rama
4. Configurar secrets en Streamlit Cloud settings

### Heroku

1. Crear `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.headless=true --server.enableCORS=false
```

2. Deployer:
```bash
heroku create mi-dashboard
git push heroku main
```

## Mantenimiento

### Backups

```bash
# Hacer backup de caché
cp data.nosync/cache.db data.nosync/cache.db.backup.$(date +%s)

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### Testing

```bash
# Verificar que todo funciona
python src/api/client.py  # APIs
python src/data/loader.py  # Data loading
streamlit run app.py      # UI
```

