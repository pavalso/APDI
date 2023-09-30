"""
This module contains the implementation of a Data Access Object (DAO) 
for interacting with the SQLite database.
"""

import sqlite3


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

    def connect(self, db_name) -> None:
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
            public INTEGER,
            PRIMARY KEY (id))'''
        self._cursor.execute(_query)

    def new_blob(self, _id: str, owner: str, public: bool = False) -> None:
        """
        Inserts a new blob into the database.

        Args:
            _id: The ID of the blob.
            owner: The owner of the blob.
            public: Whether the blob is public or not. Defaults to False.
        """
        _query = f'''INSERT INTO {self.BLOBS} (id, owner, public)
            VALUES (?, ?, ?)'''
        self._cursor.execute(_query, (_id, owner, public))
        self._conn.commit()

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
        return self._cursor.fetchone()

    def update_blob(self, _id: str, owner: str, public: bool = False) -> None:
        """
        Updates a blob in the database.

        Args:
            _id: The ID of the blob to update.
            owner: The new owner of the blob.
            public: Whether the blob is public or not. Defaults to False.
        """
        _query = f'''UPDATE {self.BLOBS}
            SET owner=?, public=?
            WHERE id=?'''
        self._cursor.execute(_query, (owner, public, _id))
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
        self._conn.commit()

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        self._conn.close()

DAO = _Dao()
