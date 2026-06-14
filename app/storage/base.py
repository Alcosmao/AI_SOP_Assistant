from typing import Protocol

class DocumentStorage(Protocol):
    """Interface for any doment storage backend (local, blob, etc.)"""


    def read_document(self, name: str) -> str | None:
        """Return the document text, or None if it does not exist."""
        ...

    def list_documents(self) -> list[str]:
        """Return the names of all available documents."""
        ...