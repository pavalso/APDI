class BlobNotFoundError(Exception):
    def __init__(self, id: str) -> None:
        super().__init__('Blob with id %s not found' % id)
