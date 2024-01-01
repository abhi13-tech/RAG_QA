import requests
from app.core.config import settings

def openrouter_answer(query: str, context: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
    }
    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Use the context to answer. Context:\n{context}\n\nQuestion: {query}"},
        ],
        "temperature": 0.2,
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenRouter error] {e}"

