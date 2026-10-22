from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from src.config import DATA_DIR, MODEL_DIR

MODEL_PATH = MODEL_DIR / "tfidf_logreg.joblib"
TEXT_COL = "complaint_text"
LABEL_COL = "category"

def load_dataset() -> pd.DataFrame:
    path = DATA_DIR / "sample_complaints.csv"
    df = pd.read_csv(path)
    df = df.dropna(subset=[TEXT_COL, LABEL_COL])
    return df

def train_classifier(force: bool = False):
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    if MODEL_PATH.exists() and not force:
        return joblib.load(MODEL_PATH)
    df = load_dataset()
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1, strip_accents="unicode")),
        ("clf", LogisticRegression(max_iter=1500, class_weight="balanced", random_state=42))
    ])
    model.fit(df[TEXT_COL].astype(str), df[LABEL_COL].astype(str))
    joblib.dump(model, MODEL_PATH)
    return model

def load_classifier():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train_classifier()

def classify(text: str) -> dict:
    model = load_classifier()
    category = str(model.predict([text])[0])
    scores = {}
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba([text])[0]
        scores = {str(label): float(prob) for label, prob in zip(model.classes_, probs)}
    return {"category": category, "class_scores": scores, "classification_method": "TF-IDF + Logistic Regression (synthetic demo dataset)"}

def evaluate_classifier() -> dict:
    df = load_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        df[TEXT_COL].astype(str), df[LABEL_COL].astype(str),
        test_size=0.25, random_state=42, stratify=df[LABEL_COL].astype(str)
    )
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1, strip_accents="unicode")),
        ("clf", LogisticRegression(max_iter=1500, class_weight="balanced", random_state=42))
    ])
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    labels = sorted(df[LABEL_COL].unique().tolist())
    return {
        "accuracy": float(accuracy_score(y_test, pred)),
        "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, pred, labels=labels).tolist(),
        "labels": labels
    }
