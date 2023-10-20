"""
This module contains the Blob class, which represents a Blob object 
that can be stored in a database and synchronizes with a file in storage
"""
from uuid import uuid4

from src.db import _DAO
from src.objects._file_blob import _FileBlob
from src.objects._perms import _Perms, Visibility
from src.entities.perms import Perms


class _DBBlob(_FileBlob):
    """
    Represents a Blob object that is stored in a database.
    """

    @property
    def allowed_users(self) -> set[str]:
        """
        Gets the permissions for the Blob.

        Returns:
            The permissions for the Blob.
        """
        return set(Perms.fetch_blob_perms(self.id_))

    @allowed_users.setter
    def allowed_users(self, value: set[str]) -> None:
        """
        Sets the permissions for the Blob.

        Args:
            value: The new permissions for the Blob.
        """
        Perms.put_blob_perms(self.id_, value)

    def __init__(
            self,
            _id: str,
            owner: str,
            visibility: Visibility = Visibility.PRIVATE) -> None:
        """
        Initializes a new Blob object.

        Args:
            _id: The ID of the Blob.
            owner: The owner of the Blob.
            public: Whether the Blob is public or not.
            allowed_users: A list of users allowed to access the Blob.
            in_db: Whether the Blob is currently stored in the database.
        """
        super().__init__(_id)

        self.seek(0)

        self.perms = _Perms(owner, visibility)

    def delete(self) -> None:
        """
        Deletes the Blob from the database.
        """
        super().delete()
        Blob.delete(self.id_)

    def add_permissions(self, user: str) -> None:
        """
        Adds permissions for a user to the Blob.

        Args:
            user: The user to add permissions for.
        """
        Perms.create(self.id_, user)

    def remove_permissions(self, user: str) -> None:
        """
        Removes permissions for a user from the Blob.

        Args:
            user: The user to remove permissions for.
        """
        Perms.delete(self.id_, user)

    def has_permissions(self, user: str) -> bool:
        """
        Checks if a user has permissions for the Blob.

        Args:
            user: The user to check permissions for.

        Returns:
            If the user has permissions for the Blob.
        """
        return user == self.perms.owner \
            or self.perms.visibility == Visibility.PUBLIC \
            or Perms.exists(self.id_, user)

    def __str__(self) -> str:
        id_ = f'id={self.id_}'
        owner_ = f'owner={self.perms.owner}'
        visibility_ = f'visibility={self.perms.visibility}'
        return f'Blob({id_}, {owner_}, {visibility_})'

class Blob:
    """
    Represents a Blob object that can be stored in a database.
    """
    @staticmethod
    def create(
        owner: str, visibility: Visibility = Visibility.PRIVATE) -> _DBBlob:
        """
        Creates a new Blob object and inserts it into the database.

        Args:
            owner: The owner of the Blob.
            public: Whether the Blob is public or not.
            allowed_users: A list of users allowed to access the Blob.

        Returns:
            Blob: The newly created Blob object.

        Raises:
            BlobAlreadyExistsError: If a Blob with the given ID already exists in the database.
        """
        _uuid = str(uuid4())

        _DAO.new_blob(_uuid, owner, visibility.value)

        return _DBBlob(_uuid, owner, visibility)

    @staticmethod
    def fetch(_id: str) -> _DBBlob:
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

        _b = _DBBlob(*_r)

        return _b

    @staticmethod
    def update(
        _id: str, owner: str = None, visibility: Visibility = None,
        allowed_users: set[str] = None) -> _DBBlob:
        """
        Updates a Blob object in the database.

        Args:
            _id: The ID of the Blob to update.
            owner: The new owner of the Blob.
            visibility: The new visibility of the Blob.
            allowed_users: The new list of users allowed to access the Blob.

        Returns:
            Blob: The updated Blob object.

        Raises:
            BlobNotFoundError: If the Blob with the given ID is not found in the database.
        """
        _b = Blob.fetch(_id)

        _b.perms.owner = owner or _b.perms.owner
        _b.perms.visibility = visibility or _b.perms.visibility
        #_b.perms.allowed_users = allowed_users or _b.perms.allowed_users

        _DAO.update_blob(_id, _b.perms.owner, _b.perms.visibility.value)

        return _b

    @staticmethod
    def fetch_user_blobs(user: str) -> dict[str, _DBBlob]:
        """
        Fetches all Blobs owned by a user.

        Args:
            user: The user to fetch Blobs for.

        Returns:
            list[Blob]: A list of Blobs owned by the user.
        """
        _r = _DAO.get_blobs(user)

        _bs = {
            _id: _DBBlob(_id, user, Visibility(_v))
            for _id, _, _v in _r 
        }

        return _bs

    @staticmethod
    def delete(_id: str) -> None:
        """
        Deletes a Blob object from the database.

        Args:
            _id: The ID of the Blob to delete.

        Raises:
            BlobNotFoundError: If the Blob with the given ID is not found in the database.
        """
        _DAO.delete_blob(_id)
 