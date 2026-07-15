from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import logging
from app.worker.tasks import scan_market

logger = logging.getLogger(__name__)

# Use Africa/Addis_Ababa timezone as requested
tz = pytz.timezone('Africa/Addis_Ababa')
scheduler = AsyncIOScheduler(timezone=tz)

def start_scheduler():
    logger.info("Starting APScheduler")
    
    # Schedule market scans for major pairs every hour
    pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF"]
    for pair in pairs:
        scheduler.add_job(
            scan_market.delay,
            CronTrigger(minute=0),
            args=[pair],
            id=f"scan_{pair.replace('/', '_')}",
            replace_existing=True
        )
        
    scheduler.start()