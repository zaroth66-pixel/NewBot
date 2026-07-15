# AI-Powered Forex Signal Telegram Bot

A production-ready Telegram bot providing AI-driven forex trading signals, market analysis, and portfolio management. Everything runs entirely within Telegram using inline keyboard buttons.

## Features
- **Live AI Signals:** Multi-timeframe analysis generating BUY/SELL/NO TRADE signals with Entry, Stop Loss, and Take Profit levels.
- **AI Integration:** Uses Groq for fast technical analysis and Google Gemini for detailed reasoning and natural language explanations.
- **Market Scanners & Sessions:** Detects active trading sessions (Sydney, Tokyo, London, New York) and scans for opportunities.
- **Telegram Native UI:** 100% InlineKeyboardMarkup based navigation. No external web dashboard needed for users.
- **Admin Dashboard:** Manage users, premium subscriptions, and view analytics directly in Telegram.
- **Background Tasks:** Uses Celery and APScheduler for periodic market scanning and notification dispatch.

## Tech Stack
- Python 3.12
- FastAPI
- python-telegram-bot v21+
- PostgreSQL (asyncpg)
- Redis
- Celery
- APScheduler
- SQLAlchemy + Alembic
- Docker + Docker Compose

## Setup Instructions

1. **Clone the repository**
2. **Copy environment variables:**
   ```bash
   cp .env.example .env
   ```
   Fill in your Telegram Bot Token, Groq API Key, Gemini API Key, and Market Data Provider API keys.

3. **Run with Docker Compose:**
   ```bash
   docker-compose up -d --build
   ```

4. **Database Migrations:**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

## Architecture
- `app/main.py`: FastAPI application entry point.
- `app/bot/`: Telegram bot handlers and keyboards.
- `app/services/`: Business logic, AI providers, and market data integrations.
- `app/worker/`: Celery tasks.
- `app/db/`: SQLAlchemy models and session management.

## Testing
Run tests using pytest:
```bash
docker-compose exec api pytest
```

## Disclaimer
This software is for educational purposes. Never promise guaranteed profits. Base every recommendation on transparent analysis and configurable risk management.