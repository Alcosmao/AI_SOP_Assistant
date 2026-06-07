def is_numbered_step(line):
    line = line.strip()

    if len(line) < 3:
        return False
    
    first_character = line[0]
    second_character = line[1]

    return first_character.isdigit() and second_character == "."

def remove_step_number(line):
    return line.split(".",1)[1].strip()


def generate_checlist_from_text(text):
    checklist_items = []

    lines = text.splitlines()

    for line in lines:
        cleaned_line = line.strip()

        if is_numbered_step(cleaned_line):
            step_text = remove_step_number(cleaned_line)
            checklist_item = f"[ ] {step_text}"
            checklist_items.append(checklist_item)

    return checklist_items