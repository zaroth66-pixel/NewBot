from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_premium_plans_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "🥉 Monthly ($19.99)",
                callback_data="buy_MONTHLY"
            )
        ],
        [
            InlineKeyboardButton(
                "🥈 Quarterly ($49.99)",
                callback_data="buy_QUARTERLY"
            )
        ],
        [
            InlineKeyboardButton(
                "🥇 Yearly ($149.99)",
                callback_data="buy_YEARLY"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 Lifetime ($499.99)",
                callback_data="buy_LIFETIME"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="main_menu"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_payment_methods_keyboard(plan: str, payment_url: str):
    keyboard = [
        [
            InlineKeyboardButton(
                "💳 Pay with Card (Stripe)",
                url=payment_url
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back to Plans",
                callback_data="premium"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "📈 Live Signals",
                callback_data="live_signals"
            ),
            InlineKeyboardButton(
                "🧠 AI Analysis",
                callback_data="ai_analysis"
            )
        ],
        [
            InlineKeyboardButton(
                "🔍 Market Scanner",
                callback_data="market_scanner"
            ),
            InlineKeyboardButton(
                "🕒 Trading Sessions",
                callback_data="trading_sessions"
            )
        ],
        [
            InlineKeyboardButton(
                "📰 Forex News",
                callback_data="forex_news"
            ),
            InlineKeyboardButton(
                "📅 Economic Calendar",
                callback_data="economic_calendar"
            )
        ],
        [
            InlineKeyboardButton(
                "💼 Portfolio",
                callback_data="portfolio"
            ),
            InlineKeyboardButton(
                "📜 Signal History",
                callback_data="signal_history"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Favorites",
                callback_data="favorites"
            ),
            InlineKeyboardButton(
                "💎 Premium",
                callback_data="premium"
            )
        ],
        [
            InlineKeyboardButton(
                "👤 Profile",
                callback_data="profile"
            ),
            InlineKeyboardButton(
                "⚙️ Settings",
                callback_data="settings"
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Support",
                callback_data="support"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_back_home_keyboard(refresh_data=None):
    row = [
        InlineKeyboardButton(
            "🏠 Home",
            callback_data="main_menu"
        ),
        InlineKeyboardButton(
            "⬅️ Back",
            callback_data="back"
        )
    ]

    if refresh_data:
        row.append(
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data=refresh_data
            )
        )

    return InlineKeyboardMarkup([row])


def get_admin_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "👥 Users",
                callback_data="admin_users"
            ),
            InlineKeyboardButton(
                "💰 Revenue",
                callback_data="admin_revenue"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 Premium",
                callback_data="admin_premium"
            ),
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="admin_broadcast"
            )
        ],
        [
            InlineKeyboardButton(
                "🎟️ Coupons",
                callback_data="admin_coupons"
            ),
            InlineKeyboardButton(
                "💳 Payments",
                callback_data="admin_payments"
            )
        ],
        [
            InlineKeyboardButton(
                "📈 Signals",
                callback_data="admin_signals"
            ),
            InlineKeyboardButton(
                "📝 Logs",
                callback_data="admin_logs"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 API Health",
                callback_data="admin_api_health"
            ),
            InlineKeyboardButton(
                "🔄 Restart Workers",
                callback_data="admin_restart"
            )
        ],
        [
            InlineKeyboardButton(
                "💾 Backups",
                callback_data="admin_backups"
            ),
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="main_menu"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)
