import pytest

from app.chunking import chunk_text


def test_chunking_splits_with_overlap():
    text = "0123456789"
    chunks = chunk_text(text, chunk_size=5, chunk_overlap=2)

    assert chunks[0] == "01234"
    assert chunks[1] == "34567"
    assert len(chunks) == 4


def test_chunking_skips_empty_chunks():
    chunks = chunk_text("   ", chunk_size=2, chunk_overlap=0)
    assert chunks == []


def test_chunk_size_must_be_positive():
    with pytest.raises(ValueError):
        chunk_text("abc", chunk_size=0, chunk_overlap=0)


def test_overlap_cannot_be_negative():
    with pytest.raises(ValueError):
        chunk_text("abc", chunk_size=3, chunk_overlap=-1)


def test_overlap_must_be_smaller_than_size():
    with pytest.raises(ValueError):
        chunk_text("abc", chunk_size=3, chunk_overlap=3)
