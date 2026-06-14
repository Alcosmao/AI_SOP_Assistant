from fastapi import FastAPI, HTTPException

from app.schemas import AskRequest, AskResponse
from app.pipeline import run_rag_pipeline
from app.storage.factory import get_storage

app = FastAPI(
    title="SOP RAG API",
    description="RAG API for SOP document Q&A",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/documents")
def list_documents():
    storage = get_storage()
    return {"documents": storage.list_documents()}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )
    try:
        result = run_rag_pipeline(question, request.document_name)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="SOP document not found on the server.",
        )

    return AskResponse(
        question=result["question"],
        has_context=result["has_context"],
        answer=result["answer"],
        sources=result["sources"],
        checklist=result["validated_checklist_items"],
    )