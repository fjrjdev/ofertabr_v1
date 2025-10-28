#!/bin/bash

# Script para setup inicial do frontend Next.js
set -e

echo "🚀 Setup do Frontend OfertaBR com Next.js"
echo "==========================================="
echo ""

# Verificar se já existe um projeto Next.js
if [ -f "package.json" ] && [ -d "app" ]; then
    echo "✅ Projeto Next.js já está inicializado!"
    echo ""
else
    echo "📦 Inicializando projeto Next.js..."
    echo ""
    
    # Criar projeto Next.js com TypeScript e Tailwind
    npx create-next-app@latest . \
        --typescript \
        --tailwind \
        --app \
        --no-src-dir \
        --import-alias "@/*" \
        --yes
    
    echo ""
    echo "✅ Projeto Next.js criado com sucesso!"
fi

# Criar arquivo .env.local se não existir
if [ ! -f ".env.local" ]; then
    echo ""
    echo "📝 Criando arquivo .env.local..."
    cat > .env.local << EOF
# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Adicione outras variáveis de ambiente aqui
EOF
    echo "✅ Arquivo .env.local criado!"
fi

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo ""
    echo "📦 Instalando dependências..."
    npm install
    echo "✅ Dependências instaladas!"
fi

echo ""
echo "✨ Setup completo!"
echo ""
echo "🎯 Próximos passos:"
echo ""
echo "1️⃣  Para rodar em modo desenvolvimento local:"
echo "    npm run dev"
echo ""
echo "2️⃣  Para rodar com Docker (modo dev):"
echo "    docker-compose -f docker-compose.frontend.yml --profile dev up frontend-dev"
echo ""
echo "3️⃣  Para rodar com Docker (modo produção):"
echo "    docker-compose -f docker-compose.frontend.yml up frontend"
echo ""
echo "4️⃣  Para rodar stack completo (backend + frontend):"
echo "    cd .. && docker-compose -f docker-compose.full.yml up -d"
echo ""
echo "📚 Documentação: veja README_DOCKER_SETUP.md e DOCKER.md"
echo ""

