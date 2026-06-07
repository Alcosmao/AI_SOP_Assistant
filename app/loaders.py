def load_document(file_path):
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def load_question(file_path):
    question_text = load_document(file_path)

    if question_text is None:
        return None

    question = question_text.strip()

    if not question:
        return None

    return question