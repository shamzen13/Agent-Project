"""
loads the sentence transformer model and converst the text into vector emebddings
"""

import logging 
from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)

MODEL_NAME = "all-MiniLM-L6-v2" # downloads on first run then caches locally after

#load once at module level so its not reloaded each func call
logger.info(f"loading embedding model : {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)
logger.info(f"embedding model loaded")

def embed( text : str) -> list[float]:
    # string to vector embedding

    if not text or not text.strip():
        raise ValueError("cant embed empty text")
    
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()

def embed_batch(texts: list[str]) -> list[list[float]]:
    # list of strings into embeddings in one batch - instead of looping embed
    if not texts:
        return []
    
    embeddings = model.encode(texts, convert_to_tensor=False, show_progress_bar=True)
    return [e.tolist() for e in embeddings]


