import sqlite3


class _Dao:

    BLOBS = 'blobs'

    def __init__(self) -> None:
        self._conn = None
        self._cursor = None

    def connect(self, db_name) -> None:
        self._conn = sqlite3.connect(db_name)
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS {self.BLOBS} (   
                id TEXT,
                owner TEXT, 
                public INTEGER, 
                PRIMARY KEY (id))''')

    def new_blob(self, _id: str, owner: str, public: bool = False) -> None:
        self._cursor.execute(
            f'''INSERT INTO {self.BLOBS} 
            VALUES (?, ?, ?)''',
            (_id, owner, public))
        self._conn.commit()

    def get_blob(self, _id: str) -> tuple:
        self._cursor.execute(
            f'''SELECT * 
            FROM {self.BLOBS} 
            WHERE id=?''',
            (_id,))
        return self._cursor.fetchone()

    def update_blob(self, _id: str, owner: str, public: bool = False) -> None:
        self._cursor.execute(
            f'''UPDATE {self.BLOBS}
            SET owner=?, public=? 
            WHERE id=?''',
            (owner, public, _id))
        self._conn.commit()

    def delete_blob(self, _id: str) -> None:
        self._cursor.execute(
            f'''DELETE FROM {self.BLOBS}
            WHERE id=?''',
            (_id,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

DAO = _Dao()
