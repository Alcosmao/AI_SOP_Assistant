class BlobDocumentStorage:
    """Reads documents from Azure Blob Storage (or Azurite emulator)."""

    def __init__(self, connection_string: str, container_name: str):
        from azure.storage.blob import BlobServiceClient

        self.service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = container_name

    def read_document(self, name: str) -> str | None:
        from azure.core.exceptions import ResourceNotFoundError

        blob_client = self.service_client.get_blob_client(
            container=self.container_name,
            blob=name,
        )
        try:
            data = blob_client.download_blob().readall()
            return data.decode("utf-8")
        except ResourceNotFoundError:
            return None
    
    def list_documents(self) -> list[str]:
        container_client = self.service_client.get_container_client(self.container_name)

        names = []
        for blob in container_client.list_blobs():
            names.append(blob.name)

        return sorted(names)