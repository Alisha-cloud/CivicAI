import json
from src.classification import evaluate_classifier
if __name__ == "__main__":
    result = evaluate_classifier()
    print(json.dumps({"accuracy": result["accuracy"], "labels": result["labels"], "classification_report": result["classification_report"]}, indent=2))
