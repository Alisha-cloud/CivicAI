from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar(query: str, rows: List[dict], exclude_id=None, threshold: float = 0.15, top_k: int = 5) -> List[Dict]:
    candidates = [r for r in rows if r.get("complaint_id") != exclude_id and r.get("original_text")]
    if not query.strip() or not candidates:
        return []
    texts = [query] + [r["original_text"] for r in candidates]
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        embeddings = model.encode(texts, normalize_embeddings=True)
        scores = np.dot(embeddings[1:], embeddings[0])
        method = "Sentence Transformers"
    except Exception:
        vectorizer = TfidfVectorizer(ngram_range=(1,2))
        matrix = vectorizer.fit_transform(texts)
        scores = cosine_similarity(matrix[1:], matrix[0]).ravel()
        method = "TF-IDF similarity fallback"
    results = []
    for row, score in zip(candidates, scores):
        if float(score) >= threshold:
            results.append({
                "complaint_id": row["complaint_id"],
                "category": row["category"],
                "urgency": row["urgency"],
                "department": row["department"],
                "similarity": round(float(score), 3),
                "method": method,
                "text": row["original_text"][:240]
            })
    return sorted(results, key=lambda x: x["similarity"], reverse=True)[:top_k]
