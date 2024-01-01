.PHONY: api ui ingest index eval clean sample-baseline

api:
	uvicorn app.main:app --reload --port 8000

ui:
	API_BASE=http://localhost:8000 streamlit run ui/app.py

ingest:
	python -m app.ingest.pipeline

index:
	python -m app.index.build

eval:
	python -m app.eval.harness

sample-baseline:
	INDEX_BACKEND=faiss python -m app.ingest.pipeline && python -m app.index.build && python -m app.eval.harness

clean:
	rm -rf index/faiss/* data/processed/*
