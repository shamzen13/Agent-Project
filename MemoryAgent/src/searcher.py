

import logging
from src.embedder import embed
from src.vector_store import search_articles, search_thoughts

logger = logging.getLogger(__name__)


def search_memory(query: str, n_articles: int = 5, n_thoughts: int = 3, category_filter: str = None) -> dict:
    """
    The main memory retrieval function.
    Takes a plain text query, embeds it, and searches both collections.

    query           : what ur looking for 
    n_articles      : how many articles to retrieve
    n_thoughts      : how many past agent thoughts to retrieve
    category_filter : optionally limit articles to 'theology' or 'politics'

    Returns a dict with 'articles' and 'thoughts' lists.
    """
    logger.info(f"Searching memory for: '{query}'")

    # Embed the query using the same model used to embed the stored content
    query_embedding = embed(query)

    # Search both collections
    articles = search_articles(query_embedding, n_results=n_articles,category_filter=category_filter)
    thoughts = search_thoughts(query_embedding, n_results=n_thoughts)

    logger.info(f"Found {len(articles)} articles, {len(thoughts)} thoughts.")

    return {
        "query": query,
        "articles": articles,
        "thoughts": thoughts
    }


def format_search_results(results: dict) -> str:
    """
    Formats search results into a readable string for terminal display.
    Also used by the Synthesis Agent to inject memory into its prompt.
    """
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  MEMORY SEARCH: \"{results['query']}\"")
    lines.append(f"{'='*60}\n")

    if results["articles"]:
        lines.append("  RELEVANT ARTICLES:")
        lines.append("")
        for i, a in enumerate(results["articles"], 1):
            meta = a["metadata"]
            similarity = round((1 - a["distance"]) * 100, 1)
            lines.append(f"  {i}. [{meta.get('category', '').upper()}] "
                         f"{meta.get('title', '')[:65]}")
            lines.append(f"     {a['text'][:120]}")
            lines.append(f"     Lean: {meta.get('ideological_lean', '')} | "
                         f"Tone: {meta.get('emotional_tone', '')} | "
                         f"Match: {similarity}%")
            lines.append("")
    else:
        lines.append("  No relevant articles found.")
        lines.append("")

    if results["thoughts"]:
        lines.append("  PAST AGENT THOUGHTS:")
        lines.append("")
        for i, t in enumerate(results["thoughts"], 1):
            similarity = round((1 - t["distance"]) * 100, 1)
            lines.append(f"  {i}. {t['text'][:120]}")
            lines.append(f"     Match: {similarity}%")
            lines.append("")
    else:
        lines.append("  No past thoughts found yet.")
        lines.append("")

    return "\n".join(lines)