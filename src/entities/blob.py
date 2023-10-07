"""
This module contains the Blob class, which represents a Blob object 
that can be stored in a database and synchronizes with a file in storage
"""

try:
    from db import _DAO
    from objects._file_blob import _FileBlob
    from objects._perms import _Perms, Visibility
except ImportError:
    from src.db import _DAO
    from src.objects._file_blob import _FileBlob
    from src.objects._perms import _Perms, Visibility


class Blob(_FileBlob):
    """
    Represents a Blob object that can be stored in a database.

    Args:
        owner: The owner of the Blob.
        public: Whether the Blob is public or not.
        allowed_users: A list of users allowed to access the Blob.
        is_in_db: Whether the Blob is currently stored in the database.
    """

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
        super().__init__(_id)

        self.perms = _Perms(owner, visibility, allowed_users)

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

        Raises:
            BlobAlreadyExistsError: If a Blob with the given ID already exists in the database.
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

        Raises:
            BlobNotFoundError: If the Blob with the given ID is not found in the database.
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

        Raises:
            BlobNotFoundError: If the Blob with the given ID is not found in the database.
        """
        _DAO.delete_blob(_id)

    def __str__(self) -> str:
        id_ = f'id={self.id_}'
        owner_ = f'owner={self.perms.owner}'
        visibility_ = f'visibility={self.perms.visibility}'
        allowed_users_ = f'allowed_users={self.perms.allowed_users}'
        return f'Blob({id_}, {owner_}, {visibility_}, {allowed_users_})'

    def user_perms(self, user: str) -> bool:
        """
        Checks whether a user has permissions to access the Blob.

        Args:
            user: The user to check.

        Returns:
            bool: True if the user has permissions to access the Blob, False otherwise.
        """
        return self.perms.owner == user or user in self.perms.allowed_users
