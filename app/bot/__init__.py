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


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


bot_application = None


def create_bot_app():

    global bot_application

    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning(
            "TELEGRAM_BOT_TOKEN is not set. Bot will not start."
        )
        return None


    bot_application = (
        Application
        .builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )


    # Commands
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


    # Inline buttons
    bot_application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )


    return bot_application



async def start_bot():

    app = create_bot_app()

    if not app:
        return


    logger.info(
        "Starting Telegram Bot"
    )


    await app.initialize()

    await app.start()

    await app.updater.start_polling(
        drop_pending_updates=True
    )


    logger.info(
        "Telegram Bot started successfully"
    )



async def stop_bot():

    global bot_application


    if bot_application:

        logger.info(
            "Stopping Telegram Bot"
        )


        await bot_application.updater.stop()

        await bot_application.stop()

        await bot_application.shutdown()


        logger.info(
            "Telegram Bot stopped"
        )
