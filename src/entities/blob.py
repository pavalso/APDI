"""
This module contains the Blob class, which represents a Blob object 
that can be stored in a database and synchronizes with a file in storage
"""
from dataclasses import dataclass


try:
    from db import _DAO
    from objects._file_blob import _FileBlob
    from objects._perms import _Perms, Visibility
except ImportError:
    from src.db import _DAO
    from src.objects._file_blob import _FileBlob
    from src.objects._perms import _Perms, Visibility


@dataclass
class Blob:
    """
    Represents a Blob object that can be stored in a database.

    Args:
        owner: The owner of the Blob.
        public: Whether the Blob is public or not.
        allowed_users: A list of users allowed to access the Blob.
        is_in_db: Whether the Blob is currently stored in the database.
    """

    @property
    def id_(self) -> str:
        """
        Returns the ID of the Blob. (read_only)
        """
        return self.stream.id_

    def __init__(
            self,
            _id: str,
            owner: str,
            visibility: Visibility = Visibility.PRIVATE,
            allowed_users: set[str] = None) -> None:
        """
        Initializes a new Blob object.

        Args:
            _id: The ID of the Blob.
            owner: The owner of the Blob.
            public: Whether the Blob is public or not.
            allowed_users: A list of users allowed to access the Blob.
            in_db: Whether the Blob is currently stored in the database.
        """
        self.perms = _Perms(owner, visibility, allowed_users)
        self.stream = _FileBlob(_id)

    @staticmethod
    def create(
        id_: str, owner: str, visibility: Visibility = Visibility.PRIVATE,
        allowed_users: set[str] = None) -> 'Blob':
        """
        Creates a new Blob object and inserts it into the database.

        Args:
            owner: The owner of the Blob.
            public: Whether the Blob is public or not.
            allowed_users: A list of users allowed to access the Blob.

        Returns:
            Blob: The newly created Blob object.
        """
        _DAO.new_blob(id_, owner, visibility.value)

        return Blob(id_, owner, visibility, allowed_users)

    @staticmethod
    def fetch(_id: str) -> 'Blob':
        """
        Fetches a Blob object from the database by its ID.

        Args:
            _id: The ID of the Blob to fetch.

        Returns:
            Blob: The fetched Blob object.

        Raises:
            BlobNotFoundError: If the Blob with the given ID is not found in the database.
        """
        _r = _DAO.get_blob(_id)

        _b = Blob(*_r)

        return _b

    @staticmethod
    def update(
        _id: str, owner: str = None, visibility: Visibility = None,
        allowed_users: set[str] = None) -> 'Blob':
        """
        Updates a Blob object in the database.

        Args:
            _id: The ID of the Blob to update.
            owner: The new owner of the Blob.
            visibility: The new visibility of the Blob.
            allowed_users: The new list of users allowed to access the Blob.

        Returns:
            Blob: The updated Blob object.
        """

        _b = Blob.fetch(_id)

        _b.perms.owner = owner or _b.perms.owner
        _b.perms.visibility = visibility or _b.perms.visibility
        _b.perms.allowed_users = allowed_users or _b.perms.allowed_users

        _DAO.update_blob(_id, _b.perms.owner, _b.perms.visibility.value)

        return _b

    @staticmethod
    def delete(_id: str) -> None:
        """
        Deletes a Blob object from the database.

        Args:
            _id: The ID of the Blob to delete.
        """

        _DAO.delete_blob(_id)
