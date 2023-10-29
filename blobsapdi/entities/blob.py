"""
This module contains the Blob class, which represents a Blob object 
that can be stored in a database and synchronizes with a file in storage
"""
from uuid import uuid4

from blobsapdi.db import _DAO
from blobsapdi.objects._file_blob import _FileBlob
from blobsapdi.enums import Visibility


class _DBBlob(_FileBlob):
    """
    Represents a Blob object that is stored in a database.
    """

    @property
    def owner(self) -> str:
        """
        Gets the owner of the Blob.

        Returns:
            The owner of the Blob.
        """
        return self._owner

    @property
    def visibility(self) -> Visibility:
        """
        Gets the visibility of the Blob.

        Returns:
            The visibility of the Blob.
        """
        return Visibility(_DAO.get_blob_visibility(self.id_))

    @visibility.setter
    def visibility(self, value: Visibility) -> None:
        """
        Sets the visibility of the Blob.

        Args:
            value: The new visibility of the Blob.
        """
        _DAO.update_blob_visibility(self.id_, value.value)

    @property
    def allowed_users(self) -> set[str]:
        """
        Gets the permissions for the Blob.

        Returns:
            The permissions for the Blob.
        """
        return {i[0] for i in _DAO.get_blob_perms(self.id_)}

    @allowed_users.setter
    def allowed_users(self, value: set[str]) -> None:
        """
        Sets the permissions for the Blob.

        Args:
            value: The new permissions for the Blob.
        """
        _DAO.replace_perms(self.id_, value)

    def __init__(
            self,
            _id: str,
            owner: str) -> None:
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

        self._owner = owner

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
        _DAO.add_perms(self.id_, user)

    def remove_permissions(self, user: str) -> None:
        """
        Removes permissions for a user from the Blob.

        Args:
            user: The user to remove permissions for.
        """
        _DAO.remove_perms(self.id_, user)

    def has_permissions(self, user: str) -> bool:
        """
        Checks if a user has permissions for the Blob.

        Args:
            user: The user to check permissions for.

        Returns:
            If the user has permissions for the Blob.
        """
        return user == self.owner \
            or self.visibility == Visibility.PUBLIC \
            or _DAO.get_user_perms(self.id_, user) is not None

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

        return _DBBlob(_uuid, owner)

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
        id_, owner, _ = _DAO.get_blob(_id)

        _b = _DBBlob(id_, owner)

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
            _id: _DBBlob(_id, user)
            for _id in _r
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
 