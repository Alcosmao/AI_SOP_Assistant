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


DOCUMENT_PATH = Path("documents/sop_oes.txt")
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 3


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

    best_index, best_chunk, best_score = find_best_chunk(
        question_embedding,
        chunk_embeddings,
        chunks
    )

    print("Document loaded successfully.")
    print("-----------------------------")
    print(f"Cleaned text lenght: {len(cleaned_text)} character")
    print(f"Chunk size: {CHUNK_SIZE} characters")
    print(f"Chunk overlap: {CHUNK_OVERLAP}")
    print("-----------------------------")
    print(f"Number of chunks: {len(chunks)}")
    print(f"Question: {question}")
    print(f"Question embedding: {question_embedding}")
    print("-----------------------------")
    print(f"Chunk ranking")
    for result in ranked_chunks:
        print(
            f"Chunk {result['chunk_index'] + 1} "
            f"score: {result['similarity_score']}"
        )
    print("-----------------------------")
    print(f"Top {TOP_K} chunks:")
    for result in top_chunks:
        print(
            f"Chunk {result['chunk_index'] + 1} "
            f"score: {result['similarity_score']}"
        )
        print(result["chunk_text"])
        print("-----------------------------")
    print(f"Best chunk number: {best_index + 1}")
    print(f"Best similarity score: {best_score}")
    print("-----------------------------")
    print("Best chunk:")
    print(best_chunk)
    print("-----------------------------")

if __name__ == "__main__":
    main()