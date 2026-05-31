#!/bin/bash

# Script para iniciar el servidor llama.cpp con Qwen3.6-27B

echo "Iniciando servidor llama.cpp..."

# Directorio donde se encuentra llama.cpp
LLAMA_CPP_DIR="/home/liandybp/llama.cpp"

# Usar modelo Qwen3.6-27B descargado
MODEL_PATH="/home/liandybp/models/qwen3.6-27b/Qwen3.6-27B-UD-Q4_K_XL.gguf"

if [ ! -f "$MODEL_PATH" ]; then
    echo "Modelo Qwen3.6-27B no encontrado en $MODEL_PATH"
    exit 1
fi

# Iniciar el servidor llama.cpp
echo "Iniciando servidor con modelo: $MODEL_PATH"
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
    --log-disable

echo "Servidor llama.cpp iniciado en http://localhost:8080"