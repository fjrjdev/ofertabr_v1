import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, newsletters, scraped_content, subscribers
from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
## 🔐 Autenticação Passwordless

Para acessar endpoints protegidos:

1. **Solicite um código:** `POST /api/v1/auth/request-code`
2. **Verifique o código no email:** Copie o código de 6 dígitos
3. **Obtenha o token:** `POST /api/v1/auth/verify-code`
4. **Autorize no Swagger:** Clique no botão 🔓 **Authorize** (canto superior direito)
5. **Cole o token** (apenas o valor de `access_token`, sem "Bearer")
6. **Teste os endpoints protegidos!** 🎉

### Endpoints Públicos
- Inscrição de newsletter
- Cancelamento de inscrição
- Autenticação (request/verify)

### Endpoints Protegidos 🔒
- Newsletters (criar, listar, enviar)
- Scraped Content (gerenciar produtos)
- Subscribers (admin)
- Auth Admin (gerenciar emails)

📚 **Documentação completa:** `SWAGGER_AUTENTICACAO.md`
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "filter": True,
        "tryItOutEnabled": True,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["authentication"]
)

app.include_router(
    subscribers.router,
    prefix=f"{settings.API_V1_STR}/subscribers",
    tags=["subscribers"]
)


app.include_router(
    newsletters.router,
    prefix=f"{settings.API_V1_STR}/newsletters",
    tags=["newsletters"]
)

app.include_router(
    scraped_content.router,
    prefix=f"{settings.API_V1_STR}/scraped_content",
    tags=["scraped_content"]
)


@app.on_event("startup")
async def startup_event():
    logger.info(f"OfertaBR API v{settings.VERSION} iniciada")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Aplicação encerrada")


@app.get("/")
async def root():
    return {
        "message": "OfertaBR API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
