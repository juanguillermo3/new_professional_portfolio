"""
SemanticRetriever
-----------------

This module provides a simple semantic search-based recommender system using a SentenceTransformer
encoder and a FAISS vector index.

It is suitable for building retrieval-based recommenders, semantic search engines, or as the
retrieval layer in RAG (Retrieval-Augmented Generation) systems.

Terminology Mapping
-------------------
This implementation maps your working terminology to standard concepts in Recommender Systems
and LLM-driven retrieval systems:

| Your Term                        | Recsys/LLM Equivalent                       |
|----------------------------------|---------------------------------------------|
| “Module to embed the query”      | Query Encoder                               |
| “Match against the vector store” | Nearest Neighbor Search on a Vector Index   |
| “Vector store”                   | FAISS Vector Index                          |
| “Keyword from user”              | Query Text                                  |
| “Portfolio items”                | Corpus / Documents / Items to Recommend     |
| “Embedding model”                | Encoder Model (e.g., BERT, CLIP, etc.)      |
| “Recommendation from search”     | Top-k Nearest Items by Vector Similarity    |

Typical Workflow
----------------
1. Offline:
   - Embed all portfolio items
   - Build a FAISS index with the document vectors
   - Store associated metadata (title, URL, etc.) in a JSON file

2. Online:
   - Accept user query from frontend (search input)
   - Encode the query with the same model
   - Search the FAISS index for top-k similar items
   - Return the matched metadata for display

Usage Example:
--------------
    retriever = SemanticRetriever("index.faiss", "metadata.json")
    results = retriever.search("data visualization")

Author: Your Name
"""

import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from typing import Optional, Dict, List

class SemanticRetriever:
    def __init__(self, index_path: str, metadata_path: str, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the semantic retriever.

        Args:
            index_path (str): Path to the FAISS index file.
            metadata_path (str): Path to the JSON file containing item metadata.
            model_name (str): Name of the sentence-transformers model to use.
        """
        self.index = faiss.read_index(index_path)
        self.model = SentenceTransformer(model_name)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def embed_query(self, text: str) -> np.ndarray:
        """
        Encodes a query string into a normalized vector.

        Args:
            text (str): The user query.

        Returns:
            np.ndarray: A 1xD float32 array representing the query embedding.
        """
        embedding = self.model.encode([text], normalize_embeddings=True)
        return embedding.astype("float32")


    def search(self, query: str, top_k: int = 5, filtering_query: Optional[Dict[str, str]] = None) -> List[dict]:
        """
        Searches for top-k items most similar to the input query and optionally filters results.

        Args:
            query (str): User query string.
            top_k (int): Number of top results to return.
            filtering_query (dict, optional): A dict representing field-based regex filters.
                Example: {'project': '^proj_abc$', 'language': 'python'}

        Returns:
            list: A list of metadata dicts matching the query and filters.
        """
        query_vector = self.embed_query(query)
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            item = self.metadata.get(str(idx), {})

            if filtering_query:
                # Apply regex-based filtering on item fields
                match = all(
                    re.search(pattern, str(item.get(key, "")))
                    for key, pattern in filtering_query.items()
                )
                if not match:
                    continue

            results.append(item)

        return results
