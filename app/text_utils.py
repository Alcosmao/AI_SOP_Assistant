def clean_text(text):
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        cleaned_line = line.strip()

        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    return "\n".join(cleaned_lines)