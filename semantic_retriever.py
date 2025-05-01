"""
SemanticRetriever
-----------------

It is suitable for building retrieval-based recommenders, semantic search engines, or as the
retrieval layer in RAG (Retrieval-Augmented Generation) systems.

This module provides a simple semantic search-based recommender system using a SentenceTransformer
encoder and a FAISS vector index.

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


import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticRetriever:
    def __init__(self, source_dir: str, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the semantic retriever.

        Args:
            source_dir (str): Directory containing FAISS index and metadata files.
                              May include subdirectories representing groups.
            model_name (str): Name of the sentence-transformers model to use.
        """
        self.model = SentenceTransformer(model_name)
        self.group_to_index = {}
        self.group_to_metadata = {}

        for entry in os.listdir(source_dir):
            full_path = os.path.join(source_dir, entry)
            if os.path.isdir(full_path):  # grouped data
                index_path = os.path.join(full_path, "projects.index")
                metadata_path = os.path.join(full_path, "metadata.json")
                if os.path.exists(index_path) and os.path.exists(metadata_path):
                    self.group_to_index[entry] = faiss.read_index(index_path)
                    with open(metadata_path, "r", encoding="utf-8") as f:
                        self.group_to_metadata[entry] = json.load(f)
            elif entry == "projects.index":  # ungrouped data
                index_path = os.path.join(source_dir, "projects.index")
                metadata_path = os.path.join(source_dir, "metadata.json")
                self.group_to_index[None] = faiss.read_index(index_path)
                with open(metadata_path, "r", encoding="utf-8") as f:
                    self.group_to_metadata[None] = json.load(f)

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

    def search(self, query: str, top_k: int = 5, group: str = None) -> list:
        """
        Searches for top-k items most similar to the input query.

        Args:
            query (str): User query string.
            top_k (int): Number of top results to return.
            group (str, optional): Group name to restrict search to. Defaults to None.

        Returns:
            list: A list of metadata dicts corresponding to the top-k results.
        """
        if group not in self.group_to_index:
            raise ValueError(f"Group '{group}' not found. Available groups: {list(self.group_to_index.keys())}")

        index = self.group_to_index[group]
        metadata = self.group_to_metadata[group]
        query_vector = self.embed_query(query)
        distances, indices = index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            item = metadata[str(idx)]
            results.append(item)
        return results
