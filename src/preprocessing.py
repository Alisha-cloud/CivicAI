import re
from typing import Dict, List

TOKEN_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Complaint text must be a string.")
    return re.sub(r"\s+", " ", text).strip()

def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(normalize_text(text).lower())

def preprocess(text: str) -> Dict[str, object]:
    normalized = normalize_text(text)
    return {"normalized_text": normalized, "tokens": tokenize(normalized)}
