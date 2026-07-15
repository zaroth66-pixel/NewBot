from telegram import Update
from telegram.ext import ContextTypes
from app.bot.keyboards import get_main_menu_keyboard, get_admin_keyboard, get_premium_plans_keyboard, get_payment_methods_keyboard
from app.services.payment import payment_service
import logging

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🤖 Welcome to AI-Powered Forex Signal Bot!\n\n"
        "I provide real-time, AI-driven forex trading signals and market analysis.\n\n"
        "Select an option below to get started:"
    )
    
    keyboard = get_main_menu_keyboard()
    
    if update.message:
        await update.message.reply_text(welcome_message, reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_message, reply_markup=keyboard)

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # In a real app, verify user is admin against DB
    user_id = update.effective_user.id
    
    admin_message = "🛠️ Admin Dashboard\nSelect a management option:"
    keyboard = get_admin_keyboard()
    
    if update.message:
        await update.message.reply_text(admin_message, reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.edit_message_text(admin_message, reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "main_menu":
        await start_command(update, context)
    elif data == "live_signals":
        # Implementation for live signals
        await query.edit_message_text("📈 Live Signals\n\nFetching latest signals...")
    elif data == "ai_analysis":
        await query.edit_message_text("🧠 AI Analysis\n\nSelect a currency pair to analyze.")
    elif data == "premium":
        await query.edit_message_text(
            "💎 Premium Subscriptions\n\n"
            "Unlock advanced AI analysis, unlimited signals, and priority support.\n\n"
            "Select a plan:",
            reply_markup=get_premium_plans_keyboard()
        )
    elif data.startswith("buy_"):
        plan = data.split("_")[1]
        user_id = update.effective_user.id # In real app, fetch internal DB user.id
        
        # Generate Stripe session
        payment_url = payment_service.create_stripe_checkout_session(user_id=user_id, plan=plan)
        
        if payment_url:
            await query.edit_message_text(
                f"You selected the {plan} plan.\n\n"
                "Please complete your payment securely via Stripe:",
                reply_markup=get_payment_methods_keyboard(plan, payment_url)
            )
        else:
            await query.edit_message_text(
                "Sorry, the payment system is currently unavailable. Please try again later.",
                reply_markup=get_premium_plans_keyboard()
            )
    # Add other handlers here...
    else:
        await query.edit_message_text(f"Not implemented yet: {data}")