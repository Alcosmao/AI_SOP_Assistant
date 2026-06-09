from pathlib import Path
from app.loaders import load_document
from app.text_utils import clean_text
from app.chunking import chunk_text
from app.openai_embeddings import create_openai_embeddings
from app.retrieval import (
    find_best_chunk,
    rank_chunks_by_similarity,
    get_top_k_chunks,
)
from app.answering import (
    build_context,
    build_source_list,
    create_grounded_answer,
)
from app.checklist import generate_checklist_from_text
from app.validation import validate_checklist_items
from app.export import save_checklist_to_txt


DOCUMENT_PATH = Path("documents/sop_oes.txt")
REPORTS_PATH = Path("reports")
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 5
MINIMUM_RELEVANCE_SCORE = 0.65

def run_rag_pipeline(question: str, documenth_path: Path = DOCUMENT_PATH):
    document_text = load_document(documenth_path)

    if document_text is None:
        raise FileNotFoundError(f"Document not found: {documenth_path}")
    
    cleaned_text = clean_text(document_text)
    chunks = chunk_text(cleaned_text, CHUNK_SIZE, CHUNK_OVERLAP)

    chunk_embeddings = []
    for chunk in chunks:
        embedding = create_openai_embeddings(chunk)
        chunk_embeddings.append(embedding)

    question_embedding = create_openai_embeddings(question)

    ranked_chunks = rank_chunks_by_similarity(
        question_embedding,
        chunk_embeddings,
        chunks,
    )

    top_chunks = get_top_k_chunks(
        question_embedding,
        chunk_embeddings,
        chunks,
        TOP_K
    )

    relevant_chunks = [
        chunk for chunk in top_chunks
        if chunk["similarity_score"] >= MINIMUM_RELEVANCE_SCORE
    ]

    has_context = len(relevant_chunks) > 0
    context = build_context(relevant_chunks)
    sources = build_source_list(relevant_chunks)

    if has_context:
        checklist_items = generate_checklist_from_text(context)
        validated_checklist_items = validate_checklist_items(checklist_items)
    else:
        checklist_items = []
        validated_checklist_items = []

    checklist_file_path = save_checklist_to_txt(
        validated_checklist_items,
        REPORTS_PATH
    )

    grounded_answer = create_grounded_answer(
        question,
        context,
        has_context,
        sources,
    )

    best_index, best_chunk, best_score = find_best_chunk(
        question_embedding,
        chunk_embeddings,
        chunks,
    )
    return {
        "question": question,
        "answer": grounded_answer,
        "sources": sources,
        "has_context": has_context,
        "relevant_chunks": relevant_chunks,
        "top_chunks": top_chunks,
        "ranked_chunks": ranked_chunks,
        "checklist_items": checklist_items,
        "validated_checklist_items": validated_checklist_items,
        "checklist_file_path": checklist_file_path,
        "cleaned_text_length": len(cleaned_text),
        "chunks_count": len(chunks),
        "question_embedding_length": len(question_embedding),
        "best_chunk_index": best_index,
        "best_chunk_text": best_chunk,
        "best_score": best_score,        
    }
