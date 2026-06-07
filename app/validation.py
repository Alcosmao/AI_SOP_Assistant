def is_valid_checklist_item(item):
    cleaned_item = item.strip()

    if not cleaned_item.startswith("[ ] "):
        return False

    step_text = cleaned_item.replace("[ ] ", "", 1).strip()

    if len(step_text) < 15:
        return False

    if not step_text.endswith("."):
        return False

    return True


def remove_duplicate_items(items):
    unique_items = []
    seen_items = set()

    for item in items:
        normalized_item = item.lower().strip()

        if normalized_item not in seen_items:
            unique_items.append(item)
            seen_items.add(normalized_item)

    return unique_items


def validate_checklist_items(items):
    valid_items = []

    for item in items:
        if is_valid_checklist_item(item):
            valid_items.append(item)

    unique_valid_items = remove_duplicate_items(valid_items)

    return unique_valid_items