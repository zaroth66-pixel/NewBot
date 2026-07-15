from app.core.celery_app import celery_app
from app.services.trading_logic import trading_logic
import asyncio
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="app.worker.tasks.scan_market")
def scan_market(symbol: str):
    logger.info(f"Starting market scan for {symbol}")
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    result = loop.run_until_complete(trading_logic.analyze_and_generate_signal(symbol))
    
    if result:
        logger.info(f"Signal generated for {symbol}: {result}")
        # Here we would save to DB and trigger Telegram notification
    else:
        logger.info(f"No signal generated for {symbol}")
        
    return result