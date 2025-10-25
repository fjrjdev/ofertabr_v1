from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import subscribers, newsletters

# Import models to register them with SQLAlchemy
from app.models import Subscriber, NewsletterEdition, ScrapedContent, ScrapedImage

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