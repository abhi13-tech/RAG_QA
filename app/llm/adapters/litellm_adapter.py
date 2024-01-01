import os
import requests
from app.core.config import settings

def litellm_answer(query: str, context: str) -> str:
    # Placeholder: calls LiteLLM proxy if configured by user.
    url = os.getenv("LITELLM_BASE", "http://localhost:4000/v1/chat/completions")
    model = settings.LITELLM_MODEL
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Answer using context. Context:\n{context}\n\nQuestion: {query}"},
        ],
        "temperature": 0.2,
    }
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[LiteLLM error] {e}"

