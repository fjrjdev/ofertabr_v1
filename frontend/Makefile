# Makefile para facilitar comandos do frontend

.PHONY: help setup install dev build start docker-dev docker-prod docker-build clean

# Cores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RESET := \033[0m

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)Frontend OfertaBR - Comandos Disponíveis$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

setup: ## Setup inicial do projeto (cria Next.js + instala deps)
	@echo "$(YELLOW)Executando setup inicial...$(RESET)"
	@chmod +x setup-frontend.sh
	@./setup-frontend.sh

install: ## Instala dependências do npm
	@echo "$(YELLOW)Instalando dependências...$(RESET)"
	npm install

dev: ## Roda em modo desenvolvimento local (sem Docker)
	@echo "$(YELLOW)Iniciando modo desenvolvimento...$(RESET)"
	npm run dev

build: ## Build de produção
	@echo "$(YELLOW)Criando build de produção...$(RESET)"
	npm run build

start: ## Inicia servidor de produção (após build)
	@echo "$(YELLOW)Iniciando servidor de produção...$(RESET)"
	npm start

lint: ## Executa linter
	@echo "$(YELLOW)Executando linter...$(RESET)"
	npm run lint

docker-dev: ## Roda com Docker em modo desenvolvimento
	@echo "$(YELLOW)Iniciando Docker (modo dev com hot-reload)...$(RESET)"
	docker-compose -f docker-compose.frontend.yml --profile dev up frontend-dev

docker-prod: ## Roda com Docker em modo produção
	@echo "$(YELLOW)Iniciando Docker (modo produção)...$(RESET)"
	docker-compose -f docker-compose.frontend.yml up frontend

docker-build: ## Build da imagem Docker
	@echo "$(YELLOW)Building imagem Docker...$(RESET)"
	docker-compose -f docker-compose.frontend.yml build

docker-stop: ## Para containers Docker
	@echo "$(YELLOW)Parando containers...$(RESET)"
	docker-compose -f docker-compose.frontend.yml down

docker-logs: ## Mostra logs do Docker
	@echo "$(YELLOW)Mostrando logs...$(RESET)"
	docker-compose -f docker-compose.frontend.yml logs -f

docker-rebuild: ## Rebuild e restart dos containers
	@echo "$(YELLOW)Rebuilding containers...$(RESET)"
	docker-compose -f docker-compose.frontend.yml up -d --build

clean: ## Remove node_modules, .next e cache
	@echo "$(YELLOW)Limpando arquivos...$(RESET)"
	rm -rf node_modules .next out dist .turbo

clean-docker: ## Remove containers, imagens e volumes
	@echo "$(YELLOW)Limpando Docker...$(RESET)"
	docker-compose -f docker-compose.frontend.yml down -v --rmi all

.DEFAULT_GOAL := help

