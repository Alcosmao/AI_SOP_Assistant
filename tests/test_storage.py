from app.storage.local_storage import LocalDocumentStorage
from app.storage import factory


def test_local_storage_reads_existing_file(tmp_path):
    (tmp_path / "doc.txt").write_text("hello world", encoding="utf-8")

    storage = LocalDocumentStorage(str(tmp_path))

    assert storage.read_document("doc.txt") == "hello world"


def test_local_storage_returns_none_for_missing_file(tmp_path):
    storage = LocalDocumentStorage(str(tmp_path))

    assert storage.read_document("does_not_exist.txt") is None


def test_factory_returns_local_storage_by_default():
    storage = factory.get_storage()

    assert isinstance(storage, LocalDocumentStorage)


def test_factory_raises_on_unknown_mode(monkeypatch):
    monkeypatch.setattr(factory, "STORAGE_MODE", "banana")

    try:
        factory.get_storage()
        assert False, "expected ValueError for unknown STORAGE_MODE"
    except ValueError:
        pass
