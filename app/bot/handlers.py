from telegram import Update
from telegram.ext import ContextTypes
import logging

from app.bot.keyboards import (
    get_main_menu_keyboard,
    get_admin_keyboard,
    get_premium_plans_keyboard,
    get_payment_methods_keyboard,
    get_currency_pairs_keyboard,
    get_back_home_keyboard
)

from app.services.payment import payment_service
from app.services.ai_provider import ai_provider


logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_message = (
        "🤖 Welcome to Selina AI Trading Bot!\n\n"
        "📈 AI-powered forex signals\n"
        "🧠 AI market analysis\n"
        "📊 Trading insights\n"
        "💎 Premium signals\n\n"
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

    await update.message.reply_text(
        "🛠️ Admin Dashboard\n\n"
        "Select management option:",
        reply_markup=get_admin_keyboard()
    )



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data


    if data == "main_menu":

        await start_command(update, context)



   # LIVE SIGNALS
elif data == "live_signals":

    await query.edit_message_text(
        "📈 Live Signals\n\n"
        "⏳ Scanning forex markets...\n\n"
        "🔎 EUR/USD\n"
        "🔎 GBP/USD\n"
        "🔎 USD/JPY"
    )


    pairs = [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY"
    ]


    results = []


    for pair in pairs:

        try:

            market_data = {
                "pair": pair,
                "timeframe": "H1",
                "indicators": [
                    "RSI",
                    "MACD",
                    "EMA",
                    "Support Resistance"
                ]
            }


            analysis = await ai_provider.analyze_market_groq(
                market_data,
                "H1"
            )


            results.append(
                f"📊 {pair}\n\n{analysis}"
            )


        except Exception as e:

            logger.error(
                f"{pair} scan error: {e}"
            )

            results.append(
                f"❌ {pair}\nAnalysis failed"
            )


    final_message = (
        "📈 Live AI Trading Signals\n\n"
        + "\n\n━━━━━━━━━━━━━━\n\n".join(results)
    )


    await query.edit_message_text(
        final_message
    )



    elif data == "ai_analysis":

        await query.edit_message_text(
            "🧠 AI Analysis\n\n"
            "Select currency pair:",
            reply_markup=get_currency_pairs_keyboard()
        )



    elif data.startswith("analyze_"):

        pair = data.replace("analyze_", "")

        await query.edit_message_text(
            f"🧠 AI Analysis\n\n"
            f"Pair: {pair}\n\n"
            "⏳ AI is analyzing market data..."
        )


        market_data = {
            "pair": pair,
            "timeframe": "H1",
            "indicators": [
                "RSI",
                "MACD",
                "EMA",
                "Support Resistance"
            ]
        }


        try:

            result = await ai_provider.analyze_market_groq(
                market_data,
                "H1"
            )


            await query.edit_message_text(
                f"📊 {pair} AI Signal\n\n"
                f"{result}",
                reply_markup=get_back_home_keyboard()
            )


        except Exception as e:

            logger.error(
                f"AI analysis error: {e}"
            )

            await query.edit_message_text(
                "❌ AI analysis failed.",
                reply_markup=get_back_home_keyboard()
            )



    elif data == "market_scanner":

        await query.edit_message_text(
            "🔍 Market Scanner\n\n"
            "⏳ Scanning global forex market...\n\n"
            "EUR/USD ✅\n"
            "GBP/USD ✅\n"
            "USD/JPY ✅",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "forex_news":

        await query.edit_message_text(
            "📰 Forex News\n\n"
            "Fetching latest market news...",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "trading_sessions":

        await query.edit_message_text(
            "🕒 Trading Sessions\n\n"
            "🌏 Asian Session\n"
            "🇬🇧 London Session\n"
            "🇺🇸 New York Session",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "economic_calendar":

        await query.edit_message_text(
            "📅 Economic Calendar\n\n"
            "Loading economic events...",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "portfolio":

        await query.edit_message_text(
            "💼 Portfolio\n\n"
            "No active trades yet.",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "signal_history":

        await query.edit_message_text(
            "📜 Signal History\n\n"
            "No previous signals.",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "favorites":

        await query.edit_message_text(
            "⭐ Favorites\n\n"
            "No favorite pairs saved.",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "profile":

        user = update.effective_user

        await query.edit_message_text(
            "👤 Profile\n\n"
            f"Name: {user.first_name}\n"
            f"Username: @{user.username}\n"
            f"ID: {user.id}",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "settings":

        await query.edit_message_text(
            "⚙️ Settings\n\n"
            "Notification settings coming soon.",
            reply_markup=get_back_home_keyboard()
        )



    elif data == "support":

        await query.edit_message_text(
            "❓ Support\n\n"
            "Contact: @your_support",
            reply_markup=get_back_home_keyboard()
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


        try:

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


        except Exception as e:

            logger.error(
                f"Payment error: {e}"
            )

            await query.edit_message_text(
                "❌ Payment failed."
            )



    elif data == "back":

        await start_command(update, context)



    else:

        logger.warning(
            f"Unknown callback: {data}"
        )

        await query.edit_message_text(
            "❌ Unknown action.",
            reply_markup=get_back_home_keyboard()
        )
