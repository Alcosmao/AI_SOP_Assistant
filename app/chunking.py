def chunk_text(text, chunk_size, chunk_overlap):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    
    chunks = []
    start_index = 0

    step = chunk_size - chunk_overlap

    while start_index < len(text):
        end_index = start_index + chunk_size
        chunk = text[start_index:end_index]

        if chunk.strip():
            chunks.append(chunk)

        start_index = start_index + step

    return chunks