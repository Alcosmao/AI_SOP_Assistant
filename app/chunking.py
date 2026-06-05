def chunk_text(text, chunk_size):
    chunks = []
    start_index = 0

    while start_index < len(text):
        end_index = start_index + chunk_size
        chunk = text[start_index:end_index]

        if chunk.strip():
            chunks.append(chunk)

        start_index = end_index
    
    return chunks