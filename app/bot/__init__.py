import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler
)

from app.core.config import settings
from app.bot.handlers import (
    start_command,
    admin_command,
    button_handler
)


logger = logging.getLogger(__name__)


def create_bot_app():

    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning(
            "TELEGRAM_BOT_TOKEN is missing"
        )
        return None


    application = (
        Application
        .builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )


    application.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )


    application.add_handler(
        CommandHandler(
            "admin",
            admin_command
        )
    )


    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )


    return application



async def run_bot():

    application = create_bot_app()

    if application:

        logger.info(
            "Starting Telegram Bot"
        )


        await application.initialize()

        await application.start()

        await application.updater.start_polling()


        logger.info(
            "Telegram Bot started"
        )
