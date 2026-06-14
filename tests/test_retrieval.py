import pytest

from app.retrieval import (
    calculate_cosine_similarity,
    rank_chunks_by_similarity,
    get_top_k_chunks,
)


def test_identical_vectors_have_similarity_one():
    score = calculate_cosine_similarity([1, 2, 3], [1, 2, 3])
    assert score == pytest.approx(1.0)


def test_orthogonal_vectors_have_similarity_zero():
    score = calculate_cosine_similarity([1, 0], [0, 1])
    assert score == pytest.approx(0.0)


def test_zero_vector_returns_zero():
    assert calculate_cosine_similarity([0, 0], [1, 1]) == 0


def test_different_length_vectors_raise():
    with pytest.raises(ValueError):
        calculate_cosine_similarity([1, 2], [1, 2, 3])


def test_ranking_is_sorted_best_first():
    question = [1, 0]
    chunk_embeddings = [[0, 1], [1, 0]]
    chunks = ["unrelated", "perfect match"]

    ranked = rank_chunks_by_similarity(question, chunk_embeddings, chunks)

    assert ranked[0]["chunk_text"] == "perfect match"
    assert ranked[0]["similarity_score"] >= ranked[1]["similarity_score"]


def test_top_k_returns_requested_count():
    question = [1, 0]
    chunk_embeddings = [[1, 0], [0, 1], [1, 1]]
    chunks = ["a", "b", "c"]

    top = get_top_k_chunks(question, chunk_embeddings, chunks, 2)

    assert len(top) == 2


def test_top_k_zero_raises():
    with pytest.raises(ValueError):
        get_top_k_chunks([1, 0], [[1, 0]], ["a"], 0)
