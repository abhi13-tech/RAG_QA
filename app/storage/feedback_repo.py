from pathlib import Path
from app.models.schemas import FeedbackRequest
import json

_PATH = Path("data/feedback.jsonl")

def save_feedback(req: FeedbackRequest):
    _PATH.parent.mkdir(parents=True, exist_ok=True)
    with _PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(req.model_dump()) + "\n")

