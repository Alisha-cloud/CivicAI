from src.preprocessing import preprocess
from src.classification import classify
from src.ner_extraction import extract_entities
from src.urgency_detection import detect_urgency
from src.department_routing import route_department
from src.summarization import summarize
from src.database import list_complaints, save_complaint
from src.similarity import find_similar

def analyze_complaint(text: str, persist: bool = True) -> dict:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Complaint text must not be empty.")
    prep = preprocess(text)
    classification = classify(text)
    entities = extract_entities(text)
    urgency = detect_urgency(text)
    department = route_department(classification["category"])
    summary = summarize(text)
    prior = list_complaints(limit=1000)
    similar = find_similar(text, prior, threshold=0.15, top_k=5)
    result = {
        "complaint_id": None,
        "original_text": text.strip(),
        "normalized_text": prep["normalized_text"],
        "tokens": prep["tokens"],
        "category": classification["category"],
        "class_scores": classification["class_scores"],
        "classification_method": classification["classification_method"],
        "entities": entities,
        "urgency": urgency["urgency"],
        "urgency_reason": urgency["reason"],
        "urgency_method": urgency["method"],
        "department": department,
        "summary": summary["summary"],
        "summary_method": summary["summary_method"],
        "similar_complaints": similar,
        "status": "AI_ANALYZED"
    }
    if persist:
        result["complaint_id"] = save_complaint(result)
    return result
