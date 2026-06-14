def is_numbered_step(line):
    line = line.strip()

    if "." not in line:
        return False
    before_dot = line.split(".", 1)[0]
    
    return before_dot.isdigit()

def remove_step_number(line):
    return line.split(".",1)[1].strip()


def generate_checklist_from_text(text):
    checklist_items = []

    lines = text.splitlines()

    for line in lines:
        cleaned_line = line.strip()

        if is_numbered_step(cleaned_line):
            step_text = remove_step_number(cleaned_line)
            checklist_item = f"[ ] {step_text}"
            checklist_items.append(checklist_item)

    return checklist_items