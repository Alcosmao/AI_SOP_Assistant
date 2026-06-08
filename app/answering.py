from app.openai_answer import create_openai_answer

def build_context(top_chunks):
    context_parts = []

    for result in top_chunks:
        chunk_number = result["chunk_index"] + 1
        score = result["similarity_score"]
        chunk_text = result["chunk_text"]

        context_part = (
            f"Source chunk {chunk_number} "
            f"(similarity score: {score})\n"
            f"{chunk_text}"
        )

        context_parts.append(context_part)

    return "\n\n".join(context_parts)


def build_source_list(top_chunks):
    source_lines = []

    for result in top_chunks:
        chunk_number = result["chunk_index"] + 1
        score = result["similarity_score"]

        source_lines.append(
            f"- [Source chunk {chunk_number}] similarity score: {score}"
        )

    return "\n".join(source_lines)


def create_grounded_answer(question, context, has_context, sources):
    if not has_context:
        return (
            "I don't know based on the provided document. "
            "The retrieved context does not contain enough relevant information."            
        )

    answer = create_openai_answer(question, context, sources)
    
    return answer