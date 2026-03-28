import json
import numpy as np
from sentence_transformers import SentenceTransformer

class Librarian:
    _cache_embeddings = None  # class-level cache

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Load static ET data
        with open("et_data.json") as f:
            self.data = json.load(f)

        self.texts = [
            x["name"] + " " + x["description"]
            for x in self.data
        ]

        # Cache embeddings globally to avoid recomputation
        if Librarian._cache_embeddings is None:
            Librarian._cache_embeddings = self.model.encode(self.texts)

        self.embeddings = Librarian._cache_embeddings

    # ✅ This method MUST be here
    def search(self, query):
        query_vec = self.model.encode([query])[0]
        scores = np.dot(self.embeddings, query_vec)
        top_idx = np.argsort(scores)[-5:][::-1]
        return [self.data[i] for i in top_idx]