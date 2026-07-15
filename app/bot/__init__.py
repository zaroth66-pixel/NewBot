import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from app.core.config import settings
from app.bot.handlers import start_command, admin_command, button_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_bot_app():
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN is not set. Bot will not start.")
        return None
        
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    return application

def run_bot():
    app = create_bot_app()
    if app:
        logger.info("Starting Telegram Bot (Polling mode)")
        app.run_polling()
        
if __name__ == "__main__":
    run_bot()