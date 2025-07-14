"""Model code."""

import json
import os
from typing import Any, List

import faiss
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

torch.set_num_threads(1)


class SimilarityModel:
    def __init__(
        self,
        folder: str,
        embed_model_name: str = "all-MiniLM-L6-v2",
        embed_device: str = "cpu",
        embed_batch_size: int = 64,
        embed_max_seq_length: int = 512,
    ) -> None:

        self.folder = folder
        self.embed_model_name = embed_model_name
        self.embed_device = embed_device
        self.embed_batch_size = embed_batch_size
        self.embed_max_seq_length = embed_max_seq_length

        self.embed_model = SentenceTransformer(
            self.embed_model_name, device=self.embed_device
        )
        self.embed_model.max_seq_length = self.embed_max_seq_length

    def infer(self, id: int, texts: List[str], top_k: int = 1) -> List[int]:
        embeddings = self.embed(texts)
        _, neighbors = self.faiss_index.search(embeddings, top_k)
        ret = []
        for neighbor in neighbors[0]:
            if id != neighbor:
                try:
                    ret.append(self.index_to_id[str(neighbor)])
                except KeyError:
                    continue
        return ret

    def embed(self, texts: List[str]) -> np.ndarray[Any, Any]:
        embeddings = self.embed_model.encode(
            texts,
            batch_size=self.embed_batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings

    def load(
        self,
    ) -> None:
        if not os.path.exists(self.folder):
            raise ValueError(f"The folder '{self.folder}' does not exsit.")

        with open(f"{self.folder}/embeddings.npy", "rb") as f:
            self.embeddings = np.load(f)

        with open(f"{self.folder}/index_to_id.json", "r") as f:
            self.index_to_id = json.load(f)

        self.faiss_index = faiss.read_index(f"{self.folder}/faiss.index")
