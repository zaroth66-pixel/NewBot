from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import logging
from app.worker.tasks import scan_market

logger = logging.getLogger(__name__)

tz = pytz.timezone("Africa/Addis_Ababa")
scheduler = AsyncIOScheduler(timezone=tz)


def start_scheduler():
    logger.info("Starting APScheduler")

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
    logger.info("APScheduler started")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("APScheduler stopped")
