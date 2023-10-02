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

    def __init__(self) -> None:
        """
        Initializes a new instance of the _Dao class.
        """
        self._conn = None
        self._cursor = None

    def connect(self, db_name: PathLike) -> _Ctx:
        """
        Connects to the specified SQLite database.

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

        return _Ctx(self)

    def new_blob(self, _id: str, owner: str, visibility: int = False) -> None:
        """
        Inserts a new blob into the database.

        Args:
            _id: The ID of the blob.
            owner: The owner of the blob.
            public: Whether the blob is public or not. Defaults to False.
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
        """
        _query = f'''SELECT *
            FROM {self.BLOBS}
            WHERE id=?'''
        self._cursor.execute(_query, (_id,))

        _r = self._cursor.fetchone()

        if _r is None:
            raise exceptions.BlobNotFoundError(_id)

        return _r

    def update_blob(self, _id: str, owner: str, visibility: int = False) -> None:
        """
        Updates a blob in the database.

        Args:
            _id: The ID of the blob to update.
            owner: The new owner of the blob.
            public: Whether the blob is public or not. Defaults to False.
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
        """
        _query = f'''DELETE FROM {self.BLOBS}
            WHERE id=?'''
        self._cursor.execute(_query, (_id,))

        if self._cursor.rowcount == 0:
            raise exceptions.BlobNotFoundError(_id)

        self._conn.commit()

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        self._conn.close()

_DAO = _Dao()

__export__ = (_DAO,)
