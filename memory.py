

import os, json
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict

MODEL = "all-MiniLM-L6-v2"
DIM = 384

class Memory:
    def __init__(self, index_path="data/memory_index"):
        self.embed = SentenceTransformer(MODEL)
        self.index_path = index_path
        os.makedirs(index_path, exist_ok=True)
        self.index_file = os.path.join(index_path, "faiss.index")
        self.meta_file = os.path.join(index_path, "meta.json")
        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(DIM)
            self.meta = []

    def add(self, text: str, meta: Dict):
        vec = self.embed.encode([text])[0].astype("float32")
        self.index.add(vec.reshape(1, -1))
        self.meta.append({"text": text, **meta})
        self._save()

    def retrieve(self, query: str, k=4) -> List[Dict]:
        if self.index.ntotal == 0:
            return []
        qv = self.embed.encode([query])[0].astype("float32")
        k = min(k, max(1, self.index.ntotal))
        D, I = self.index.search(qv.reshape(1, -1), k)
        return [self.meta[i] for i in I[0].tolist() if i < len(self.meta)]

    def _save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)
