from app.checklist import is_numbered_step, generate_checklist_from_text
from app.validation import is_valid_checklist_item, validate_checklist_items


def test_is_numbered_step():
    assert is_numbered_step("1. Do something") is True
    assert is_numbered_step("hello") is False
    assert is_numbered_step("1") is False


def test_generate_checklist_only_keeps_numbered_lines():
    text = "1. First step\n2. Second step\nthis is not a step"
    items = generate_checklist_from_text(text)

    assert items == ["[ ] First step", "[ ] Second step"]


def test_valid_checklist_item_rules():
    assert is_valid_checklist_item("[ ] Inspect the fiber connector.") is True
    # too short (less than 15 chars of step text)
    assert is_valid_checklist_item("[ ] short.") is False
    # missing trailing period
    assert is_valid_checklist_item("[ ] This has no period") is False


def test_validate_removes_duplicates():
    items = [
        "[ ] Inspect the fiber connector.",
        "[ ] Inspect the fiber connector.",
    ]
    assert validate_checklist_items(items) == ["[ ] Inspect the fiber connector."]
