# 🎯 OfertaBR v1

**Plataforma automatizada de newsletter com web scraping, AI e autenticação passwordless**

Sistema completo para captura automatizada de ofertas/produtos através de web scraping com n8n + AI, gerenciamento de newsletters e envio automático para subscribers.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias](#-tecnologias)
- [Funcionalidades](#-funcionalidades)
- [Instalação e Setup](#-instalação-e-setup)
- [Autenticação](#-autenticação)
- [API Endpoints](#-api-endpoints)
- [Integração com n8n](#-integração-com-n8n)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Scripts Úteis](#-scripts-úteis)
- [Configuração](#-configuração)

---

## 🚀 Sobre o Projeto

OfertaBR é uma plataforma que automatiza a curadoria e distribuição de ofertas:

1. **Captura**: Web scraping automatizado via n8n + AI extrai produtos de sites
2. **Armazena**: Dados estruturados salvos em PostgreSQL com cache Redis
3. **Cria**: Newsletters personalizadas com produtos selecionados
4. **Envia**: Distribuição automática via Brevo para lista de subscribers
5. **Gerencia**: Sistema completo de inscrições e cancelamentos

### Principais Diferenciais

- ✨ **Autenticação Passwordless**: Login sem senhas usando códigos temporários ou magic links
- 🤖 **AI**: Google Gemini API para extração inteligente de dados
- ⚡ **Alta Performance**: Cache Redis para consultas otimizadas
- 📦 **Batch Processing**: Processamento em lote de múltiplos produtos
- 🎨 **Templates Modernos**: Emails responsivos com Jinja2

---

## 🛠️ Tecnologias

### Backend

- **FastAPI** - Framework web moderno e rápido
- **Python 3.12** - Linguagem principal
- **SQLAlchemy 2.0** - ORM async para PostgreSQL
- **Pydantic v2** - Validação de dados
- **Alembic** - Migrations de banco de dados

### Infraestrutura

- **PostgreSQL 16** - Banco relacional principal
- **Redis 7** - Cache e sessões
- **Docker & Docker Compose** - Containerização

### Integrações

- **JWT** - Tokens stateless para autenticação
- **Brevo (SendinBlue)** - Envio transacional de emails
- **n8n** - Orquestração de workflows e web scraping
- **Google Gemini API** - Extração inteligente de dados

### Frontend

- **Next.js 16** - Framework React
- **TypeScript** - Type safety
- **Tailwind CSS** - Estilização

---

## ✨ Funcionalidades

### 🔐 Autenticação Passwordless

- Login via código de 6 dígitos (email)
- Magic links (acesso com um clique)
- JWT tokens válidos por 7 dias
- Gerenciamento de emails autorizados

### 📰 Scraped Content

- Captura automatizada via n8n + AI
- Batch processing (até 100 produtos/request)
- Cache Redis para performance
- Campos: nome, preço, desconto, imagens, etc.

### 📧 Newsletters

- Criação e gerenciamento de edições
- Templates HTML responsivos
- Envio em lote para subscribers
- Preview antes do envio

### 👥 Subscribers

- Inscrição pública com verificação de email
- Cancelamento simples
- Soft delete (mantém histórico)
- Gerenciamento completo para admins

---

## 📦 Instalação e Setup

### Pré-requisitos

- Docker & Docker Compose
- Git

### Instalação

```bash
# 1. Clone o repositório
git clone <repository-url>
cd ofertabr_v1

# 2. Execute o script de setup
bash setup.sh
```

O script `setup.sh` automaticamente:

- Cria arquivo `backend/.env.backend` se não existir
- Inicia containers Docker (PostgreSQL, Redis, API, n8n)
- Aguarda PostgreSQL ficar pronto
- Executa migrations do banco

### Acesso

- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Alternativa (ReDoc)**: http://localhost:8000/redoc
- **n8n Interface**: http://localhost:5678 (admin/admin123)
- **Frontend**: http://localhost:3000
- **Health Check**: http://localhost:8000/health

---

## 🔐 Autenticação

O sistema usa autenticação passwordless. Não há senhas - apenas emails autorizados e códigos temporários.

### Fluxo de Autenticação

**Opção 1: Código de 6 dígitos**

```bash
# 1. Solicitar código
curl -X POST http://localhost:8000/api/v1/auth/request-code \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@ofertabr.com"}'

# 2. Verificar código (recebido por email)
curl -X POST http://localhost:8000/api/v1/auth/verify-code \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@ofertabr.com", "code": "123456"}'

# Response: {"access_token": "eyJ...", "token_type": "bearer"}
```

**Opção 2: Magic Link**

```bash
# Solicitar magic link
curl -X POST http://localhost:8000/api/v1/auth/request-magic-link \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@ofertabr.com"}'

# Clicar no link recebido por email (acesso automático)
```

**Usar Token nas Requisições**

```bash
curl -X GET http://localhost:8000/api/v1/newsletters \
  -H "Authorization: Bearer eyJ..."
```

---

## 📡 API Endpoints

### 🔓 Endpoints Públicos

| Método | Endpoint                          | Descrição                      |
| ------ | --------------------------------- | ------------------------------ |
| `POST` | `/api/v1/auth/request-code`       | Solicitar código de acesso     |
| `POST` | `/api/v1/auth/verify-code`        | Verificar código e obter token |
| `POST` | `/api/v1/auth/request-magic-link` | Solicitar magic link           |
| `GET`  | `/api/v1/auth/verify-magic`       | Verificar magic link           |
| `POST` | `/api/v1/auth/service-token`      | Token para serviços (n8n)      |
| `POST` | `/api/v1/subscribers/`            | Inscrever na newsletter        |
| `POST` | `/api/v1/subscribers/unsubscribe` | Cancelar inscrição             |
| `GET`  | `/health`                         | Status da API                  |

### 🔒 Endpoints Protegidos

#### Scraped Content

| Método   | Endpoint                              | Descrição                |
| -------- | ------------------------------------- | ------------------------ |
| `POST`   | `/api/v1/scraped_content/batch`       | Criar múltiplos produtos |
| `GET`    | `/api/v1/scraped_content/`            | Listar produtos          |
| `GET`    | `/api/v1/scraped_content/unprocessed` | Listar não processados   |
| `GET`    | `/api/v1/scraped_content/{id}`        | Buscar por ID            |
| `PATCH`  | `/api/v1/scraped_content/{id}`        | Atualizar produto        |
| `DELETE` | `/api/v1/scraped_content/{id}`        | Deletar produto          |

#### Newsletters

| Método | Endpoint                        | Descrição          |
| ------ | ------------------------------- | ------------------ |
| `POST` | `/api/v1/newsletters/`          | Criar newsletter   |
| `GET`  | `/api/v1/newsletters/`          | Listar newsletters |
| `POST` | `/api/v1/newsletters/{id}/send` | Enviar newsletter  |

#### Subscribers (Admin)

| Método | Endpoint                               | Descrição          |
| ------ | -------------------------------------- | ------------------ |
| `GET`  | `/api/v1/subscribers/`                 | Listar subscribers |
| `GET`  | `/api/v1/subscribers/by-email/{email}` | Buscar por email   |

#### Auth Admin

| Método | Endpoint                          | Descrição                  |
| ------ | --------------------------------- | -------------------------- |
| `POST` | `/api/v1/auth/admin/add-email`    | Adicionar email autorizado |
| `POST` | `/api/v1/auth/admin/remove-email` | Remover email autorizado   |
| `GET`  | `/api/v1/auth/admin/list-emails`  | Listar emails autorizados  |

---

## 🔗 Integração com n8n

O n8n automatiza a captura de produtos através de web scraping + AI.

### Workflow Simplificado

```
Trigger (Cron) → HTTP Scraping → OpenAI → OfertaBR API
```

### Configuração

1. Acesse: http://localhost:5678
2. Login: `admin` / `admin123`
3. Importe workflow de `n8n_workflows/`
4. Configure credenciais OpenAI e OfertaBR

### Exemplo de Payload para Batch

```json
[
  {
    "title": "Notebook Dell Inspiron 15",
    "source_url": "https://exemplo.com/produto-1",
    "product_name": "Notebook Dell Inspiron 15 i7 16GB",
    "current_price": 3499.99,
    "old_price": 4999.99,
    "discount_percentage": 30,
    "installments": "12x R$ 291,67 sem juros",
    "free_shipping": true,
    "images": [
      {
        "image_url": "https://exemplo.com/img1.jpg",
        "is_featured": true,
        "display_order": 1
      }
    ]
  }
]
```

**Endpoint para envio:** `POST /api/v1/scraped_content/batch`  
**Header:** `Authorization: Bearer {token}`

---

## 📁 Estrutura do Projeto

```
ofertabr_v1/
├── backend/                      # Backend FastAPI
│   ├── alembic/                  # Migrations
│   ├── app/
│   │   ├── api/v1/               # Endpoints REST
│   │   ├── core/                 # Configurações centrais
│   │   ├── models/               # SQLAlchemy models
│   │   ├── repositories/         # Acesso a dados
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Lógica de negócio
│   │   └── templates/emails/     # Templates HTML
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/                     # Frontend Next.js
│   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── types/
│   ├── package.json
│   └── Dockerfile
│
├── n8n_workflows/                # Workflows n8n
├── docker-compose.yml            # Orquestração
└── setup.sh                      # Setup inicial
```

---

## 🛠️ Scripts Úteis

### Setup Inicial

```bash
bash setup.sh
```

### Reset do Banco

```bash
bash reset_db.sh
```

### Reset Migrations

```bash
bash reset_migrations.sh
```

### Docker Commands

```bash
# Ver logs
docker-compose logs -f api

# Acessar shell
docker-compose exec api bash

# Reiniciar
docker-compose restart

# Parar tudo
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

### Migrations (dentro do container)

```bash
# Criar migration
docker-compose exec api alembic revision -m "description"

# Aplicar migrations
docker-compose exec api alembic upgrade head

# Reverter
docker-compose exec api alembic downgrade -1
```

---

## 🔧 Configuração

Arquivo: `backend/.env.backend`

```bash
# App
PROJECT_NAME=OfertaBR API
VERSION=0.1.0
API_V1_STR=/api/v1

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 dias

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=ofertabr_db

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Email (Brevo/SendinBlue)
BREVO_API_KEY=your-brevo-api-key
EMAIL_FROM=your-email@example.com
EMAIL_FROM_NAME=OfertaBR

# URLs
FRONTEND_URL=http://localhost:3000
API_URL=http://localhost:8000

# n8n Integration
N8N_SERVICE_SECRET=your-secret-for-n8n
N8N_WEBHOOK_NEW_SUBSCRIBER=http://n8n:5678/webhook/subscriber
```

**Nota**: O arquivo `.env.backend` é criado automaticamente pelo `setup.sh`.  
Configure `BREVO_API_KEY` e `EMAIL_FROM` para envio de emails funcionar.

---

## 📊 Arquitetura

```
┌─────────────────────────────────────────┐
│         API (FastAPI)                   │
│  ┌────────────┬──────────┬───────────┐  │
│  │ Auth       │ Scraped  │ News-     │  │
│  │            │ Content  │ letters   │  │
│  └────────────┴──────────┴───────────┘  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Services Layer                   │
│  (Lógica de Negócio + Integrações)      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Repositories Layer                  │
│      (Acesso a Dados)                    │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│    PostgreSQL (Dados) + Redis (Cache)   │
└──────────────────────────────────────────┘
```

---

## 📝 Licença

Este projeto está sob a licença MIT.

---

**Made with ❤️ and Python 🐍**
