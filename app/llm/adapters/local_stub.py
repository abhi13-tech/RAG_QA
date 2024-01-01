def local_answer(query: str, context: str) -> str:
    snippet = context[:300].replace("\n", " ")
    return f"[LOCAL MODE]\nQ: {query}\nA: Based on indexed context: {snippet} ..."

