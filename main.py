from pathlib import Path

from app.loaders import load_document
from app.text_utils import clean_text
from app.chunking import chunk_text
from app.embeddings import create_simple_embedding
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


DOCUMENT_PATH = Path("documents/sop_oes.txt")
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 3
MINIMUM_RELEVANCE_SCORE = 4


def main():
    document_text = load_document(DOCUMENT_PATH)

    if document_text is None:
        print("Document not found.")
        return

    cleaned_text = clean_text(document_text)
    chunks = chunk_text(cleaned_text, CHUNK_SIZE, CHUNK_OVERLAP)
    
    chunk_embeddings = []

    for chunk in chunks:
        embedding = create_simple_embedding(chunk)
        chunk_embeddings.append(embedding)

    question = "What should I do if OES signal is unstable?"
    question_embedding = create_simple_embedding(question)

    ranked_chunks = rank_chunks_by_similarity(
        question_embedding,
        chunk_embeddings,
        chunks
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

    grounded_answer = create_grounded_answer(
        question,
        context,
        has_context,
        sources
    )

    best_index, best_chunk, best_score = find_best_chunk(
        question_embedding,
        chunk_embeddings,
        chunks
    )

    print("\n" + "=" * 60)
    print("RAG PIPELINE RESULT")
    print("=" * 60)

    print("\nDOCUMENT")
    print("-" * 60)
    print(f"Cleaned text length: {len(cleaned_text)} characters")
    print(f"Chunk size: {CHUNK_SIZE} characters")
    print(f"Chunk overlap: {CHUNK_OVERLAP} characters")
    print(f"Number of chunks: {len(chunks)}")

    print("\nQUESTION")
    print("-" * 60)
    print(question)
    print(f"Question embedding: {question_embedding}")

    print("\nCHUNK RANKING")
    print("-" * 60)
    for result in ranked_chunks:
        print(
            f"Chunk {result['chunk_index'] + 1}: "
            f"score {result['similarity_score']}"
        )

    print(f"\nTOP {TOP_K} CHUNKS")
    print("-" * 60)
    for result in top_chunks:
        chunk_number = result["chunk_index"] + 1
        score = result["similarity_score"]
        chunk_preview = result["chunk_text"][:220].replace("\n", " ")

        print(f"Chunk {chunk_number}: score {score}")
        print(f"Preview: {chunk_preview}...")
        print("")

    print("\nBEST CHUNK")
    print("-" * 60)
    print(f"Best chunk number: {best_index + 1}")
    print(f"Best similarity score: {best_score}")
    print(f"Preview: {best_chunk[:300].replace('\n', ' ')}...")

    print("\nRELEVANCE CHECK")
    print("-" * 60)
    print(f"Minimum relevance score: {MINIMUM_RELEVANCE_SCORE}")
    print(f"Has relevant context: {has_context}")

    print("\nSOURCES")
    print("-" * 60)
    print(sources)

    print("\nGROUNDED ANSWER")
    print("-" * 60)
    print(grounded_answer[:1000])
    print("=" * 60)

if __name__ == "__main__":
    main()