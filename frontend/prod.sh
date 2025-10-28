#!/bin/bash

# Script rápido para produção com Docker
# Uso: bash prod.sh (execute na pasta frontend/)
# Ou: bash frontend/prod.sh (execute na raiz do projeto)

echo "🚀 Iniciando frontend em modo produção com Docker..."
echo ""

# Detecta se está na pasta frontend ou na raiz
if [ -f "docker-compose.yml" ]; then
    # Está na raiz do projeto
    docker-compose --profile frontend up -d frontend
else
    # Está na pasta frontend
    cd ..
    docker-compose --profile frontend up -d frontend
fi

echo ""
echo "✅ Frontend iniciado em background!"
echo "O frontend estará disponível em: http://localhost:3000"
echo ""
echo "Ver logs: docker-compose logs -f frontend"
echo "Parar: docker-compose stop frontend"

