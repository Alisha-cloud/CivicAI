# CivicAI — NLP Grievance Classification and Routing

CivicAI is a runnable academic NLP mini project that analyzes citizen grievances. It demonstrates text normalization/tokenization, TF-IDF + Logistic Regression classification, pattern-based entity extraction, urgency estimation, department routing, extractive summarization, optional Gemini summarization, similarity matching, SQLite persistence, and evaluation.

> **Dataset note:** `data/sample_complaints.csv` contains synthetic examples for software demonstration. Metrics from it are not evidence of real-world performance.

## Requirements
- Python 3.10–3.12 recommended
- Internet connection only for installing dependencies or optional external models/API calls

## Windows setup (PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/seed_data.py
python scripts/train_classifier.py
streamlit run app.py
```
If PowerShell blocks activation, run `.venv\Scripts\activate.bat` from Command Prompt instead.

## macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/seed_data.py
python scripts/train_classifier.py
streamlit run app.py
```

## Optional Gemini summarization
Set `GEMINI_API_KEY` in your shell or create a local `.env` file based on `.env.example`. For automatic `.env` loading, add `from dotenv import load_dotenv; load_dotenv()` near the start of `src/config.py`. Never commit secrets. Without a key, the app uses an extractive fallback.

## Optional spaCy NER
```bash
pip install spacy
python -m spacy download en_core_web_sm
```
The application still runs with pattern-based extraction if the model is unavailable.

## Optional semantic embeddings
```bash
pip install sentence-transformers
```
The first model use may download a pretrained embedding model. Without it, the app uses TF-IDF cosine similarity.

## Evaluate and test
```bash
python scripts/evaluate_classifier.py
pytest -q
```

## CSV format
Batch analysis requires a column named `complaint_text`. For training, the included dataset uses `complaint_text` and `category`.

## Main workflow
Complaint text → preprocessing → TF-IDF classifier → entity extraction → urgency estimate → department recommendation → summary → similarity matching → SQLite storage.

## Important limitations
- The starter dataset is synthetic and intentionally small.
- Urgency detection uses transparent heuristic rules and needs human review.
- Pattern-based NER is not a substitute for a domain-trained entity model.
- TF-IDF classification will not generalize reliably without a larger, representative, independently labelled dataset.
- Similarity results are potential matches, not proof of duplicate incidents.
- Gemini and optional model integrations may require internet access and credentials.
