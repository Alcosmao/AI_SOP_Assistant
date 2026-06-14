from pathlib import Path
from app.loaders import load_question
from app.pipeline import run_rag_pipeline, TOP_K, MINIMUM_RELEVANCE_SCORE, CHUNK_SIZE, CHUNK_OVERLAP

QUESTION_PATH = Path("input/question.txt")

def main():
    question = load_question(QUESTION_PATH)
    DOCUMENT_NAME = "sop_oes.txt"

    if question is None:
        print("Question file not found or emtpy")
        print(f"Createa a file at: {QUESTION_PATH}")
        return
    try:
        result = run_rag_pipeline(question, DOCUMENT_NAME)
    except FileNotFoundError as error:
        print(error)
        return
    
    print("\n" + "=" * 60)
    print("RAG PIPELINE RESULT")
    print("=" * 60)
    print("\nDOCUMENT")
    print("-" * 60)
    print(f"Cleaned text length: {result['cleaned_text_length']} characters")
    print(f"Chunk size: {CHUNK_SIZE} characters")
    print(f"Chunk overlap: {CHUNK_OVERLAP} characters")
    print(f"Number of chunks: {result['chunks_count']}")
    print("\nQUESTION")
    print("-" * 60)
    print(f"Question file: {QUESTION_PATH}")
    print(result["question"])
    print(f"Question embedding length: {result['question_embedding_length']}")
    print("\nCHUNK RANKING")
    print("-" * 60)
    for item in result["ranked_chunks"]:
        print(
            f"Chunk {item['chunk_index'] + 1}: "
            f"score {item['similarity_score']}"
        )
    print(f"\nTOP {TOP_K} CHUNKS")
    print("-" * 60)
    for item in result["top_chunks"]:
        chunk_number = item["chunk_index"] + 1
        score = item["similarity_score"]
        chunk_preview = item["chunk_text"][:220].replace("\n", " ")
        print(f"Chunk {chunk_number}: score {score}")
        print(f"Preview: {chunk_preview}...")
        print("")
    print("\nBEST CHUNK")
    print("-" * 60)
    print(f"Best chunk number: {result['best_chunk_index'] + 1}")
    print(f"Best similarity score: {result['best_score']}")
    print(f"Preview: {result['best_chunk_text'][:300].replace(chr(10), ' ')}...")
    print("\nRELEVANCE CHECK")
    print("-" * 60)
    print(f"Minimum relevance score: {MINIMUM_RELEVANCE_SCORE}")
    print(f"Has relevant context: {result['has_context']}")
    print("\nSOURCES")
    print("-" * 60)
    print(result["sources"])
    print("\nCHECKLIST")
    print("-" * 60)
    print(f"Raw checklist items: {len(result['checklist_items'])}")
    print(f"Validated checklist items: {len(result['validated_checklist_items'])}")
    print("")
    if result["validated_checklist_items"]:
        for item in result["validated_checklist_items"]:
            print(item)
    else:
        print("No valid checklist items found in the relevant context.")
    print("")
    if result["checklist_file_path"]:
        print(f"Checklist saved to: {result['checklist_file_path']}")
    else:
        print("Checklist file not created (no valid items to save).")
    print("\nGROUNDED ANSWER")
    print("-" * 60)
    print(result["answer"][:1000])
    print("=" * 60)
if __name__ == "__main__":
    main()   