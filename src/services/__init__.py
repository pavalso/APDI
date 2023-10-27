"""
This module contains functions for 
creating, updating, deleting, and retrieving Blob objects from a database.
"""

import hashlib
import io

from src._logger import LOGGER
from src.entities.blob import _DBBlob
from src.entities import Blob, Client
from src.enums import Visibility
from src import exceptions


logger = LOGGER

_BUFF_SIZE = 1024 * 1024
_AVAILABLE_HASHES = {"md5", "sha1", "sha256", "sha512"}

def create_blob(
        user_token: str,
        visibility: Visibility = Visibility.PRIVATE) -> _DBBlob:
    """
    Creates a new Blob object and inserts it into the database.

    Args:
        user_token: The token of the user creating the blob.
        visibility: Visibility of the blob.

    Returns:
        Blob: The created Blob object

    Raises:
        UserNotExists: If the user token is invalid.
    """
    user = Client.fetch_user(user_token)

    blob = user.create_blob(visibility)

    logger.debug("Created blob %s for user %s", blob.id_, user.username)

    return blob

def update_blob(
        blob_id: str,
        user_token: str,
        raw: io.BytesIO) -> _DBBlob:
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

    blob.truncate(0)

    logger.debug("Writing to blob %s", blob_id)

    while (chunk := raw.read(_BUFF_SIZE)) != b'':
        blob.write(chunk)

    return blob

def update_blob_visibility(blob_id: str, user_token: str, visibility: int) -> None:
    """
    Updates the visibility of a Blob object in the database.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.
        visibility: The new visibility of the Blob.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    visibility = Visibility(visibility)

    user = Client.fetch_user(user_token)

    blob = user.blobs.get(blob_id)

    if blob is None:
        raise exceptions.BlobNotFoundError(blob_id)

    blob.visibility = visibility

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

def get_hash_blob(blob_id: str, user_token: str, hashes_types: str) -> tuple[str, str]:
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

    for hash_type in hashes_types:
        if hash_type not in _AVAILABLE_HASHES:
            raise ValueError(f"Invalid hash type: {hash_type}")

    hashes = { }

    for hash_type in hashes_types:
        hashes[hash_type] = hashlib.file_digest(blob, hash_type, _bufsize = _BUFF_SIZE).hexdigest()
        blob.seek(0)

    return hashes

def get_blob(blob_id: str, user_token: str) -> _DBBlob:
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

    if blob.visibility == Visibility.PUBLIC:
        return blob

    if user_token is None:
        raise exceptions.BlobNotFoundError(blob_id)

    user = Client.fetch_user(user_token)

    if not blob.has_permissions(user.username):
        raise exceptions.BlobNotFoundError(blob_id)

    return blob

def get_user_blobs(user_token: str) -> list[str]:
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

def _get_blob_only_owner(blob_id: str, user_token: str) -> _DBBlob:
    """
    Gets a Blob object from the database, only if the user is the owner.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.

    Returns:
        Blob: The Blob object.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    user = Client.fetch_user(user_token)

    blob = user.blobs.get(blob_id)

    if blob is None:
        raise exceptions.BlobNotFoundError(blob_id)

    return blob

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
    """
    blob = _get_blob_only_owner(blob_id, user_token)

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
    """
    blob = _get_blob_only_owner(blob_id, user_token)

    blob.remove_permissions(username)

def get_read_permissions(blob_id: str, user_token: str) -> list[str] | None:
    """
    Gets all users allowed to read a Blob.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.

    Returns:
        list[str]: A list of usernames allowed to read the Blob or None if the Blob is public.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    blob = _get_blob_only_owner(blob_id, user_token)

    if blob.visibility == Visibility.PUBLIC:
        return None

    return list(blob.allowed_users)

def put_read_permissions(blob_id: str, user_token: str, usernames: set[str]) -> None:
    """
    Sets the list of users allowed to read a Blob.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.
        usernames: The list of usernames to set.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    blob = _get_blob_only_owner(blob_id, user_token)

    blob.allowed_users = usernames

def patch_read_permissions(blob_id: str, user_token: str, usernames: set[str]) -> None:
    """
    Adds users to the list of users allowed to read a Blob.

    Args:
        blob_id: The ID of the Blob.
        user_token: The token of the Blob owner.
        usernames: The list of usernames to add.

    Raises:
        BlobNotFoundError: If the Blob was not found 
            or the user does not have permission to access the Blob.
        UserNotExists: If the user token is invalid.
    """
    blob = _get_blob_only_owner(blob_id, user_token)

    blob.allowed_users |= usernames
