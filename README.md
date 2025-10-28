# 🎯 OfertaBR v1

**Sistema de Newsletter automatizada com Web Scraping, AI e Autenticação Passwordless**

API FastAPI moderna para captura automatizada de ofertas/produtos através de web scraping com n8n + AI, gerenciamento de newsletters e envio automático para subscribers.

> 📦 **Estrutura Monorepo**: O projeto está organizado com `/backend` e `/frontend` (em breve) separados. Todo o código do backend está em `backend/`.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura e Camadas](#-arquitetura-e-camadas)
- [Tecnologias](#-tecnologias)
- [Funcionalidades](#-funcionalidades)
- [Instalação e Setup](#-instalação-e-setup)
- [Autenticação Passwordless](#-autenticação-passwordless)
- [API Endpoints](#-api-endpoints)
- [Integração com n8n](#-integração-com-n8n)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Banco de Dados](#-banco-de-dados)
- [Cache e Performance](#-cache-e-performance)
- [Scripts Úteis](#-scripts-úteis)

---

## 🚀 Sobre o Projeto

OfertaBR é uma plataforma automatizada de curadoria de ofertas que:

1. **Captura produtos/ofertas** de sites através de web scraping automatizado (n8n + AI)
2. **Armazena e gerencia** o conteúdo capturado em banco de dados PostgreSQL
3. **Cria newsletters** com os produtos selecionados
4. **Envia emails** automaticamente para lista de subscribers via Brevo (SendinBlue)
5. **Gerencia subscribers** com controle de inscrições e cancelamentos

### Diferencial Principal

- ✨ **Autenticação Passwordless**: Sistema moderno sem senhas, usando códigos temporários ou magic links
- 🤖 **Integração com AI**: n8n + OpenAI para extração inteligente de dados
- ⚡ **Cache Redis**: Performance otimizada para consultas frequentes
- 🎨 **Templates HTML**: Emails responsivos e modernos com Jinja2
- 📦 **Batch Processing**: Envio de múltiplos produtos em uma única requisição

---

## 🏗️ Arquitetura e Camadas

O projeto segue uma arquitetura em camadas bem definida (Clean Architecture):

```
┌─────────────────────────────────────────────────────────┐
│                     PRESENTATION                         │
│              (FastAPI Routes - API v1)                   │
│  ┌──────────┬──────────┬──────────┬──────────────────┐  │
│  │   Auth   │ Scraped  │  News-   │   Subscribers   │  │
│  │          │ Content  │  letters │                  │  │
│  └──────────┴──────────┴──────────┴──────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   BUSINESS LOGIC                         │
│                    (Services Layer)                      │
│  ┌──────────┬──────────┬──────────┬──────────────────┐  │
│  │   Auth   │ Scraped  │  News-   │   Subscribers   │  │
│  │ Service  │ Content  │  letter  │    Service      │  │
│  │          │ Service  │  Service │                  │  │
│  └──────────┴──────────┴──────────┴──────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  DATA ACCESS                             │
│                (Repositories Layer)                      │
│  ┌──────────────┬─────────────┬────────────────────┐   │
│  │   Scraped    │  Newsletter │   Subscriber       │   │
│  │  Repository  │  Repository │   Repository       │   │
│  └──────────────┴─────────────┴────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    DATABASE                              │
│         ┌──────────────┬──────────────────┐             │
│         │  PostgreSQL  │      Redis       │             │
│         │   (Dados)    │     (Cache)      │             │
│         └──────────────┴──────────────────┘             │
└──────────────────────────────────────────────────────────┘
```

### Descrição das Camadas

#### 1️⃣ **Presentation Layer** (`app/api/v1/`)

- Endpoints REST da API
- Validação de requests (Pydantic schemas)
- Documentação automática (Swagger/OpenAPI)
- Autenticação e autorização (JWT)

#### 2️⃣ **Business Logic Layer** (`app/services/`)

- Regras de negócio da aplicação
- Orquestração entre repositories
- Integração com serviços externos (Email, Redis)
- Processamento de lógica complexa

#### 3️⃣ **Data Access Layer** (`app/repositories/`)

- Operações CRUD no banco de dados
- Queries otimizadas com SQLAlchemy
- Abstração do acesso aos dados
- Padrão Repository

#### 4️⃣ **Database Layer**

- **PostgreSQL**: Persistência de dados principais
- **Redis**: Cache de alto desempenho

### Fluxo de uma Requisição

```
1. Cliente HTTP → 2. FastAPI Route → 3. Service → 4. Repository → 5. Database
                                     ↓
                              6. External APIs
                              (Brevo, n8n)
```

---

## 🛠️ Tecnologias

### Backend

- **FastAPI** - Framework web moderno e rápido
- **Python 3.12** - Linguagem principal
- **SQLAlchemy 2.0** - ORM async para PostgreSQL
- **Pydantic v2** - Validação de dados e schemas
- **Alembic** - Migrations de banco de dados

### Banco de Dados

- **PostgreSQL 16** - Banco relacional principal
- **Redis 7** - Cache e armazenamento de sessões

### Autenticação

- **JWT (JSON Web Tokens)** - Tokens stateless (autenticação passwordless)
- **Python-Jose** - Criação/validação de JWTs

### Email & Templates

- **Brevo (SendinBlue)** - Envio transacional de emails
- **Jinja2** - Template engine para HTML

### Automação

- **n8n** - Orquestração de workflows e web scraping
- **OpenAI API** - Extração inteligente de dados

### DevOps

- **Docker & Docker Compose** - Containerização
- **Poetry** - Gerenciamento de dependências Python
- **Uvicorn** - ASGI server

---

## ✨ Funcionalidades

### 🔐 Autenticação Passwordless

- Autenticação via código de 6 dígitos (email)
- Magic links (acesso com um clique)
- JWT tokens com validade de 7 dias
- Gerenciamento de emails permitidos via Redis

### 📰 Scraped Content (Produtos)

- Captura de produtos via n8n + AI
- Batch processing (até 100 produtos por request)
- Campos estruturados: nome, preço, desconto, imagens, etc.
- Cache Redis para consultas rápidas
- Controle de processamento (is_processed)

### 📧 Newsletters

- Criação de edições de newsletter
- Template HTML responsivo
- Envio em lote para subscribers
- Tracking de envios (total_sent)
- Preview antes do envio

### 👥 Subscribers

- Inscrição pública (sem auth)
- Cancelamento via endpoint
- Gerenciamento de status (active/inactive)
- Controle de datas (subscribed_at, unsubscribed_at)

### ⚡ Cache Inteligente

- Cache automático de consultas frequentes
- Invalidação automática em updates
- TTL configurável por endpoint
- Fallback gracioso se Redis offline

---

## 📦 Instalação e Setup

### Pré-requisitos

- Docker & Docker Compose
- Git

### 1. Clone o repositório

```bash
git clone <repository-url>
cd ofertabr_v1
```

### 2. Configure as variáveis de ambiente

```bash
# O arquivo backend/.env.backend será criado automaticamente pelo setup.sh
# Você pode editá-lo depois para configurar BREVO_API_KEY e EMAIL_FROM
```

### 3. Inicie o projeto com setup automático

```bash
bash setup.sh
```

**O script `setup.sh` faz:**

- ✅ Cria arquivo `backend/.env.backend` se não existir
- ✅ Inicia containers Docker (PostgreSQL, Redis, API, n8n)
- ✅ Aguarda PostgreSQL ficar pronto
- ✅ Executa migrations do banco

### 4. Acesse a aplicação

- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Alternativa (ReDoc)**: http://localhost:8000/redoc
- **n8n Interface**: http://localhost:5678 (admin/admin123)
- **Health Check**: http://localhost:8000/health

---

## 🔐 Autenticação Passwordless

### Como Funciona

O sistema **NÃO usa senhas**. A autenticação funciona com emails permitidos e códigos temporários.

```
┌──────────┐     1. Request Code      ┌──────────┐
│          │ ─────────────────────────▶│          │
│  Client  │                           │   API    │
│          │ ◀─────────────────────────│          │
└──────────┘   2. Email with code     └──────────┘
                                            │
     │                                      │ 3. Store in Redis
     │                                      ▼
     │                              ┌──────────────┐
     │                              │    Redis     │
     │                              │ Key: "auth:  │
     │                              │ code:{email}"│
     │                              │ TTL: 900s    │
     │                              └──────────────┘
     │
     │         4. Verify Code           │
     └──────────────────────────────────▶
                                         │
               5. JWT Token              │
     ◀──────────────────────────────────┘
```

### Armazenamento

| Componente            | Onde    | TTL        | Formato            |
| --------------------- | ------- | ---------- | ------------------ |
| **Emails Permitidos** | Redis   | Permanente | Lista JSON         |
| **Código de Acesso**  | Redis   | 15 minutos | String (6 dígitos) |
| **Magic Link Token**  | Redis   | 15 minutos | String (32 bytes)  |
| **JWT Token**         | Cliente | 7 dias     | JWT assinado       |

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
# 1. Solicitar magic link
curl -X POST http://localhost:8000/api/v1/auth/request-magic-link \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@ofertabr.com"}'

# 2. Clicar no link recebido por email (acesso automático)
```

### Usar Token nas Requisições

```bash
# Com Bearer token
curl -X GET http://localhost:8000/api/v1/newsletters \
  -H "Authorization: Bearer eyJ..."
```

---

## 📡 API Endpoints

### 🔓 Públicos (Sem Autenticação)

| Método | Endpoint                          | Descrição                      |
| ------ | --------------------------------- | ------------------------------ |
| `POST` | `/api/v1/auth/request-code`       | Solicitar código de acesso     |
| `POST` | `/api/v1/auth/verify-code`        | Verificar código e obter token |
| `POST` | `/api/v1/auth/request-magic-link` | Solicitar magic link           |
| `GET`  | `/api/v1/auth/verify-magic`       | Verificar magic link           |
| `POST` | `/api/v1/subscribers/`            | Inscrever email na newsletter  |
| `GET`  | `/health`                         | Status da API                  |

### 🔒 Protegidos (Requerem Autenticação)

#### Scraped Content

| Método   | Endpoint                              | Descrição                      |
| -------- | ------------------------------------- | ------------------------------ |
| `POST`   | `/api/v1/scraped_content/batch`       | Criar múltiplos produtos (n8n) |
| `GET`    | `/api/v1/scraped_content/`            | Listar todos produtos          |
| `GET`    | `/api/v1/scraped_content/unprocessed` | Listar não processados         |
| `GET`    | `/api/v1/scraped_content/{id}`        | Buscar produto por ID          |
| `PATCH`  | `/api/v1/scraped_content/{id}`        | Atualizar produto              |
| `DELETE` | `/api/v1/scraped_content/{id}`        | Deletar produto                |

#### Newsletters

| Método   | Endpoint                        | Descrição            |
| -------- | ------------------------------- | -------------------- |
| `POST`   | `/api/v1/newsletters/`          | Criar newsletter     |
| `GET`    | `/api/v1/newsletters/`          | Listar newsletters   |
| `GET`    | `/api/v1/newsletters/{id}`      | Buscar newsletter    |
| `PATCH`  | `/api/v1/newsletters/{id}`      | Atualizar newsletter |
| `DELETE` | `/api/v1/newsletters/{id}`      | Deletar newsletter   |
| `POST`   | `/api/v1/newsletters/{id}/send` | Enviar newsletter    |

#### Subscribers

| Método  | Endpoint                               | Descrição            |
| ------- | -------------------------------------- | -------------------- |
| `GET`   | `/api/v1/subscribers/`                 | Listar subscribers   |
| `GET`   | `/api/v1/subscribers/by-id/{id}`       | Buscar por ID        |
| `GET`   | `/api/v1/subscribers/by-email/{email}` | Buscar por email     |
| `PATCH` | `/api/v1/subscribers/{id}`             | Atualizar subscriber |
| `POST`  | `/api/v1/subscribers/{id}/unsubscribe` | Cancelar inscrição   |

#### Auth Admin

| Método | Endpoint                          | Descrição                 |
| ------ | --------------------------------- | ------------------------- |
| `POST` | `/api/v1/auth/admin/add-email`    | Adicionar email permitido |
| `POST` | `/api/v1/auth/admin/remove-email` | Remover email permitido   |
| `GET`  | `/api/v1/auth/admin/list-emails`  | Listar emails permitidos  |

---

## 🔗 Integração com n8n

O n8n é usado para automatizar a captura de produtos através de web scraping + AI.

### Workflow

```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│ Trigger │───▶│  Scraper │───▶│ OpenAI  │───▶│ OfertaBR │
│ (Cron)  │    │  (HTTP)  │    │   API   │    │   API    │
└─────────┘    └──────────┘    └─────────┘    └──────────┘
```

### Setup do n8n

1. Acesse: http://localhost:5678
2. Login: `admin` / `admin123`
3. Importe o workflow (arquivo em `n8n_workflows/`)

### Configuração do Workflow

**1. Trigger (Schedule)**

- Executar a cada X horas/dias
- Exemplo: Diariamente às 9h

**2. HTTP Request (Scraping)**

- URL do site alvo
- Extração de HTML/JSON

**3. OpenAI Node**

- Modelo: GPT-4 ou GPT-3.5-turbo
- Prompt: Extrair dados estruturados
- Output: JSON com produtos

**4. HTTP Request (OfertaBR API)**

- Endpoint: `POST /api/v1/scraped_content/batch`
- Headers: `Authorization: Bearer {token}`
- Body: Array de produtos

### Exemplo de Payload

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

### Screenshots do n8n

> **📸 Adicione aqui prints do seu workflow n8n:**

<!-- SEÇÃO PARA PRINTS DO N8N -->

#### 1. Visão Geral do Workflow

_[Adicionar print do workflow completo]_

#### 2. Configuração do Trigger

_[Adicionar print da configuração do trigger/schedule]_

#### 3. Node de Scraping

_[Adicionar print do HTTP Request node configurado]_

#### 4. Node OpenAI

_[Adicionar print da configuração do OpenAI com prompt]_

#### 5. Node de Envio para API

_[Adicionar print do POST para /batch endpoint]_

#### 6. Execução Bem-Sucedida

_[Adicionar print de uma execução com sucesso]_

<!-- FIM DA SEÇÃO DE PRINTS -->

---

## 📁 Estrutura do Projeto

> ⚠️ **Estrutura Monorepo**: O projeto está organizado com backend e frontend separados.

```
ofertabr_v1/                      # Raiz do monorepo
├── backend/                      # 🐍 Backend FastAPI
│   ├── alembic/                  # Migrations do banco
│   │   ├── versions/             # Arquivos de migration
│   │   └── env.py                # Configuração Alembic
│   │
│   ├── app/
│   │   ├── api/                  # Camada de Apresentação
│   │   │   └── v1/               # API v1
│   │   │       ├── auth.py       # Endpoints de autenticação
│   │   │       ├── scraped_content.py
│   │   │       ├── newsletters.py
│   │   │       └── subscribers.py
│   │   │
│   │   ├── core/                 # Configurações centrais
│   │   │   ├── config.py         # Settings (Pydantic)
│   │   │   ├── database.py       # Setup SQLAlchemy
│   │   │   ├── redis.py          # Cliente Redis
│   │   │   ├── security.py       # JWT, Hashing
│   │   │   └── dependencies.py   # Dependências FastAPI
│   │   │
│   │   ├── models/               # Modelos SQLAlchemy
│   │   │   ├── base.py           # TimestampMixin
│   │   │   ├── scraped_content.py
│   │   │   ├── newsletter.py
│   │   │   └── subscriber.py
│   │   │
│   │   ├── repositories/         # Camada de Acesso a Dados
│   │   │   ├── scraped_content.py
│   │   │   ├── newsletters.py
│   │   │   └── subscribers.py
│   │   │
│   │   ├── schemas/              # Pydantic Schemas
│   │   │   ├── auth.py
│   │   │   ├── scraped_content.py
│   │   │   ├── newsletter.py
│   │   │   └── subscribers.py
│   │   │
│   │   ├── services/             # Camada de Lógica de Negócio
│   │   │   ├── auth_service.py
│   │   │   ├── scraped_content.py
│   │   │   ├── newsletters.py
│   │   │   ├── subscribers.py
│   │   │   ├── email_service.py
│   │   │   └── newsletter_builder.py
│   │   │
│   │   ├── templates/            # Templates HTML
│   │   │   └── emails/
│   │   │       ├── access_code.html
│   │   │       ├── magic_link.html
│   │   │       ├── welcome.html
│   │   │       └── newsletter.html
│   │   │
│   │   └── main.py               # Aplicação FastAPI
│   │
│   ├── tests/                    # Testes (mock data)
│   │   ├── batch_scraped_content_example.json
│   │   ├── mock_newsletter_edition.json
│   │   └── mock_scraped_content.json
│   │
│   ├── Dockerfile                # Imagem Docker do backend
│   ├── pyproject.toml            # Dependências Poetry
│   ├── alembic.ini               # Config Alembic
│   └── .env.backend              # Variáveis de ambiente do backend
│
├── frontend/                     # ⚛️ Frontend Next.js (em breve)
│   └── (próxima etapa)
│
├── n8n_workflows/                # Workflows n8n
│
├── docker-compose.yml            # Orquestração de containers
├── .env                          # Variáveis compartilhadas (raiz)
│
├── setup.sh                      # Script de setup inicial
├── reset_db.sh                   # Reset banco (dev)
├── reset_migrations.sh           # Reset migrations (dev)
│
└── README.md                     # Este arquivo
```

---

## 🗄️ Banco de Dados

### Modelos e Relacionamentos

```
┌─────────────────────┐
│   scraped_content   │
│─────────────────────│
│ • id (UUID)         │
│ • title             │
│ • content           │◀────────┐
│ • source_url        │         │
│ • product_name      │         │
│ • current_price     │         │
│ • old_price         │         │ (FK)
│ • discount_%        │         │
│ • is_processed      │         │
│ • images []         │         │
└─────────────────────┘         │
                                │
┌─────────────────────┐         │
│ newsletter_editions │         │
│─────────────────────│         │
│ • id (UUID)         │         │
│ • title             │         │
│ • content (HTML)    │         │
│ • sent_at           │         │
│ • total_sent        │         │
│ • scraped_id  ──────┘
└─────────────────────┘


┌─────────────────────┐
│    subscribers      │
│─────────────────────│
│ • id (UUID)         │
│ • email (unique)    │
│ • name              │
│ • is_active         │
│ • subscribed_at     │
│ • unsubscribed_at   │
└─────────────────────┘


┌─────────────────────┐
│   scraped_images    │
│─────────────────────│
│ • id (UUID)         │
│ • content_id (FK)   │
│ • image_url         │
│ • alt_text          │
│ • is_featured       │
│ • display_order     │
└─────────────────────┘
```

### Migrations

```bash
# Criar nova migration
docker-compose exec api alembic revision -m "description"

# Aplicar migrations
docker-compose exec api alembic upgrade head

# Reverter última migration
docker-compose exec api alembic downgrade -1

# Ver histórico
docker-compose exec api alembic history
```

---

## ⚡ Cache e Performance

### Estratégia de Cache (Redis)

```python
# Padrão de nomenclatura de chaves
"scraped_content:all"              # TTL: 300s (5min)
"scraped_content:unprocessed:*"    # TTL: 300s
"subscribers:all"                  # TTL: 600s (10min)
"newsletters:*"                    # TTL: 300s
"auth:allowed_emails"              # TTL: ∞ (permanente)
"auth:code:{email}"                # TTL: 900s (15min)
"auth:magic:{token}"               # TTL: 900s
```

### Invalidação Automática

O cache é invalidado automaticamente quando:

- Criar novo scraped content
- Atualizar scraped content
- Criar novo subscriber
- Atualizar subscriber
- Criar/atualizar newsletter

### Performance

- **Sem Cache**: ~200-500ms (consulta ao PostgreSQL)
- **Com Cache**: ~10-50ms (leitura do Redis)
- **Melhoria**: 80-90% mais rápido

---

## 🛠️ Scripts Úteis

### Setup Inicial

```bash
bash setup.sh
```

Cria `.env`, inicia containers e executa migrations.

### Reset do Banco de Dados

```bash
bash reset_db.sh
```

Remove volume do PostgreSQL, recria banco e executa migrations.

### Reset Total (Migrations)

```bash
bash reset_migrations.sh
```

Remove migrations antigas, cria nova migration automática e recria banco.

### Comandos Docker Úteis

```bash
# Ver logs da API
docker-compose logs -f api

# Ver logs do n8n
docker-compose logs -f n8n

# Acessar shell da API
docker-compose exec api bash

# Reiniciar serviços
docker-compose restart

# Parar tudo
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

---

## 🔧 Configuração (backend/.env.backend)

> ⚠️ O arquivo de configuração do backend agora está em `backend/.env.backend`

```bash
# App
PROJECT_NAME=OfertaBR API
VERSION=0.1.0
API_V1_STR=/api/v1

# Security
SECRET_KEY=seu-secret-key-aqui-gere-com-openssl
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
BREVO_API_KEY=sua-api-key-aqui
EMAIL_FROM=seu-email@exemplo.com
EMAIL_FROM_NAME=OfertaBR
FRONTEND_URL=http://localhost:3000
```

---

## 📝 Desenvolvimento

### Adicionar Nova Funcionalidade

1. **Criar Model** em `app/models/`
2. **Criar Schema** em `app/schemas/`
3. **Criar Repository** em `app/repositories/`
4. **Criar Service** em `app/services/`
5. **Criar Endpoints** em `app/api/v1/`
6. **Criar Migration**: `alembic revision -m "description"`
7. **Aplicar Migration**: `alembic upgrade head`

### Code Style

O projeto usa **Ruff** para linting:

```bash
# Verificar código
docker-compose exec api ruff check .

# Corrigir automaticamente
docker-compose exec api ruff check --fix .
```

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Made with ❤️ and Python 🐍**
