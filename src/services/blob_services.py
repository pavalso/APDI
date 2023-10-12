"""
This module contains functions for 
creating, updating, deleting, and retrieving Blob objects from a database.
"""
from src.entities import Blob
from src.objects import Visibility
from src import exceptions


def create_blob(
        owner: str,
        visibility: Visibility = Visibility.PRIVATE,
        allowed_users: set[str] = None) -> Blob | None:
    """
    Creates a new Blob object and inserts it into the database.

    Args:
        owner: The owner of the Blob.
        public: Whether the Blob is public or not.
        allowed_users: A list of users allowed to access the Blob.

    Returns:
        Blob: The created Blob object or None if the Blob already exists.
    """
    try:
        blob = Blob.create(owner, visibility, allowed_users)
    except exceptions.BlobAlreadyExistsError:
        return None

    return blob

def update_blob(
        id_: str,
        owner: str = None,
        visibility: Visibility = None,
        allowed_users: set[str] = None) -> Blob | None:
    """
    Updates a Blob object in the database.

    Args:
        id_: The ID of the Blob.
        owner: The owner of the Blob.
        public: Whether the Blob is public or not.
        allowed_users: A list of users allowed to access the Blob.

    Returns:
        Blob: The updated Blob object or None if the Blob was not found.
    """
    try:
        blob = Blob.update(id_, owner, visibility, allowed_users)
    except exceptions.BlobNotFoundError:
        return None

    return blob

def delete_blob(id_: str) -> bool:
    """
    Deletes a Blob object from the database.

    Args:
        id_: The ID of the Blob.

    Returns:
        bool: True if the Blob was deleted, False if the Blob was not found.
    """
    try:
        Blob.delete(id_)
    except exceptions.BlobNotFoundError:
        return False

    return True

def get_hash_blob(id_: str) -> int | None:
    """
    Gets the hash of a Blob object from the database.

    Args:
        id_: The ID of the Blob.

    Returns:
        int: The hash of the Blob or None if the Blob was not found.
    """
    try:
        blob = Blob.fetch(id_)
    except exceptions.BlobNotFoundError:
        return None

    return hash(blob)

def get_blob(id_: str) -> Blob | None:
    """
    Gets a Blob object from the database.

    Args:
        id_: The ID of the Blob.

    Returns:
        Blob: The Blob object or None if the Blob was not found.
    """
    try:
        blob = Blob.fetch(id_)
    except exceptions.BlobNotFoundError:
        return None

    return blob

def get_all_blobs() -> list[Blob]:
    """
    Gets all Blob objects from the database.
    """
    raise NotImplementedError
