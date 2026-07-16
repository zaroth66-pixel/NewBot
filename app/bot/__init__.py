import logging

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

from app.core.config import settings
from app.bot.handlers import (
    start_command,
    admin_command,
    button_handler,
)

logger = logging.getLogger(__name__)

bot_application = None


def create_bot_app():

    global bot_application

    if bot_application:
        return bot_application

    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning(
            "TELEGRAM_BOT_TOKEN is missing"
        )
        return None


    bot_application = (
        Application
        .builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )


    bot_application.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )

    bot_application.add_handler(
        CommandHandler(
            "admin",
            admin_command
        )
    )

    bot_application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )


    return bot_application



async def run_bot():

    bot = create_bot_app()

    if not bot:
        return


    logger.info(
        "Starting Telegram bot polling"
    )


    await bot.initialize()

    await bot.start()

    await bot.updater.start_polling()



async def stop_bot():

    global bot_application

    if bot_application:

        logger.info(
            "Stopping Telegram bot"
        )

        await bot_application.updater.stop()

        await bot_application.stop()

        await bot_application.shutdown()
