from fastapi import APIRouter
from fastapi import Body
from app.models.schemas import IngestRequest, SearchRequest, QARequest, FeedbackRequest
from app.ingest.pipeline import run_ingest
from app.index.build import build_index, get_index
from app.llm.generator import answer_question
from app.storage.feedback_repo import save_feedback
from app.retrieval.reranker import rerank_hits

router = APIRouter()

@router.post("/ingest")
def ingest(req: IngestRequest):
    count = run_ingest(paths=req.paths)
    return {"processed": count}

@router.post("/index")
def index():
    n = build_index()
    return {"indexed": n}

@router.post("/search")
def search(req: SearchRequest):
    idx = get_index()
    hits = idx.search(req.query, top_k=req.top_k)
    hits = rerank_hits(req.query, hits)
    return {"hits": hits}

@router.post("/qa")
def qa(req: QARequest):
    idx = get_index()
    hits = idx.search(req.query, top_k=req.top_k)
    hits = rerank_hits(req.query, hits)
    answer = answer_question(req.query, hits)
    return {"answer": answer, "contexts": hits}

@router.post("/feedback")
def feedback(req: FeedbackRequest):
    save_feedback(req)
    return {"ok": True}
