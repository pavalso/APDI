"""
This module contains custom exceptions that can be raised in the application.
"""

class BlobNotFoundError(Exception):
    """
    Exception raised when a blob with a given ID is not found.

    Args:
        _id: The ID of the missing blob.
    """

    def __init__(self, _id: str) -> None:
        super().__init__(f'Blob with id {_id} not found')

class BlobAlreadyExistsError(Exception):
    """
    Exception raised when a blob with a given ID already exists.

    Args:
        _id: The ID of the already existing blob.
    """

    def __init__(self, _id: str) -> None:
        super().__init__(f'Blob with id {_id} already exists')
