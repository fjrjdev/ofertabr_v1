# Dockerfile para Next.js - Multi-stage build otimizado

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apk add --no-cache libc6-compat

# Copiar arquivos de dependências
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./

# Instalar dependências baseado no gerenciador de pacotes disponível
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copiar dependências do stage anterior
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Variáveis de ambiente para o build
# Next.js coleta telemetria anônima - desabilitar em produção
ENV NEXT_TELEMETRY_DISABLED 1

# Build da aplicação
# Se usar pnpm: RUN corepack enable pnpm && pnpm run build
# Se usar yarn: RUN yarn build
RUN npm run build

# Stage 3: Runner (Imagem final)
FROM node:20-alpine AS runner
WORKDIR /app

# Adicionar grupo e usuário não-root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Desabilitar telemetria
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production

# Copiar arquivos públicos
COPY --from=builder /app/public ./public

# Copiar arquivos de build do Next.js
# Standalone mode cria uma estrutura otimizada
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Mudar para usuário não-root
USER nextjs

# Expor porta
EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Comando para iniciar a aplicação
CMD ["node", "server.js"]

