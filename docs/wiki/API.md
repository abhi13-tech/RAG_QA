API

Health
- GET /health

Ingest
- POST /ingest
  - Body: { "paths": ["optional/file/or/dir"] }

Index
- POST /index

Search
- POST /search
  - Body: { "query": "...", "top_k": 5 }
  - Res: { "hits": [ { text, source, score? } ] }

Q&A
- POST /qa
  - Body: { "query": "...", "top_k": 5 }
  - Res: { "answer": "...", "contexts": [...] }

Feedback
- POST /feedback
  - Body: { query, answer, helpful, comment? }

Example
- curl -X POST localhost:8000/search -H 'Content-Type: application/json' \
  -d '{"query":"What is FastAPI?","top_k":5}'

