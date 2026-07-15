from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.scheduler import start_scheduler

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

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for AI-Powered Forex Signal Telegram Bot",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Forex Bot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Webhook endpoint for Telegram (if not using polling)
@app.post("/webhook")
async def telegram_webhook(data: dict):
    logger.info(f"Received webhook data: {data}")
    # Integration with telegram-python-bot webhook handler goes here
    return {"status": "ok"}