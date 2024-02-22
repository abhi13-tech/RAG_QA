Troubleshooting

No results returned
- Ensure you ran make ingest and make index
- Check that data/processed/chunks.jsonl exists and is non-empty

Qdrant errors
- In Compose, QDRANT_URL should be http://qdrant:6333
- The collection is created if missing; rebuild indexes with make index

Models won’t download
- Offline fallback is used automatically (hash embeddings, no-op reranker)
- When online, set EMBEDDING_MODEL/RERANKER_MODEL and retry

LLM errors
- Local mode avoids network calls; switch to litellm/openrouter only with valid credentials

