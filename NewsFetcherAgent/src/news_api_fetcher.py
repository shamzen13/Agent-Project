

"""
fetches articles from newsapi.org for keyword based theology and politics queries

"""

import requests
import logging
from datetime import datetime, timedelta
from src.cleaner import clean_text, truncate
from src.database import insert_article
from config import NEWS_API_KEY

logger = logging.getLogger(__name__)

NEWSAPI_URL = "https://newsapi.org/v2/everything"

# ─────────────────────────────────────────────
# SEARCH QUERIES
# These are the keywords the agent searches for.
# Add or modify freely.
# ─---------------------------------------------

THEOLOGY_QUERIES = [
    "theology religion philosophy",
    "liberation theology",
    "faith politics church",
    "religious ethics morality",
    "islam", "christianity", "judiasm"
]

POLITICS_QUERIES = [
    "political philosophy power",
    "democracy authoritarianism",
    "political ideology movement",
    "sovereignty justice governance",
     "Political systems",
    "political ideologies",
    "democracy",
    "liberalism",
    "conservatism", "socialism",
    "nationalism",  "The Presidency", "Executive Branch", 
    "Congress", "legislative branch", "Supreme Court", 
    "judicial branch", "separation of powers"
]


def fetch_newsapi_query(query:str, category: str, days_back:int = 2)-> int:
    """
    searches newsAPI for given query and saves result to database
    days_back ; how far back to search ( free limited to 30 days)
    returns number of new articles saved

    """

    if not NEWS_API_KEY:
        logger.warning("NEWS_API_KEY not set, skipping newsAPI fetch")

    from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    params = {

        "q" : query,
        "from" : from_date,
        "sortBy" : "relavency",
        "language" : "en",
        "pageSize" : "10",
        "apiKey" : NEWS_API_KEY

    }

    saved_count = 0

    try:
        response = requests.get(NEWSAPI_URL, params = params, timeout= 10)
        response.raise_for_status()
        data = response.json()

        articles= data.get("articles", [])
        logger.info(f"newsAPI [{query}]: {len(articles)} results")

        for article in articles: 
            title = (article.get("title") or "").strip()
            url = (article.get("url") or "").strip()


            if "[Removed]" in title or not url:
                continue

            raw_content = article.get("content") or article.get("description") or ""
            content = truncate(clean_text(raw_content), max_chars=2000)
            published = article.get("publishedAt", "")
            source = article.get("source", {}).get("name", "NewsAPI")

            was_saved = insert_article(
                source=source,
                title=title,
                url=url,
                content=content,
                published_at=published,
                category=category
            )
        
            if was_saved:
                saved_count += 1

    except requests.RequestException as e :
        logger.error(f"NewsAPI request failed for [{query}]: {e}")
    except Exception as e:
        logger.error(f"Unexpected error for [{query}]: {e}")

    return saved_count



def fetch_all_newsapi() -> int:
    """runs all theo and politic queries and returns total new articles saved"""

    total = 0
     
    for query in THEOLOGY_QUERIES:
        total += fetch_newsapi_query(query, "theology")
    
    for query in POLITICS_QUERIES:
        total += fetch_newsapi_query(query, "politics")

    logger.info(f"NewsAPI fetch complete, total new articles : {total}")
    return total


