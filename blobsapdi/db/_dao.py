"""
This module contains the implementation of a Data Access Object (DAO) 
for interacting with the SQLite database.
"""

import logging
import sqlite3

from os import PathLike
from threading import Lock

from blobsapdi import exceptions


logger = logging.getLogger("APDI")

class _Dao:
    """
    This class represents a Data Access Object (DAO) for interacting with a SQLite database.
    """
    BLOBS = 'blobs'
    PERMS = 'perms'

    LOCK = Lock()

    def __init__(self) -> None:
        """
        Initializes a new instance of the _Dao class.
        """
        self._conn = None
        self._cursor = None

    def connect(self, db_name: PathLike) -> '_Dao':
        """
        Connects to the specified SQLite database and creates the necessary tables.

        Args:
            db_name: The name of the database to connect to.
        """

        logger.info("Connecting to database %s", db_name)

        self._conn = sqlite3.connect(db_name, check_same_thread=False)
        self._cursor = self._conn.cursor()

        _query = f'''CREATE TABLE IF NOT EXISTS {self.BLOBS} (
            id TEXT,
            owner TEXT,
            visibility TEXT,
            PRIMARY KEY (id))'''

        self._cursor.execute(_query)

        _query = f'''CREATE TABLE IF NOT EXISTS {self.PERMS} (
            id TEXT,
            user TEXT UNIQUE,
            perms INTEGER DEFAULT 0 NOT NULL,
            PRIMARY KEY (id, user),
            FOREIGN KEY (id) REFERENCES {self.BLOBS}(id))'''

        self._cursor.execute(_query)

        return self

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
            with _Dao.LOCK:
                self._cursor.execute(_query, (_id, owner, visibility))
                self._conn.commit()
        except sqlite3.IntegrityError:
            raise exceptions.BlobAlreadyExistsError(_id) from sqlite3.IntegrityError

    def get_blob(self, _id: str) -> tuple[str, str, int]:
        """
        Retrieves a blob from the database.

        Args:
            _id: The ID of the blob to retrieve.

        Returns:
            tuple: A tuple representing the blob.

        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''SELECT id, owner, visibility
            FROM {self.BLOBS}
            WHERE id=?'''

        with _Dao.LOCK:
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

        with _Dao.LOCK:
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
  
        with _Dao.LOCK:
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
        self.bulk_add_perms(_id, {user})

    def bulk_add_perms(self, _id: str, users: set[str]) -> None:
        """
        Adds permissions to multiple users for a blob.

        Args:
            _id: The ID of the blob.
            users: The users to add permissions for.

        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''INSERT OR IGNORE INTO {self.PERMS} (id, user, perms)
            VALUES (?, ?, ?)'''

        with _Dao.LOCK:
            self._cursor.executemany(_query, [(_id, user, 0) for user in users])
            self._conn.commit()

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

        with _Dao.LOCK:
            self._cursor.execute(_query, (_id, user))
            self._conn.commit()

    def replace_perms(self, _id: str, users: set[str]) -> None:
        """
        Replaces the permissions of a blob with the specified users.

        Args:
            _id: The ID of the blob.
            users: The users to set permissions for.

        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''DELETE FROM {self.PERMS}
            WHERE id=?'''

        with _Dao.LOCK:
            self._cursor.execute(_query, (_id,))

        self.bulk_add_perms(_id, users)

    def get_user_perms(self, _id: str, user: str) -> int:
        """
        Retrieves the permissions of a user for a blob.

        Args:
            _id: The ID of the blob.
            user: The user whose permissions to retrieve.

        Returns:
            int: The permissions of the user for the blob.
        """
        _query = f'''SELECT perms
            FROM {self.PERMS}
            WHERE id=? AND user=?'''

        with _Dao.LOCK:
            self._cursor.execute(_query, (_id, user))
            _r = self._cursor.fetchone()
            return None if _r is None else _r[0]

    def get_blob_perms(self, _id: str) -> list[tuple[str, int]]:
        """
        Retrieves all permissions for a blob.

        Args:
            _id: The ID of the blob.

        Returns:
            list[tuple]: A list of tuples representing the permissions.
        """
        _query = f'''SELECT user, perms
            FROM {self.PERMS}
            WHERE id=?'''

        with _Dao.LOCK:
            self._cursor.execute(_query, (_id,))
            return self._cursor.fetchall()

    def get_blobs(self, user: str) -> list[str]:
        """
        Retrieves all blobs owned by a user.

        Args:
            user: The user whose blobs to retrieve.

        Returns:
            list[tuple]: A list of tuples representing the blobs.
        """
        _query = f'''SELECT id
            FROM {self.BLOBS}
            WHERE owner=?'''

        with _Dao.LOCK:
            self._cursor.execute(_query, (user,))
            return [_t[0] for _t in self._cursor.fetchall()]

    def get_blob_visibility(self, _id: str) -> str:
        """
        Retrieves the visibility of a blob.

        Args:
            _id: The ID of the blob.

        Returns:
            str: The visibility of the blob.
        
        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''SELECT visibility
            FROM {self.BLOBS}
            WHERE id=?'''

        with _Dao.LOCK:
            self._cursor.execute(_query, (_id,))
            _r = self._cursor.fetchone()

            if _r is None:
                raise exceptions.BlobNotFoundError(_id)

            return _r[0]

    def update_blob_visibility(self, _id: str, visibility: str) -> None:
        """
        Updates the visibility of a blob.

        Args:
            _id: The ID of the blob.
            visibility: The new visibility of the blob.

        Raises:
            BlobNotFoundError: If the blob with the specified ID is not found.
        """
        _query = f'''UPDATE {self.BLOBS}
            SET visibility=?
            WHERE id=?'''

        with _Dao.LOCK:
            self._cursor.execute(_query, (visibility, _id))

            if self._cursor.rowcount == 0:
                raise exceptions.BlobNotFoundError(_id)

            self._conn.commit()

    def close(self) -> None:
        """
        Closes the connection to the database.
        """

        logger.info("Closing database connection")

        self._conn.close()

    def __enter__(self) -> '_Dao':
        return self

    def __exit__(self, *_):
        self.close()

_DAO = _Dao()

__export__ = (_DAO,)
