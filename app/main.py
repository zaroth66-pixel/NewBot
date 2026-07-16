from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.webhooks import router as webhooks_router
from app.scheduler import start_scheduler, stop_scheduler

from app.bot import create_bot_app

import asyncio
import logging

logger = logging.getLogger(__name__)

telegram_bot = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global telegram_bot

    # Startup
    logger.info("Starting up FastAPI application")

    # Start scheduler
    start_scheduler()

    # Start Telegram bot
    telegram_bot = create_bot_app()

    if telegram_bot:
        try:
            await telegram_bot.initialize()
            await telegram_bot.start()

            asyncio.create_task(
                telegram_bot.updater.start_polling()
            )

            logger.info("Telegram bot started")

        except Exception as e:
            logger.error(f"Telegram bot startup failed: {e}")

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application")

    if telegram_bot:
        try:
            await telegram_bot.updater.stop()
            await telegram_bot.stop()
            await telegram_bot.shutdown()

            logger.info("Telegram bot stopped")

        except Exception as e:
            logger.error(f"Telegram bot shutdown error: {e}")

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


@app.post("/webhook")
async def telegram_webhook(data: dict):
    logger.info(f"Received webhook data: {data}")

    return {
        "status": "ok"
    }
