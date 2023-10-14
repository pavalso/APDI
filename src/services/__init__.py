"""
This module contains functions for 
creating, updating, deleting, and retrieving Blob objects from a database.
"""
import hashlib
import io

from src.entities import Blob, Client
from src.objects import Visibility
from src import exceptions


def create_blob(
        user_token: str,
        visibility: Visibility = Visibility.PRIVATE) -> Blob:
    """
    Creates a new Blob object and inserts it into the database.

    Args:
        user_token: The token of the user creating the blob.
        visibility: Visibility of the blob.

    Returns:
        Blob: The created Blob object

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    user = Client.fetch_user(user_token)

    blob = user.create_blob(visibility)

    return blob

def update_blob(
        blob_id: str,
        user_token: str,
        raw: io.BytesIO) -> Blob:
    """
    Updates the contents of a Blob object in the database.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.
        raw: The data to write to the Blob.

    Returns:
        Blob: The updated Blob object.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    user = Client.fetch_user(user_token)

    blob = user.blobs.get(blob_id)

    if blob is None:
        raise exceptions.BlobNotFoundError(blob_id)

    blob.write(raw)

    return blob

def delete_blob(blob_id: str, user_token: str) -> None:
    """
    Deletes a Blob object from the database.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    user = Client.fetch_user(user_token)

    blob = user.blobs.get(blob_id)

    if blob is None:
        raise exceptions.BlobNotFoundError(blob_id)

    blob.delete()

def get_hash_blob(blob_id: str, user_token: str) -> tuple[str, str]:
    """
    Gets the hash of a Blob object from the database.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.

    Returns:
        int: The hash of the Blob.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    blob = get_blob(blob_id, user_token)

    _md5 = hashlib.file_digest(blob.stream, 'md5').hexdigest()
    _sha256 = hashlib.file_digest(blob.stream, 'sha256').hexdigest()

    return _md5, _sha256

def get_blob(blob_id: str, user_token: str) -> Blob:
    """
    Gets a Blob object from the database.

    Args:
        blob_id: The ID of the Blob.

    Returns:
        Blob: The Blob object.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    blob = Blob.fetch(blob_id)

    if blob.perms.visibility == Visibility.PUBLIC:
        return blob

    user = Client.fetch_user(user_token)

    if not blob.has_permissions(user.username):
        raise exceptions.BlobNotFoundError(blob_id)

    return blob

def get_user_blobs(user_token: str) -> list[Blob]:
    """
    Gets all Blobs owned by a user.

    Args:
        user_token: The token of the user.

    Returns:
        list[Blob]: A list of Blobs owned by the user.

    Raises:
        UserNotExists: If the user token is invalid.
    """
    user = Client.fetch_user(user_token)

    return list(user.blobs.keys())

def add_read_permission(blob_id: str, user_token: str, username: str) -> None:
    """
    Adds a user to the list of users allowed to read a Blob.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.
        username: The username of the user to add.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
        UserHavePermissionsError: If the user already has permissions for the Blob.
    """
    blob = get_blob(blob_id, user_token)

    blob.add_permissions(username)

def remove_read_permission(blob_id: str, user_token: str, username: str) -> None:
    """
    Removes a user from the list of users allowed to read a Blob.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.
        username: The username of the user to remove.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
        UserHaveNoPermissionsError: If the user does not have permissions for the Blob.
    """
    blob = get_blob(blob_id, user_token)

    blob.remove_permissions(username)
