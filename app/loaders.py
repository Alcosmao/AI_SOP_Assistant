def load_document(file_path):
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return