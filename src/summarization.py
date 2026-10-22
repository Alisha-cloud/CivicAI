import re
from src.config import GEMINI_API_KEY, GEMINI_MODEL

def summarize(text: str) -> dict:
    if GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=(
                    "Summarize this citizen grievance in one concise, factual sentence. "
                    "Do not invent details. Return only the summary.\n\nComplaint:\n" + text
                ),
            )
            summary = (getattr(response, "text", "") or "").strip()
            if summary:
                return {"summary": summary, "summary_method": f"Gemini ({GEMINI_MODEL})"}
        except Exception:
            pass
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    summary = sentences[0] if sentences and sentences[0] else text.strip()
    words = summary.split()
    if len(words) > 32:
        summary = " ".join(words[:32]) + "…"
    return {"summary": summary or "No summary available.", "summary_method": "Extractive fallback"}
