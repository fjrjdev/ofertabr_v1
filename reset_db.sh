#!/bin/bash

echo "🔄 Resetando banco de dados..."

# Parar containers
echo "⏹️  Parando containers..."
docker-compose down

# Remover apenas o volume do banco
echo "🗑️  Removendo volume do PostgreSQL..."
docker volume rm ofertabr_v1_postgres_data 2>/dev/null || true

# Recriar containers
echo "🐳 Recriando containers..."
docker-compose up -d

# Aguardar banco ficar pronto
echo "⏳ Aguardando PostgreSQL ficar pronto..."
sleep 10

# Executar migrations
echo "⚡ Executando migrations..."
docker-compose exec -T api alembic upgrade head

echo ""
echo "✅ Banco resetado com sucesso!"
echo ""
echo "🔐 Autenticação passwordless:"
echo "   Email padrão: admin@ofertabr.com"
echo "   Solicite código em: POST /api/v1/auth/request-code"
echo ""
