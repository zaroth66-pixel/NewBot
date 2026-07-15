from app.core.celery_app import celery_app
from app.services.trading_logic import trading_logic
from app.db.session import async_session
from app.db.models import Signal, User
from app.core.config import settings
from telegram import Bot
from sqlalchemy.future import select
import asyncio
import logging

logger = logging.getLogger(__name__)

async def _process_and_notify_signal(symbol: str):
    try:
        result = await trading_logic.analyze_and_generate_signal(symbol)
        
        if result:
            logger.info(f"Signal generated for {symbol}: {result['direction']}")
            
            async with async_session() as db:
                # Save to DB
                new_signal = Signal(
                    currency_pair=symbol,
                    direction=result['direction'],
                    entry_price=result['entry_price'],
                    stop_loss=result['stop_loss'],
                    tp1=result['tp1'],
                    tp2=result.get('tp2'),
                    confidence=result['confidence'],
                    probability=result['probability'],
                    risk_score=result['risk_score'],
                    risk_reward=result['risk_reward'],
                    trade_duration=result.get('trade_duration'),
                    ai_reasoning=result['ai_reasoning']
                )
                db.add(new_signal)
                await db.commit()
                
                # Notify Users
                if settings.TELEGRAM_BOT_TOKEN:
                    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                    # Find users who want new signal notifications
                    users_query = await db.execute(select(User).filter(User.notify_new_signals == True))
                    users = users_query.scalars().all()
                    
                    message = (
                        f"🚨 *NEW SIGNAL: {symbol}*\n\n"
                        f"Direction: {result['direction'].value}\n"
                        f"Entry: {result['entry_price']}\n"
                        f"Take Profit 1: {result['tp1']}\n"
                        f"Take Profit 2: {result.get('tp2', 'N/A')}\n"
                        f"Stop Loss: {result['stop_loss']}\n"
                        f"Confidence: {result['confidence']}%\n\n"
                        f"💡 *Reasoning:*\n{result['ai_reasoning'][:500]}..." # Truncate reasoning to avoid too long messages
                    )
                    
                    for user in users:
                        try:
                            await bot.send_message(
                                chat_id=user.telegram_id,
                                text=message,
                                parse_mode="Markdown"
                            )
                        except Exception as e:
                            logger.error(f"Failed to send signal to user {user.telegram_id}: {str(e)}")
        else:
            logger.info(f"No signal generated for {symbol}")
    except Exception as e:
        logger.error(f"Error in _process_and_notify_signal for {symbol}: {str(e)}")

@celery_app.task(name="app.worker.tasks.scan_market")
def scan_market(symbol: str):
    logger.info(f"Starting market scan for {symbol}")
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(_process_and_notify_signal(symbol))
    return f"Scan completed for {symbol}"