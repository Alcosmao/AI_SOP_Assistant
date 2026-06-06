def calculate_similarity(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have same lenght")

    score = 0

    for index in range(len(vector_a)):
        score = score + vector_a[index] * vector_b[index]

    return score


def rank_chunks_by_similarity(question_embedding, chunk_embeddings, chunks):
    ranked_chunks = []

    for index, chunk_embedding in enumerate(chunk_embeddings):
        score = calculate_similarity(question_embedding, chunk_embedding)

        ranked_chunks.append({
            "chunk_index": index,
            "chunk_text": chunks[index],
            "similarity_score": score
        })

    ranked_chunks.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    return ranked_chunks

def find_best_chunk(question_embedding, chunk_embeddings, chunks):
    ranked_chunks = rank_chunks_by_similarity(
        question_embedding,
        chunk_embeddings,
        chunks
    )

    if not ranked_chunks:
        return None, None, 0
    
    best_result = ranked_chunks[0]

    return (
        best_result["chunk_index"],
        best_result["chunk_text"],
        best_result["similarity_score"]
    )


def get_top_k_chunks(question_embodding, chunk_embeddings, chunks, top_k):
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")
    
    ranked_chunks = rank_chunks_by_similarity(
        question_embodding,
        chunk_embeddings,
        chunks
    )

    return ranked_chunks[:top_k]