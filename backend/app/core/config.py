import logging
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Configura logging
logger = logging.getLogger(__name__)

# Define o diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

# Log apenas se arquivo .env não existir
if not ENV_FILE.exists():
    logger.warning(f"Arquivo .env não encontrado em: {ENV_FILE}")


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = Field(..., validation_alias='PROJECT_NAME')
    VERSION: str = Field(..., validation_alias='VERSION')
    API_V1_STR: str = Field(..., validation_alias='API_V1_STR')

    # Security
    SECRET_KEY: str = Field(..., validation_alias='SECRET_KEY')
    ALGORITHM: str = Field(default='HS256', validation_alias='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, validation_alias='ACCESS_TOKEN_EXPIRE_MINUTES')

    # Database
    POSTGRES_USER: str = Field(..., validation_alias='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., validation_alias='POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = Field(..., validation_alias='POSTGRES_SERVER')
    POSTGRES_PORT: int = Field(default=5432, validation_alias='POSTGRES_PORT')
    POSTGRES_DB: str = Field(..., validation_alias='POSTGRES_DB')

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Redis
    REDIS_HOST: str = Field(..., validation_alias='REDIS_HOST')
    REDIS_PORT: int = Field(default=6379, validation_alias='REDIS_PORT')

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = Field(..., validation_alias='BACKEND_CORS_ORIGINS')

    # Email Configuration (Brevo)
    BREVO_API_KEY: str = Field(..., validation_alias='BREVO_API_KEY')
    EMAIL_FROM: str = Field(..., validation_alias='EMAIL_FROM')
    EMAIL_FROM_NAME: str = Field(..., validation_alias='EMAIL_FROM_NAME')
    FRONTEND_URL: str = Field(..., validation_alias='FRONTEND_URL')

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
