from app.text_utils import clean_text


def test_clean_text_removes_empty_lines_and_trims():
    raw = "a\n\n   b   \n\nc"
    assert clean_text(raw) == "a\nb\nc"


def test_clean_text_on_empty_string():
    assert clean_text("") == ""
