from pathlib import Path

class LocalDocumentStorage:
    """Reads documents from the local filesystem."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def read_document(self, name: str) -> str | None:
        file_path = self.base_path / name
        try:
            return file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None