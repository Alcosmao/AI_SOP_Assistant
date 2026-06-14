from app.config import (
    STORAGE_MODE,
    DOCUMENTS_PATH,
    AZURE_STORAGE_CONNECTION_STRING,
    AZURE_STORAGE_CONTAINER_NAME
)
from app.storage.local_storage import LocalDocumentStorage
from app.storage.blob_storage import BlobDocumentStorage

def get_storage():
    if STORAGE_MODE == "local":
        return LocalDocumentStorage(DOCUMENTS_PATH)  

    if STORAGE_MODE == "blob":
        return BlobDocumentStorage(
            AZURE_STORAGE_CONNECTION_STRING,
            AZURE_STORAGE_CONTAINER_NAME
        )

    raise ValueError(f"Unknown STORAGE_MODE: {STORAGE_MODE}")