import pytest
from src.preprocessing import normalize_text, tokenize
from src.department_routing import route_department
from src.urgency_detection import detect_urgency
from src.ner_extraction import extract_entities

def test_normalize_text():
    assert normalize_text("  no   water \n supply ") == "no water supply"

def test_tokenize():
    assert "water" in tokenize("Water supply is stopped.")

def test_department_mapping():
    assert route_department("Water Supply") == "Water Supply Department"

def test_urgency_critical():
    assert detect_urgency("There is a live wire on the road.")["urgency"] == "CRITICAL"

def test_entity_duration():
    entities = extract_entities("Water supply has stopped for five days in Ward 14.")
    assert any(e["label"] == "DURATION" for e in entities)
    assert any(e["label"] == "LOCATION" for e in entities)

def test_empty_text_rejected():
    from src.pipeline import analyze_complaint
    with pytest.raises(ValueError):
        analyze_complaint("   ", persist=False)
