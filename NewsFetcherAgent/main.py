"""
entry point for news fetcher agent

Usage:
    python main.py            → starts the scheduled agent (runs forever)
    python main.py --once     → runs a single fetch cycle and exits
    python main.py --view     → prints the 20 most recent articles from DB

"""

import sys 
import logging
from src.database import init_db, get_recent_articles, get_article_count
from src.scheduler import run_fetch_cycle, start_scheduler
from config import FETCH_INTERVAL_HOURS

# LOGGING SETUP

logging.basicConfig(

    level = logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/agent.log"),
    ]

)

logger = logging.getLogger(__name__)

def view_articles():
    """pretty prints recent articles from the db"""

    articles = get_recent_articles(limit=20)
    total = get_article_count()

    print(f"\n{'='*60}")
    print(f"  STORED ARTICLES — Total: {total}")

    print(f"\n{'='*60}")


    if not articles:
        print("  No articles stored yet. Run a fetch cycle first.")
        return
    
    for row in articles:
        print(f"  [{row['category'].upper()}] {row['source']}")
        print(f"  {row['title'][:75]}")
        print(f"  {row['url'][:75]}")
        print(f"  Fetched: {row['fetched_at']}")
        print()


def main():
    init_db()

    args = sys.argv[1:]

    if "--view" in args:
        view_articles()

    elif "--once" in args:
        logger.info("Running single fetch cycle...")
        run_fetch_cycle()
        logger.info("Done. Run with --view to see stored articles.")

    else:
        # Default: start the scheduled agent
        logger.info("Starting News Fetcher Agent...")
        start_scheduler(interval_hours=FETCH_INTERVAL_HOURS)


if __name__ == "__main__":
    main()
    

