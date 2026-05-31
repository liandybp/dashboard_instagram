#!/bin/bash

# Script para iniciar el servidor llama.cpp y el dashboard Streamlit

echo "Iniciando servidor llama.cpp..."

# Directorio donde se encuentra llama.cpp
LLAMA_CPP_DIR="/home/liandybp/llama.cpp"

# Usar modelo Qwen3.5 disponible
MODEL_PATH="/home/liandybp/llama.cpp/models/ggml-vocab-qwen35.gguf"

if [ ! -f "$MODEL_PATH" ]; then
    echo "Modelo Qwen3.5 no encontrado en $MODEL_PATH"
    echo "Por favor descargue el modelo y colóquelo en este directorio"
    exit 1
fi

# Iniciar el servidor llama.cpp en segundo plano
echo "Iniciando servidor llama.cpp..."
cd "$LLAMA_CPP_DIR"

# Usar el comando correcto para iniciar el servidor
./build/bin/llama-server \
    --port 8080 \
    --host 0.0.0.0 \
    --model "$MODEL_PATH" \
    --ctx-size 8192 \
    --n-gpu-layers 35 \
    --temp 0.95 \
    --threads 8 \
    --log-disable \
    --nobrowser &

# Guardar el PID del proceso
LLAMA_PID=$!

echo "Servidor llama.cpp iniciado con PID $LLAMA_PID"

# Esperar un momento para que el servidor se inicie
sleep 5

# Verificar si el servidor está corriendo
if kill -0 $LLAMA_PID 2>/dev/null; then
    echo "Servidor llama.cpp está corriendo"
else
    echo "Error: Servidor llama.cpp no se inició correctamente"
    exit 1
fi

echo "Iniciando dashboard Streamlit..."
# Iniciar el dashboard Streamlit
cd /home/liandybp/PyCharmMiscProject/greter/dashboard_instagram
streamlit run app_fixed.py --server.enableCORS=false --server.enableXsrfProtection=false

# Limpiar al finalizar
echo "Limpiando procesos..."
kill $LLAMA_PID 2>/dev/null || true