FAQ

Does this work offline?
- Yes. It falls back to lightweight local embeddings and skips heavy reranking.

Which vector DB should I use?
- Start with FAISS locally. Use Qdrant via Docker Compose for durability and remote access.

How do I switch LLMs?
- Set LLM_MODE=local|litellm|openrouter and configure env vars (see Configuration page).

How do I add my own docs?
- Drop files into data/raw/ and run make ingest index.

\n- Synced via CI at 2025-09-18T16:12:36Z
