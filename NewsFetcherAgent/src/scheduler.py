
"""
scheduler.py
Sets up APScheduler to run fetch jobs automatically every few hours.
Also provides a manual trigger function for testing.
"""




import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.rss_fetcher import fetch_all_rss
from src.news_api_fetcher import fetch_all_newsapi
from src.database import get_article_count

logger = logging.getLogger(__name__)

def run_fetch_cycle(): 
    """
    single fetch cycle --> runs RSS + NewsAPI fetchers
    called both manually and by the scheduler
    """

    logger.info("=" * 50)
    logger.info("FETCH CYCLE STARTED")
    logger.info("=" * 50)

    rss_new = fetch_all_rss()
    api_new = fetch_all_newsapi()

    total_new = rss_new + api_new
    total_stored = get_article_count()


    logger.info("=" * 50)
    logger.info(f"FETCH CYCLE COMPLETE")
    logger.info(f"New articles this cycle: {total_new}")
    logger.info(f"Total articles in DB:    {total_stored}")
    logger.info("=" * 50)


def start_scheduler(interval_hours : int = 4):
    """
    Starts the background scheduler.
    Runs a fetch cycle immediately, then every `interval_hours` hours.

    interval_hours: how often to re-fetch (default every 4 hours)
    """

    scheduler = BlockingScheduler()

    scheduler.add_job( 
        func=run_fetch_cycle,
        trigger=IntervalTrigger(hours=interval_hours),
        id="fetch_cycle",
        name="News Fetch Cycle",
        replace_existing=True,
        max_instances=1,  #--> prevents overlappiong runs
    )






    logger.info(f"Scheduler started. Fetching every {interval_hours} hours.")
    logger.info("Press Ctrl+C to stop.\n")

    # Run once immediately on start
    run_fetch_cycle()

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
        scheduler.shutdown()