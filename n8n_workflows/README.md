# 🤖 Workflows n8n - OfertaBR

Esta pasta contém os workflows do n8n para automação de scraping e envio de newsletters.

## 📋 Workflows Disponíveis

### 1. Cron Scrapping-ML.json
**Execução:** Diariamente às 1h da manhã  
**Função:** Scraping automatizado do Mercado Livre

**Fluxo:**
1. Schedule Trigger (1h)
2. HTTP Request → Jina AI (converte HTML em Markdown)
3. AI Agent (Google Gemini 2.0 Flash) → Extrai produtos
4. Format JSON → Trata JSON truncado e valida
5. Transform to API Schema → Converte para schema da API
6. Fetch Access Token → Obtém JWT token
7. Send Products to API → Envia batch para `/api/v1/scraped_content/batch`

**Recursos:**
- Extrai até 10 produtos por execução
- Tratamento de JSON truncado
- Validação de produtos antes do envio
- Usa Google Gemini API

### 2. Cron - Send email.json
**Execução:** Diariamente às 8h da manhã  
**Função:** Geração e envio de newsletter

**Fluxo:**
1. Schedule Trigger (8h)
2. Fetch Access Token → Obtém JWT token
3. Get All Scraped → Busca produtos do banco
4. Aggregate → Agrupa produtos
5. AI Agent (Google Gemini 2.0 Flash Lite) → Gera título criativo
6. Select Random Title → Escolhe título aleatório
7. Generate Newsletter → Cria newsletter
8. Send Newsletter → Envia para todos os subscribers

**Recursos:**
- Geração automática de título com AI
- Seleção aleatória de título
- Envio em massa para subscribers ativos

---

## ⚠️ CONFIGURAÇÃO IMPORTANTE - SEGURANÇA

### Secret Hardcoded nos Workflows

**PROBLEMA CRÍTICO IDENTIFICADO:**

Os workflows originais contêm o `N8N_SERVICE_SECRET` hardcoded diretamente no JSON:

```json
"jsonBody": "{\n  \"service_name\": \"n8n\",\n  \"secret\": \"8252880558200397\"\n}"
```

**🔴 RISCOS:**
- Secret exposto no versionamento
- Qualquer pessoa com acesso ao repositório pode ver o secret
- Comprometimento da segurança da API

### 🔧 Solução para n8n Community Edition

Como você está usando n8n Community Edition (que não suporta variáveis de ambiente nativamente), existem 3 opções:

#### **Opção 1: Usar Node "Set" (RECOMENDADO)** ✅

Já implementado nos workflows melhorados. Basta:

1. Importar o workflow no n8n
2. Localizar o node "Set Secret" no início do workflow
3. Editar o valor do campo `secret`:

```json
{
  "secret": "SEU_SECRET_AQUI"
}
```

4. Salvar o workflow

**Vantagem:** Secret fica apenas dentro do n8n (não no repositório)

#### **Opção 2: Usar Credentials Customizadas**

1. No n8n, vá em: **Settings → Credentials → New Credential**
2. Escolha tipo: **Header Auth** ou **HTTP Query Auth**
3. Configure:
   - Name: `OfertaBR Service Auth`
   - Value: `seu-secret-aqui`
4. Use essa credential nos nodes HTTP Request

#### **Opção 3: Variáveis de Ambiente (n8n Self-Hosted)**

Se você controla o servidor n8n, adicione no `.env` do n8n:

```bash
N8N_CUSTOM_SECRET=seu-secret-aqui
```

E use no workflow:
```javascript
"secret": "{{ $env.N8N_CUSTOM_SECRET }}"
```

---

## 🚀 Como Importar os Workflows

### 1. Acessar n8n
```
http://localhost:5678
Login: admin
Senha: admin123
```

### 2. Importar Workflow

1. Clique em **"+"** → **Import from File**
2. Selecione o arquivo `.json` do workflow
3. Configure as credenciais:
   - Google Gemini API
   - Secret do OfertaBR (veja seção de segurança acima)
4. Ative o workflow

### 3. Testar Manualmente

Antes de ativar o cron, teste manualmente:
1. Clique em **"Execute Workflow"**
2. Verifique cada node se está funcionando
3. Corrija erros se necessário
4. Ative o workflow quando estiver funcionando

---

## 🔑 Obter Service Token Manualmente

Se precisar gerar um token manualmente para testes:

```bash
curl -X POST http://localhost:8000/api/v1/auth/service-token \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "n8n",
    "secret": "SEU_SECRET_AQUI"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 604800
}
```

Token válido por **7 dias** (604800 segundos).

---

## 📊 Melhorias Aplicadas

### Workflow de Scraping
- ✅ Prompt AI otimizado (reduzido em 50%)
- ✅ Nomes de nodes mais descritivos
- ✅ Comentários/notas adicionados
- ✅ Remoção de pinData de teste
- ⚠️ Secret movido para node "Set" (configurável)

### Workflow de Newsletter
- ✅ Remoção de autenticação duplicada
- ✅ Reutilização do token
- ✅ Prompt AI otimizado
- ✅ Fallback para título padrão
- ✅ Nomes de nodes mais descritivos
- ⚠️ Secret movido para node "Set" (configurável)

---

## 🛠️ Troubleshooting

### Erro: "Invalid or expired access code"
- Verifique se o `N8N_SERVICE_SECRET` está correto
- Confirme que é o mesmo valor do `backend/.env.backend`

### Erro: "Failed to send products to API"
- Verifique se a API está rodando (`http://localhost:8000/health`)
- Confirme que o token está sendo obtido corretamente

### Google Gemini API não funciona
- Verifique se as credenciais do Google Gemini estão configuradas
- Confirme que a API key é válida

### Workflow não executa no horário
- Verifique se o workflow está **ativo** (toggle verde)
- Confirme o timezone do servidor n8n
- Verifique logs: **Settings → Logs**

---

## 📝 Próximos Passos Recomendados

1. **Rotacionar o Secret:** Gere um novo secret e atualize em:
   - `backend/.env.backend`
   - Node "Set Secret" nos workflows n8n

2. **Implementar Rate Limiting:** Adicionar controle de frequência para não sobrecarregar APIs

3. **Adicionar Notificações:** Configurar webhooks para alertas de falha

4. **Monitoramento:** Implementar logs estruturados e métricas

5. **Backup dos Workflows:** Exportar workflows regularmente

---

## 🔒 Checklist de Segurança

- [ ] Secret removido do JSON e movido para node "Set"
- [ ] Novo secret gerado com `openssl rand -hex 16`
- [ ] Secret atualizado no `backend/.env.backend`
- [ ] Secret atualizado no node "Set" do n8n
- [ ] Workflows testados com novo secret
- [ ] Secret antigo revogado/removido

---

**Última atualização:** 2025-01-29
**Versão:** 1.0.0

