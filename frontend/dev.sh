#!/bin/bash

# Script rápido para desenvolvimento com Docker
# Uso: bash dev.sh (execute na pasta frontend/)
# Ou: bash frontend/dev.sh (execute na raiz do projeto)

echo "🚀 Iniciando frontend em modo desenvolvimento com Docker..."
echo ""
echo "O frontend estará disponível em: http://localhost:3000"
echo "Para parar: Ctrl+C"
echo ""

# Detecta se está na pasta frontend ou na raiz
if [ -f "docker-compose.yml" ]; then
    # Está na raiz do projeto
    docker-compose --profile dev up frontend-dev
else
    # Está na pasta frontend
    cd ..
    docker-compose --profile dev up frontend-dev
fi

