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

    def list_documents(self) -> list[str]:
        if not self.base_path.exists():
            return []
        
        names = []
        for item in self.base_path.iterdir():
            if item.is_file() and not item.name.startswith("."):
                names.append(item.name)

        return sorted(names)