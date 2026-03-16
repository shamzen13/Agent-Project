"""

Manages the Chroma vector db

TWO COLLECTIONS: 
- 'articles' : tagged articles from the fetcheragent db

- 'thoughts' : the agents own generated ideas ( used from mini project 4 onward )

"""

import logging 
import chromadb
import os

logger = logging.getLogger(__name__)


# ── Chroma DB path ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

# ── Initialise persistent Chroma client ───────────────────────────────────────
client = chromadb.PersistentClient(path=CHROMA_PATH)

# ── Collections ───────────────────────────────────────────────────────────────
# Think of collections like tables in a regular database
articles_collection = client.get_or_create_collection(
    name="articles",
    metadata={"hnsw:space": "cosine"}   # cosine similarity for semantic search
)

thoughts_collection = client.get_or_create_collection(
    name="thoughts",
    metadata={"hnsw:space": "cosine"}
)



#articles

def article_exists_in_chrome(article_id : int) -> bool:
    results = articles_collection.get(ids=[str(article_id)])
    return len(results["ids"]) > 0 

def store_article(article_id: int, text:str, embedding:list[float], metadata:dict):
    """
    Stores a single article embedding in the articles collection.

    article_id : the SQLite row id (used as the Chroma document id)
    text       : the text that was embedded (summary + themes)
    embedding  : the vector produced by embedder.py
    metadata   : dict of extra info stored alongside the vector
                 (source, category, lean, tone, etc.)
    """

    articles_collection.add(ids=[str(article_id)],
                            embeddings=[embedding],
                            documents = [text],
                            metadatas=[metadata]
                            )
    logger.debug(f"stored article {article_id} in vectorDB")


def search_articles(query_embedding: list[float], n_results: int = 5, category_filter: str = None) -> list[dict]:
    """
    searches articles collection for most semantically similar entries
    """

    where = {"category" : category_filter} if category_filter else None
    
    results = articles_collection.query(
        query_embeddings = [query_embedding],
        n_results = [n_results],
        where = where,
        include= ["documents", "metadatas", "distances"]

    )
    #reformat to clean list of dicts

    formatted = []
    for i in range(len(results["ids"][0])):
        formatted.append({
            "id" : results["ids"][0][i],
            "text" : results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance" : results["distances"][0][i]

        })

        return formatted 
    

#THOUGHTS 

def store_thought( thought_id: str, text: str, embedding:list[float], metadata:dict):

    thoughts_collection.add(
        ids=[thought_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata]
    )
    logger.info(f"stored thought {thought_id} in vector db")



def search_thoughts(query_embedding: list[float], n_results: int = 3) -> list[dict]:
    """
    Searches the agent's own past thoughts for relevant ideas.
    Used by the Synthesis Agent to retrieve its own memory before generating new ideas.
    """

    if thoughts_collection.count() == 0:
        return []
    
    results = thoughts_collection.query(
        query_embeddings=[query_embedding],
        n_results= n_results,
        include= ["documents", "metadatas", "distances"]
    )

    formatted= []
    for i in range (len(results["ids"][0])):
        formatted.append({
            "ids": results["ids"][0][i],
            "text" : results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]

        })

    return formatted 
    




# ── Stats ──────────────────────────────────────────────────────────────────────

def get_collection_counts() -> dict:
    """Returns the number of entries in each collection."""
    return {
        "articles": articles_collection.count(),
        "thoughts": thoughts_collection.count()
    }
        
