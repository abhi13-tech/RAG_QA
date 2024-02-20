Quickstart

Local (Python 3.10+)
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- make ingest index
- make api  (browse http://localhost:8000/docs)
- make ui   (browse http://localhost:8501)

Docker Compose
- docker compose up --build
- Uses Qdrant, API, UI with sensible defaults.

Sample data
- Example docs in data/raw/sample/
- Baseline: make sample-baseline

