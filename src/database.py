import json
import sqlite3
import uuid
from datetime import datetime, timezone
from src.config import DB_PATH

def connect():
    conn = sqlite3.connect(DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            original_text TEXT NOT NULL,
            normalized_text TEXT,
            tokens_json TEXT,
            category TEXT,
            class_scores_json TEXT,
            urgency TEXT,
            urgency_reason TEXT,
            department TEXT,
            entities_json TEXT,
            summary TEXT,
            classification_method TEXT,
            summary_method TEXT,
            status TEXT NOT NULL DEFAULT 'AI_ANALYZED',
            created_at TEXT NOT NULL,
            similar_count INTEGER DEFAULT 0
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_complaints_category ON complaints(category)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_complaints_urgency ON complaints(urgency)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_complaints_created_at ON complaints(created_at)")

def save_complaint(result: dict) -> str:
    complaint_id = result.get("complaint_id") or str(uuid.uuid4())
    created_at = result.get("created_at") or datetime.now(timezone.utc).isoformat()
    with connect() as conn:
        conn.execute("""
        INSERT INTO complaints (
            complaint_id, original_text, normalized_text, tokens_json, category,
            class_scores_json, urgency, urgency_reason, department, entities_json,
            summary, classification_method, summary_method, status, created_at, similar_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            complaint_id, result["original_text"], result["normalized_text"],
            json.dumps(result["tokens"]), result["category"], json.dumps(result["class_scores"]),
            result["urgency"], result["urgency_reason"], result["department"],
            json.dumps(result["entities"]), result["summary"], result["classification_method"],
            result["summary_method"], result.get("status", "AI_ANALYZED"), created_at,
            len(result.get("similar_complaints", []))
        ))
    return complaint_id

def _row_to_dict(row):
    item = dict(row)
    for key in ("tokens_json", "class_scores_json", "entities_json"):
        raw = item.pop(key, None)
        dest = {"tokens_json":"tokens", "class_scores_json":"class_scores", "entities_json":"entities"}[key]
        item[dest] = json.loads(raw) if raw else []
    return item

def list_complaints(limit=500):
    with connect() as conn:
        rows = conn.execute("SELECT * FROM complaints ORDER BY created_at DESC LIMIT ?", (int(limit),)).fetchall()
    return [_row_to_dict(r) for r in rows]

def get_complaint(complaint_id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM complaints WHERE complaint_id=?", (complaint_id,)).fetchone()
    return _row_to_dict(row) if row else None

def update_status(complaint_id, status):
    allowed = {"SUBMITTED","AI_ANALYZED","ASSIGNED","IN_PROGRESS","RESOLVED","CLOSED","REOPENED"}
    if status not in allowed:
        raise ValueError("Invalid status")
    with connect() as conn:
        conn.execute("UPDATE complaints SET status=? WHERE complaint_id=?", (status, complaint_id))
