from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import get_db
from app.api.webhooks import router as webhooks_router
from app.scheduler import start_scheduler, stop_scheduler

import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI application")

    start_scheduler()

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application")

    stop_scheduler()


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for AI-Powered Forex Signal Telegram Bot",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(
    webhooks_router,
    prefix="/api/webhooks",
    tags=["webhooks"]
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Forex Bot API"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


# Telegram webhook endpoint
@app.post("/webhook")
async def telegram_webhook(data: dict):
    logger.info(f"Received webhook data: {data}")

    # Telegram bot webhook handler integration goes here

    return {
        "status": "ok"
    }
