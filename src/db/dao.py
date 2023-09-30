import sqlite3


class _Dao:

    BLOBS = 'blobs'

    def __init__(self) -> None:
        self._conn = None
        self._cursor = None

    def connect(self, db_name) -> None:
        self._conn = sqlite3.connect(db_name)
        self._cursor = self._conn.cursor()

        _query = f'''CREATE TABLE IF NOT EXISTS {self.BLOBS} (
            id TEXT,
            owner TEXT,
            public INTEGER,
            PRIMARY KEY (id))'''
        self._cursor.execute(_query)

    def new_blob(self, _id: str, owner: str, public: bool = False) -> None:
        _query = f'''INSERT INTO {self.BLOBS} (id, owner, public)
            VALUES (?, ?, ?)'''
        self._cursor.execute(_query, (_id, owner, public))
        self._conn.commit()

    def get_blob(self, _id: str) -> tuple:
        _query = f'''SELECT *
            FROM {self.BLOBS}
            WHERE id=?'''
        self._cursor.execute(_query, (_id,))
        return self._cursor.fetchone()

    def update_blob(self, _id: str, owner: str, public: bool = False) -> None:
        _query = f'''UPDATE {self.BLOBS}
            SET owner=?, public=?
            WHERE id=?'''
        self._cursor.execute(_query, (owner, public, _id))
        self._conn.commit()

    def delete_blob(self, _id: str) -> None:
        _query = f'''DELETE FROM {self.BLOBS}
            WHERE id=?'''
        self._cursor.execute(_query, (_id,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

DAO = _Dao()
