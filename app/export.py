def save_checklist_to_txt(checklist_items, reports_folder):
    if not checklist_items:
        return None

    reports_folder.mkdir(parents=True, exist_ok=True)

    file_path = reports_folder / "checklist.txt"
    checklist_text = "\n".join(checklist_items)
    file_path.write_text(checklist_text, encoding="utf-8")

    return file_path
