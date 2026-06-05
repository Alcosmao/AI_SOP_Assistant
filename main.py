from pathlib import Path

from app.loaders import load_documents
from app.text_utils import clean_text
from app.chunking import chunk_text


DOCUMENT_PATH = Path("documents/sop_oes.txt")
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


def main():
    document_text = load_documents(DOCUMENT_PATH)

    if document_text is None:
        print("Document not found.")
        return

    cleaned_text = clean_text(document_text)
    chunks = chunk_text(cleaned_text, CHUNK_SIZE, CHUNK_OVERLAP)


    print("Document loaded successfully.")
    print("-----------------------------")
    print(f"Cleaned text lenght: {len(cleaned_text)} character")
    print(f"Chunk size: {CHUNK_SIZE} characters")
    print(f"Chunk overlap: {CHUNK_OVERLAP}")
    print(f"Number of chunks: {len(chunks)}")
    print("-----------------------------")

    for index, chunk in enumerate(chunks, start=1):
        print(f"Chunk {index}")
        print(chunk)
        print(f"Chunk lenght: {len(chunk)} characters")
        print("-----------------------------")

if __name__ == "__main__":
    main()