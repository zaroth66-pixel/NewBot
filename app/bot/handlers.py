from telegram import Update
from telegram.ext import ContextTypes
import logging

from app.bot.keyboards import (
    get_main_menu_keyboard,
    get_admin_keyboard,
    get_premium_plans_keyboard,
    get_payment_methods_keyboard
)

from app.services.payment import payment_service


logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_message = (
        "🤖 Welcome to Selina AI Trading Bot!\n\n"
        "📈 AI-powered forex signals\n"
        "🧠 Market analysis\n"
        "📊 Trading insights\n\n"
        "Select an option below:"
    )

    keyboard = get_main_menu_keyboard()

    if update.message:
        await update.message.reply_text(
            welcome_message,
            reply_markup=keyboard
        )

    elif update.callback_query:
        await update.callback_query.edit_message_text(
            welcome_message,
            reply_markup=keyboard
        )


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = (
        "🛠️ Admin Dashboard\n\n"
        "Select management option:"
    )

    keyboard = get_admin_keyboard()

    await update.message.reply_text(
        message,
        reply_markup=keyboard
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data


    if data == "main_menu":

        await start_command(update, context)


    elif data == "live_signals":

        await query.edit_message_text(
            "📈 Live Signals\n\n"
            "Fetching latest trading signals..."
        )


    elif data == "ai_analysis":

        await query.edit_message_text(
            "🧠 AI Analysis\n\n"
            "Select currency pair:\n\n"
            "EUR/USD\n"
            "GBP/USD\n"
            "USD/JPY"
        )


    elif data == "market_scanner":

        await query.edit_message_text(
            "🔍 Market Scanner\n\n"
            "Scanning forex markets..."
        )


    elif data == "forex_news":

        await query.edit_message_text(
            "📰 Forex News\n\n"
            "Fetching latest market news..."
        )


    elif data == "trading_sessions":

        await query.edit_message_text(
            "🕒 Trading Sessions\n\n"
            "🌏 Asian Session\n"
            "🇬🇧 London Session\n"
            "🇺🇸 New York Session"
        )


    elif data == "economic_calendar":

        await query.edit_message_text(
            "📅 Economic Calendar\n\n"
            "Loading economic events..."
        )


    elif data == "portfolio":

        await query.edit_message_text(
            "💼 Portfolio\n\n"
            "No trades available yet."
        )


    elif data == "signal_history":

        await query.edit_message_text(
            "📜 Signal History\n\n"
            "No previous signals."
        )


    elif data == "favorites":

        await query.edit_message_text(
            "⭐ Favorites\n\n"
            "No favorite pairs saved."
        )


    elif data == "profile":

        user = update.effective_user

        await query.edit_message_text(
            "👤 Profile\n\n"
            f"Name: {user.first_name}\n"
            f"Username: @{user.username}\n"
            f"ID: {user.id}"
        )


    elif data == "settings":

        await query.edit_message_text(
            "⚙️ Settings\n\n"
            "Notification settings coming soon."
        )


    elif data == "support":

        await query.edit_message_text(
            "❓ Support\n\n"
            "Contact: @your_support"
        )


    elif data == "premium":

        await query.edit_message_text(
            "💎 Premium Plans\n\n"
            "Choose your subscription:",
            reply_markup=get_premium_plans_keyboard()
        )


    elif data.startswith("buy_"):

        plan = data.split("_")[1]

        user_id = update.effective_user.id

        payment_url = payment_service.create_stripe_checkout_session(
            user_id=user_id,
            plan=plan
        )


        if payment_url:

            await query.edit_message_text(
                f"💎 Selected Plan: {plan}\n\n"
                "Complete payment:",
                reply_markup=get_payment_methods_keyboard(
                    plan,
                    payment_url
                )
            )

        else:

            await query.edit_message_text(
                "❌ Payment service unavailable."
            )


    elif data == "back":

        await start_command(update, context)


    else:

        logger.warning(
            f"Unknown callback: {data}"
        )

        await query.edit_message_text(
            f"Unknown action: {data}"
        )
