import re

CRITICAL_PATTERNS = [
    r"\b(life[- ]threatening|electrocution|live wire|building collapse|major fire|gas leak|contaminated drinking water|severe flooding|immediate danger|people trapped)\b",
]
HIGH_PATTERNS = [
    r"\b(no water|water supply stopped|power outage|no electricity|overflowing sewage|major pothole|multiple families|many residents|hospital emergency)\b",
]
MEDIUM_PATTERNS = [
    r"\b(not working|broken|leaking|missed collection|damaged|for \d+ days|for the last \d+ days)\b",
]

def detect_urgency(text: str) -> dict:
    low = text.lower()
    if any(re.search(p, low) for p in CRITICAL_PATTERNS):
        return {"urgency": "CRITICAL", "reason": "Potential immediate public-safety risk indicator detected.", "method": "rules"}
    if any(re.search(p, low) for p in HIGH_PATTERNS):
        return {"urgency": "HIGH", "reason": "Significant service disruption or broad impact indicator detected.", "method": "rules"}
    if any(re.search(p, low) for p in MEDIUM_PATTERNS):
        return {"urgency": "MEDIUM", "reason": "Service fault or ongoing issue indicator detected.", "method": "rules"}
    return {"urgency": "LOW", "reason": "No configured high-priority indicators detected; human review may change this estimate.", "method": "rules"}
