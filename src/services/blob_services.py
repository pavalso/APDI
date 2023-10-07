"""
This module contains functions for 
creating, updating, deleting, and retrieving Blob objects from a database.
"""

from uuid import uuid4

from src.entities import Blob, User
from src.objects import Visibility
from src import exceptions


def create_blob(
        user_token: str,
        visibility: Visibility = Visibility.PRIVATE,
        allowed_users: set[str] = None) -> Blob | None:
    """
    Creates a new Blob object and inserts it into the database.

    Args:
        user_token: The token of the user creating the blob.
        visibility: Visibility of the blob.
        allowed_users: A list of users allowed to access the Blob.

    Returns:
        Blob: The created Blob object or None if the Blob already exists.
    """
    if (user := User.token_owner(user_token)) is None:
        raise exceptions.InvalidTokenError(user_token)

    return Blob.create(str(uuid4()), user, visibility, allowed_users)

def update_blob(
        blob_id: str,
        user_token: str,
        visibility: Visibility = None,
        allowed_users: set[str] = None) -> Blob | None:
    """
    Updates a Blob object in the database.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.
        visibility: New visibility of the blob.
        allowed_users: A list of users allowed to access the Blob.

    Returns:
        Blob: The updated Blob object or None if the Blob was not found.
    """
    if (user := User.token_owner(user_token)) is None:
        raise exceptions.InvalidTokenError(user_token)

    if not Blob.fetch(blob_id).perms.owner == user:
        raise exceptions.InsufficientPermissionsError(user, blob_id)

    return Blob.update(blob_id, user, visibility, allowed_users)

def delete_blob(blob_id: str, user_token: str) -> None:
    """
    Deletes a Blob object from the database.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.
    """
    if (user := User.token_owner(user_token)) is None:
        raise exceptions.InvalidTokenError(user_token)

    if not Blob.fetch(blob_id).perms.owner == user:
        raise exceptions.InsufficientPermissionsError(user, blob_id)

    Blob.delete(blob_id)

def get_hash_blob(blob_id: str, user_token: str) -> int | None:
    """
    Gets the hash of a Blob object from the database.

    Args:
        blob_id: The ID of the Blob.

    Returns:
        int: The hash of the Blob or None if the Blob was not found.
    """
    if (user := User.token_owner(user_token)) is None:
        raise exceptions.InvalidTokenError(user_token)

    _perms = Blob.fetch(blob_id).perms

    if not _perms.owner == user or user not in _perms.allowed_users:
        raise exceptions.InsufficientPermissionsError(user, blob_id)

    return hash(Blob.fetch(blob_id))

def get_blob(blob_id: str, user_token: str) -> Blob | None:
    """
    Gets a Blob object from the database.

    Args:
        blob_id: The ID of the Blob.

    Returns:
        Blob: The Blob object or None if the Blob was not found.
    """
    blob = Blob.fetch(blob_id)

    if blob.perms.visibility == Visibility.PUBLIC:
        return blob

    if (user := User.token_owner(user_token)) is None:
        raise exceptions.InvalidTokenError(user_token)

    if not blob.perms.owner == user or user not in blob.perms.allowed_users:
        raise exceptions.InsufficientPermissionsError(user, blob_id)

    return blob

def get_all_blobs() -> list[Blob]:
    """
    Gets all Blob objects from the database.
    """
    raise NotImplementedError
