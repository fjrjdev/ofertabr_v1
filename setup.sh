#!/bin/bash

echo "🚀 Setup OfertaBR v1"
echo ""

# Verificar se .env do backend existe
if [ ! -f backend/.env.backend ]; then
    echo "⚙️  Criando arquivo backend/.env.backend..."
    cp env.example.txt backend/.env.backend
    echo "✅ Arquivo backend/.env.backend criado!"
else
    echo "✅ Arquivo backend/.env.backend já existe"
fi

echo ""
echo "🐳 Iniciando containers..."
docker-compose up -d

echo ""
echo "⏳ Aguardando PostgreSQL ficar pronto..."
sleep 10

echo ""
echo "⚡ Executando migrations..."
docker-compose exec -T api alembic upgrade head


echo ""
echo "✅ Setup completo!"
echo "📚 Acesse: http://localhost:8000/docs"
echo ""
