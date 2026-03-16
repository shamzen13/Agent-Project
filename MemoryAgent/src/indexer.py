"""
Orchestrates the indexing pipeline.
Reads tagged articles from SQL, embeds them, and stores in Chroma.
Skips articles already in the vector store so it's safe to run multiple times.
"""

import logging
from src.database import get_tagged_articles
from src.embedder import embed
from src.vector_store import store_article, article_exists_in_chroma, get_collection_counts

logger = logging.getLogger(__name__)


def build_article_text(article) -> str:
    """
    Constructs the text that gets embedded for each article.
    We embed the summary + themes together — this gives the richest
    semantic representation of what the article is actually about.
    """
    parts = []

    if article["summary"]:
        parts.append(article["summary"])

    if article["themes"]:
        parts.append(f"Themes: {article['themes']}")

    if article["ideological_lean"]:
        parts.append(f"Lean: {article['ideological_lean']}")

    if article["theological_tradition"] and article["theological_tradition"] != "None":
        parts.append(f"Tradition: {article['theological_tradition']}")

    return " | ".join(parts)


def build_article_metadata(article) -> dict:
    """
    Builds the metadata dict stored alongside each vector.
    Metadata lets you filter searches and display context in results.
    """
    return {
        "source": article["source"] or "",
        "title": article["title"] or "",
        "category": article["category"] or "",
        "ideological_lean": article["ideological_lean"] or "",
        "theological_tradition": article["theological_tradition"] or "",
        "emotional_tone": article["emotional_tone"] or "",
        "themes": article["themes"] or "",
    }


def run_indexing_cycle():
    """
    Main indexing loop.
    Fetches all tagged articles, embeds any that aren't in Chroma yet,
    and stores them in the vector database.
    """
    logger.info("=" * 50)
    logger.info("INDEXING CYCLE STARTED")
    logger.info("=" * 50)

    articles = get_tagged_articles()

    if not articles:
        logger.warning("No tagged articles found. Run TaggerAgent first.")
        return 0

    stored = 0
    skipped = 0

    for article in articles:
        article_id = article["id"]

        # Skip if already in Chroma
        if article_exists_in_chroma(article_id):
            skipped += 1
            continue

        # Build the text to embed
        text = build_article_text(article)

        if not text.strip():
            logger.warning(f"Empty text for article {article_id}, skipping.")
            continue

        # Generate embedding
        try:
            embedding = embed(text)
        except Exception as e:
            logger.error(f"Embedding failed for article {article_id}: {e}")
            continue

        # Build metadata
        metadata = build_article_metadata(article)

        # Store in Chroma
        store_article(article_id, text, embedding, metadata)
        stored += 1

        if stored % 20 == 0:
            logger.info(f"Progress: {stored} articles indexed...")

    counts = get_collection_counts()

    logger.info("=" * 50)
    logger.info("INDEXING CYCLE COMPLETE")
    logger.info(f"Newly indexed:     {stored}")
    logger.info(f"Already in Chroma: {skipped}")
    logger.info(f"Total in Chroma:   {counts['articles']}")
    logger.info("=" * 50)

    return stored