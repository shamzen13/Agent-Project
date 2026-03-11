import feedparser
import logging
from src.cleaner import clean_text, truncate
from src.database import insert_article



logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# ADD OR REMOVE FEEDS HERE FREELY
# Format: ("Display Name", "Feed URL", "category")
# ─────────────────────────────────────────────

THEOLOGY_FEEDS = [
    
    ("First Things", "https://www.firstthings.com/rss", "theology"),
    ("The Gospel Coalition", "https://www.thegospelcoalition.org/feed/", "theology"),
    ("Aeon - Philosophy", "https://aeon.co/feed.rss", "theology"),
    ("ABC Religion & Ethics", "https://www.abc.net.au/religion/rss.xml", "theology"),

]


POLITICS_FEEDS = [
    ("The Guardian - Politics", "https://www.theguardian.com/politics/rss", "politics"),
    ("BBC News - Politics", "http://feeds.bbci.co.uk/news/politics/rss.xml", "politics"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml", "politics"),
    ("NPR News", "https://feeds.npr.org/1001/rss.xml", "politics"),
    ("Foreign Affairs", "https://www.foreignaffairs.com/rss.xml", "politics"),

]

ALL_FEEDS = THEOLOGY_FEEDS + POLITICS_FEEDS

def fetch_rss_feed(name: str, url: str, category: str) -> int:
    logger.info(f"fetching rss:{name}")
    save_count =0

    try: 
        feed = feedparser.parse(url)

        if feed.bozo:
            logger.warning(f"feed may be malformed : {name}")

            #dividing entries to able to assign it to different classes (?)
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                link = entry.get("link","" ).strip()

                if not title or not link:
                    continue
                
                #get content - try multiple fields feedparser may return
                #extracts attributes and assigns to raw content's attr
                raw_content = "" 
                if hasattr(entry, "content"):
                    raw_content = entry.conent[0].get("value" , "")
                elif hasattr(entry,"summary"):
                    raw_content = entry.summary
                elif hasattr(entry, "description"):
                    raw_content = entry.description

                content = truncate(clean_text(raw_content), max_chars=2000) # makes sure  raw content is limited to max chars

                #publushed date
                published = ""
                if hasattr(entry, "published"):
                    published = entry.published
                elif hasattr(entry, "updated"):
                    published = entry.updated
                

                was_saved = insert_article(
                    source = name,
                    title = title,
                    url = link,
                    content=content,
                    published_at=published,
                    category=category
                )

                if was_saved:
                    save_count += 1

    except Exception as e:
        logger.error(f"Error fetching {name}:{e}")

    return save_count


def fetch_all_rss() -> int:
    """ fetches all configured RSS feeds, returns total new articles saved"""
    total = 0 
    for name, url, category in ALL_FEEDS:
        total += fetch_rss_feed(name, url,category)
    logger.info(f"RSS fetch complete, total articles (new) : {total}" )
    return total

