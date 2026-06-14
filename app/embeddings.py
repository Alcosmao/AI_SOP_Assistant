# LEGACY - kept for learning, NOT used in the pipeline.
# This was my first naive "embedding": it just counts a few fixed keywords.
# The project now uses real semantic embeddings in app/openai_embeddings.py,
# which understand meaning (1536 numbers) instead of counting exact words.

KEYWORDS = [
    "oes",
    "signal",
    "fiber",
    "alarm",
    "safety",
    "test",
]


def create_simple_embedding(text):
    text_lower = text.lower()

    embedding = []

    for keyword in KEYWORDS:
        count = text_lower.count(keyword)
        embedding.append(count)

    return embedding