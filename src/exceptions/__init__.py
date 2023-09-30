class BlobNotFoundError(Exception):
    def __init__(self, _id: str) -> None:
        super().__init__(f'Blob with id {_id} not found')
