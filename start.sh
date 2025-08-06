#!/bin/bash
# Script de inicialização para Render

# Criar diretório para banco se não existir
mkdir -p /opt/render/project/src

# Iniciar a aplicação
uvicorn app.main:app --host 0.0.0.0 --port $PORT