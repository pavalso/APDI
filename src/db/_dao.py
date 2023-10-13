"""
This module contains the implementation of a Data Access Object (DAO) 
for interacting with the SQLite database.
"""

import sqlite3

from os import PathLike

try:
    import exceptions
except ImportError:
    from src import exceptions


class _Ctx:
    """
    A context manager for handling database connections.
    """

    def __init__(self, _dao: '_Dao') -> None:
        self._dao = _dao

    def __enter__(self):
        return

    def __exit__(self, *_):
        self._dao.close()

class _Dao:
    """
    This class represents a Data Access Object (DAO) for interacting with a SQLite database.
    """
    BLOBS = 'blobs'
    PERMS = 'perms'

    def __init__(self) -> None:
        """
        Initializes a new instance of the _Dao class.
        """
        self._conn = None
        self._cursor = None

    def connect(self, db_name: PathLike) -> _Ctx:
        """
        Connects to the specified SQLite database and creates the necessary tables.

        Args:
            db_name: The name of the database to connect to.
        """
        self._conn = sqlite3.connect(db_name)
        self._cursor = self._conn.cursor()

        _query = f'''CREATE TABLE IF NOT EXISTS {self.BLOBS} (
            id TEXT,
            owner TEXT,
            visibility INTEGER,
            PRIMARY KEY (id))'''

        self._cursor.execute(_query)

        _query = f'''CREATE TABLE IF NOT EXISTS {self.PERMS} (
            id TEXT,
            user TEXT,
            perms INTEGER DEFAULT 0 NOT NULL,
            PRIMARY KEY (id, user),
            FOREIGN KEY (id) REFERENCES {self.BLOBS}(id))'''

        self._cursor.execute(_query)

        return _Ctx(self)

    def new_blob(self, _id: str, owner: str, visibility: int = False) -> None:
        """
        Inserts a new blob into the database.

        Args:
            _id: The ID of the blob.
            owner: The owner of the blob.
            public: Whether the blob is public or not. Defaults to False.
        
        Raises:
            BlobAlreadyExistsError: If a blob with the specified ID already exists.
        """
        _query = f'''INSERT INTO {self.BLOBS} (id, owner, visibility)
            VALUES (?, ?, ?)'''

        try:
            self._cursor.execute(_query, (_id, owner, visibility))
            self._conn.commit()
        except sqlite3.IntegrityError:
            raise exceptions.BlobAlreadyExistsError(_id) from sqlite3.IntegrityError

    def get_blob(self, _id: str) -> tuple:
        """
        Retrieves a blob from the database.

        Args:
            _id: The ID of the blob to retrieve.

        Returns:
            tuple: A tuple representing the blob.

        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''SELECT *
            FROM {self.BLOBS}
            WHERE id=?'''
        self._cursor.execute(_query, (_id,))

        _r = self._cursor.fetchone()

        if _r is None:
            raise exceptions.BlobNotFoundError(_id)

        return _r

    def update_blob(self, _id: str, owner: str, visibility: int = 0) -> None:
        """
        Updates a blob in the database.

        Args:
            _id: The ID of the blob to update.
            owner: The new owner of the blob.
            visibility: The new visibility of the blob.

        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''UPDATE {self.BLOBS}
            SET owner=?, visibility=?
            WHERE id=?'''
        self._cursor.execute(_query, (owner, visibility, _id))

        if self._cursor.rowcount == 0:
            raise exceptions.BlobNotFoundError(_id)

        self._conn.commit()

    def delete_blob(self, _id: str) -> None:
        """
        Deletes a blob from the database.

        Args:
            _id: The ID of the blob to delete.
        
        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''DELETE FROM {self.BLOBS}
            WHERE id=?'''
        self._cursor.execute(_query, (_id,))

        if self._cursor.rowcount == 0:
            raise exceptions.BlobNotFoundError(_id)

        self._conn.commit()

    def add_perms(self, _id: str, user: str) -> None:
        """ 
        Add permissions to a user for a blob.
        
        Args:
            _id: The ID of the blob.
            user: The user to add permissions for.

        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''INSERT INTO {self.PERMS} (id, user, perms)
            VALUES (?, ?, ?)'''

        try:
            self._cursor.execute(_query, (_id, user, 1))
            self._conn.commit()
        except sqlite3.IntegrityError:
            raise exceptions.UserAlreadyHavePermissionsError(_id, user) from sqlite3.IntegrityError

    def remove_perms(self, _id: str, user: str) -> None:
        """ 
        Remove the permissions of a user from a blob.

        Args:
            _id: The ID of the blob.
            user: The user whose permissions to remove.
        
        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''DELETE FROM {self.PERMS}
            WHERE id=? AND user=?'''
        self._cursor.execute(_query, (_id, user))

        if self._cursor.rowcount == 0:
            raise exceptions.UserHaveNoPermissionsError(_id, user)

        self._conn.commit()

    def get_user_perms(self, _id: str, user: str) -> tuple:
        """
        Retrieves the permissions of a user for a blob.

        Args:
            _id: The ID of the blob.
            user: The user whose permissions to retrieve.

        Returns:
            tuple: A tuple representing the permissions.

        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''SELECT perms
            FROM {self.PERMS}
            WHERE id=? AND user=?'''
        self._cursor.execute(_query, (_id, user))

        _r = self._cursor.fetchone()

        return _r if _r is None else _r[0]

    def get_blobs(self, user: str) -> list[tuple]:
        """
        Retrieves all blobs owned by a user.

        Args:
            user: The user whose blobs to retrieve.

        Returns:
            list[tuple]: A list of tuples representing the blobs.
        """
        _query = f'''SELECT *
            FROM {self.BLOBS}
            WHERE owner=?'''
        self._cursor.execute(_query, (user,))

        return self._cursor.fetchall()


    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        self._conn.close()

_DAO = _Dao()

__export__ = (_DAO,)
