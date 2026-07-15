import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI-Powered Forex Signal Telegram Bot"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = ""
    WEBHOOK_URL: str = ""

    # AI Providers
    GROQ_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Market Data Providers
    TWELVEDATA_API_KEY: str = ""
    FINNHUB_API_KEY: str = ""
    POLYGON_API_KEY: str = ""
    ALPHAVANTAGE_API_KEY: str = ""
    FOREXRATE_API_KEY: str = ""
    DEFAULT_DATA_PROVIDER: str = "twelvedata"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/forex_bot"

    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()