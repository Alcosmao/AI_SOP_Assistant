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