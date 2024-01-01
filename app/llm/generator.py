from typing import List, Dict
from app.core.config import settings
from app.llm.adapters.local_stub import local_answer
from app.llm.adapters.litellm_adapter import litellm_answer
from app.llm.adapters.openrouter_adapter import openrouter_answer

def answer_question(query: str, contexts: List[Dict]) -> str:
    ctx_text = "\n\n".join([c.get("text", "") for c in contexts])
    mode = settings.LLM_MODE.lower()
    if mode == "litellm":
        return litellm_answer(query, ctx_text)
    if mode == "openrouter":
        return openrouter_answer(query, ctx_text)
    return local_answer(query, ctx_text)

