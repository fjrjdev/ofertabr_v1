import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import subscribers, newsletters, scraped_content
# AUTHENTICATION TEMPORARILY DISABLED
# from app.api.v1 import auth

# Import models to register them with SQLAlchemy
from app.models import Subscriber, NewsletterEdition, ScrapedContent, ScrapedImage
# AUTHENTICATION TEMPORARILY DISABLED
# from app.models import Admin

# Configurar logging
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
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# AUTHENTICATION TEMPORARILY DISABLED
# app.include_router(
#     auth.router,
#     prefix=f"{settings.API_V1_STR}/auth",
#     tags=["authentication"]
# )

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
    prefix=f"{settings.API_V1_STR}/scraped-content",
    tags=["scraped-content"]
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