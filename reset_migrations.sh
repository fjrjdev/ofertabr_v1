#!/bin/bash

echo "🔄 Resetando migrations e banco de dados..."

# Parar containers
echo "⏹️  Parando containers..."
docker-compose down

# Remover volumes (isso apaga o banco)
echo "🗑️  Removendo volumes do banco..."
docker-compose down -v

# Remover migrations antigas
echo "🗑️  Removendo migrations antigas..."
rm -f backend/alembic/versions/*.py
touch backend/alembic/versions/.gitkeep

# Recriar containers
echo "🐳 Recriando containers..."
docker-compose up -d

# Aguardar banco ficar pronto
echo "⏳ Aguardando PostgreSQL ficar pronto..."
sleep 10

# Criar migration automática
echo "📝 Criando migration automática..."
docker-compose exec -T api alembic revision --autogenerate -m "initial_setup"

# Executar migrations
echo "⚡ Executando migrations..."
docker-compose exec -T api alembic upgrade head

echo ""
echo "✅ Setup completo!"
echo ""
echo "🔐 Autenticação passwordless:"
echo "   Email padrão: admin@ofertabr.com"
echo "   Solicite código em: POST /api/v1/auth/request-code"
echo ""
echo "📚 Documentação: http://localhost:8000/docs"
echo ""

