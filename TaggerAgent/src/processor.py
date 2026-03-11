"""
processor.py
Orchestrates the tagging loop.
Fetches untagged articles in batches, tags them, and saves results back.
t's the orchestrator that connects everything together.
"""


import time 
import logging
from src.database import(
    get_untagged_articles,
    save_tags,
    get_tagged_count,
    get_untagged_count
)

from src.tagger import tag_article
logger = logging.getLogger(__name__)

#SETTINGS

BATCH_SIZE = 10
DELAY_BETWEEN_CALLS = 1 # seconds between API calls (be polite to the API)


def run_tagging_cycle():
    """
    main tagging loop, processes all untagged articles in batches until none remain
    """

    logger.info("="*50)
    logging.info("TAGGING CYCLE STARTED")
    logger.info("="*50)


    total_tagged = 0
    total_failed = 0

    while True:
        #fetch batch of untagged articles
        articles = get_untagged_articles(limit=BATCH_SIZE)

        if not articles:
            logger.info("no more untagged articles, cycle complete.")
            break
        
        
        for article in articles:
            article_id = article["id"]
            title = article["title"]
            content = article["content"]
            category = article["category"]

            logger.info(f"Tagging [{article_id}]: {title[:60]}")

        
            tags = tag_article(article_id,title,content, category)

            if tags:
                save_tags(
                    article_id=article_id,
                    summary=tags["summary"],
                    ideological_lean=tags["ideological_lean"],
                    theological_tradition=tags["theological_tradition"],
                    emotional_tone=tags["emotional_tone"]
                )

                total_tagged += 1
            else:
                logger.warning(f"Failed to tag article {article_id} — skipping")
                total_failed += 1

            # Small delay between API calls to avoid rate limiting
            time.sleep(DELAY_BETWEEN_CALLS)

    logger.info("=" * 50)
    logger.info("TAGGING CYCLE COMPLETE")
    logger.info(f"Tagged this cycle:     {total_tagged}")
    logger.info(f"Failed this cycle:     {total_failed}")
    logger.info(f"Total tagged in DB:    {get_tagged_count()}")
    logger.info(f"Remaining untagged:    {get_untagged_count()}")
    logger.info("=" * 50)

    return total_tagged, total_failed

