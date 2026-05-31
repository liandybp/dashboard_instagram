#!/bin/bash

# Script para instalar llama.cpp y configurar el servidor para Qwen3.6-27B

echo "Instalando llama.cpp..."

# Clonar o actualizar llama.cpp si no existe
if [ ! -d "/home/liandybp/llama.cpp" ]; then
    echo "Clonando llama.cpp..."
    git clone https://github.com/ggerganov/llama.cpp.git /home/liandybp/llama.cpp
fi

cd /home/liandybp/llama.cpp

# Compilar llama.cpp
echo "Compilando llama.cpp..."
make clean
make

# Verificar si el servidor está compilado
if [ -f "build/bin/llama-server" ]; then
    echo "llama-server compilado correctamente"
else
    echo "Error: No se pudo compilar llama-server"
    exit 1
fi

echo "Instalación completada."