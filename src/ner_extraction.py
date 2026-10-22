import re
from typing import List, Dict

PATTERNS = [
    ("LOCATION", re.compile(r"\b(?:Ward\s+\d+[A-Za-z]?|[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}(?: Nagar| Colony| Road| Street| Layout| Area))\b")),
    ("DURATION", re.compile(r"\b(?:for\s+)?(?:the\s+last\s+)?\d+\s+(?:hours?|days?|weeks?|months?|years?)\b", re.I)),
    ("DURATION", re.compile(r"\b(?:for\s+)?(?:the\s+last\s+)?(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:hours?|days?|weeks?|months?|years?)\b", re.I)),
    ("QUANTITY_AFFECTED", re.compile(r"\b(?:around\s+)?\d+\s+(?:families|people|households|residents|homes|buildings)\b", re.I)),
    ("SERVICE", re.compile(r"\b(?:water supply|water tanker|electricity|street lights?|garbage collection|sewage|road|public transport|bus service|hospital|drainage)\b", re.I)),
    ("DATE_OR_TIME", re.compile(r"\b(?:today|yesterday|last night|since Monday|since Tuesday|since Wednesday|since Thursday|since Friday|since Saturday|since Sunday|this week)\b", re.I)),
]

def extract_entities(text: str) -> List[Dict[str, str]]:
    found = []
    seen = set()
    for label, pattern in PATTERNS:
        for match in pattern.finditer(text):
            value = match.group(0).strip()
            key = (label, value.lower())
            if key not in seen:
                found.append({"label": label, "value": value, "method": "pattern"})
                seen.add(key)
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in {"GPE", "LOC", "FAC"}:
                label = "LOCATION"
            elif ent.label_ in {"DATE", "TIME"}:
                label = "DATE_OR_TIME"
            elif ent.label_ in {"ORG"}:
                label = "ORGANIZATION"
            elif ent.label_ in {"PERSON"}:
                label = "PERSON"
            else:
                continue
            key = (label, ent.text.lower())
            if key not in seen:
                found.append({"label": label, "value": ent.text, "method": "spaCy"})
                seen.add(key)
    except (ImportError, OSError):
        pass
    return found
