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


import os
import zipfile
import requests
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticRetriever:
    def __init__(self, source_dir: str, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the semantic retriever. Downloads the model if not available locally.

        Args:
            source_dir (str): Directory containing FAISS index and metadata files.
                              May include subdirectories representing groups.
            model_name (str): Name of the sentence-transformers model to use.
        """
        self.model = self.load_model(model_name)
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

    def load_model(self, model_name: str):
        """
        Loads the SentenceTransformer model either by name or from a local/remote path.

        Args:
            model_name (str): The name of the model or path to the model directory.

        Returns:
            SentenceTransformer: Loaded model.
        """
        model_dir = model_name  # Local directory where model might be stored

        # Hardcode the download URL for the model
        model_url = "https://drive.google.com/uc?id=1lmALQ0W4PHz_OekK7SvJH8nwbl-hKQ5s&export=download"

        # Check if the model is already available locally
        if not os.path.exists(model_dir):
            self.download_and_extract_model(model_url, model_dir)

        # Load the model
        return SentenceTransformer(model_dir)

    def download_and_extract_model(self, model_url: str, model_dir: str):
        """
        Downloads and extracts the model from the given URL.

        Args:
            model_url (str): The URL to download the model from.
            model_dir (str): Directory to save the extracted model.
        """
        # Download the model
        print(f"Downloading model from {model_url}...")
        r = requests.get(model_url)
        with open("model.zip", "wb") as f:
            f.write(r.content)
        
        # Unzip the model
        with zipfile.ZipFile("model.zip", "r") as zip_ref:
            zip_ref.extractall(model_dir)
        print(f"Model downloaded and extracted to {model_dir}")

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

