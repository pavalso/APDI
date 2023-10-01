"""
This module contains the Blob class, which represents a Blob object 
that can be stored in a database and synchronizes with a file in storage
"""
from dataclasses import dataclass


try:
    from db.dao import DAO
    from classes._file_blob import _FileBlob
    from entity.perms import Perms, Visibility
except ImportError:
    from src.db.dao import DAO
    from src.classes._file_blob import _FileBlob
    from src.entity.perms import Perms, Visibility


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
        self.perms = Perms(owner, visibility, allowed_users)
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
        DAO.new_blob(id_, owner, visibility.value)

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
        _r = DAO.get_blob(_id)

        _b = Blob(*_r)

        return _b

    def delete(self) -> None:
        """
        Deletes the Blob object from the database.
        """
        super().delete()
        DAO.delete_blob(self.id_)
        self._in_db = False

    def update(self) -> None:
        """
        Updates the Blob object in the database.
        """
        DAO.update_blob(self.id_, self.owner, self.public)
