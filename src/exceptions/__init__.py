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

class InvalidTokenError(Exception):
    """
    Exception raised when a token is invalid.

    Args:
        token: The invalid token.
    """

    def __init__(self, token: str) -> None:
        super().__init__(f'Token {token} is invalid')

class InsufficientPermissionsError(Exception):
    """
    Exception raised when a user does not have sufficient permissions.

    Args:
        username: The username of the user.
        blob_id: The ID of the blob.
    """

    def __init__(self, username: str, blob_id: str) -> None:
        super().__init__(
            f'User {username} does not have sufficient permissions to access blob {blob_id}')

class UserHavePermissionsError(Exception):
    """
    Exception raised when a user already has permissions for a blob.

    Args:
        blob: The blob the user already has permissions for.
        user: The user that already has permissions for the blob.
    """

    def __init__(self, blob: str, user: str) -> None:
        super().__init__(f'User {user} already has permissions for blob {blob}')

class UserHaveNoPermissionsError(Exception):
    """
    Exception raised when a user does not have permissions for a blob.

    Args:
        blob: The blob the user does not have permissions for.
        user: The user that does not have permissions for the blob.
    """

    def __init__(self, blob: str, user: str) -> None:
        super().__init__(f'User {user} does not have permissions for blob {blob}')
