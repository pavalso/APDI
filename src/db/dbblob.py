"""
This module contains the Blob class, which represents a Blob object 
that can be stored in a database and synchronizes with a file in storage
"""

import uuid


try:
    import exceptions
    from db.dao import DAO
    from classes._file_blob import _FileBlob
except ImportError:
    from src import exceptions
    from src.db.dao import DAO
    from src.classes._file_blob import _FileBlob


class Blob(_FileBlob):
    """
    Represents a Blob object that can be stored in a database.

    Args:
        owner: The owner of the Blob.
        public: Whether the Blob is public or not.
        allowed_users: A list of users allowed to access the Blob.
        is_in_db: Whether the Blob is currently stored in the database.
    """

    @property
    def is_in_db(self) -> bool:
        """
        Returns whether the Blob is currently stored in the database.
        """
        return self._in_db

    def __init__(
            self, _id: str,
            /,
            owner = None,
            public: bool = False,
            allowed_users: list = None,
            in_db: bool = False) -> None:
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

        self.owner = owner
        self.public = public
        self.allowed_users = allowed_users if allowed_users else []

        self._in_db = in_db

    @staticmethod
    def create(owner, public: bool = False, allowed_users: list = None) -> 'Blob':
        """
        Creates a new Blob object and inserts it into the database.

        Args:
            owner: The owner of the Blob.
            public: Whether the Blob is public or not.
            allowed_users: A list of users allowed to access the Blob.

        Returns:
            Blob: The newly created Blob object.
        """
        _b = Blob(str(uuid.uuid4()), owner, public, allowed_users)
        _b.insert()
        return _b

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

        if _r is None:
            raise exceptions.BlobNotFoundError(id)

        _b = Blob(*_r, in_db=True)

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

    def insert(self) -> None:
        """
        Inserts the Blob object into the database.
        """
        if self.is_in_db:
            return

        DAO.new_blob(self.id_, self.owner, self.public)
        self._in_db = True

    def __str__(self) -> str: # pragma: no cover
        """
        Returns a string representation of the Blob object.
        """
        _public = 'Public' if self.public else 'Private'
        _in_db = 'Yes' if self.is_in_db else 'No'
        return f'{_public} Blob {self.id_} owner: {self.owner}, in database: {_in_db}'
