import sqlite3


class __Dao:

    BLOBS = 'blobs'

    def __init__(self) -> None:
        self._conn = None
        self._cursor = None

    def connect(self, db_name) -> None:
        self._conn = sqlite3.connect(db_name)
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            '''CREATE TABLE IF NOT EXISTS %s (   
                id TEXT,
                owner TEXT, 
                public INTEGER, 
                PRIMARY KEY (id))''' % self.BLOBS)

    def newBlob(self, id: str, owner: str, public: bool = False) -> None:
        self._cursor.execute(
            '''INSERT INTO %s 
            VALUES (?, ?, ?)''' % self.BLOBS, 
            (id, owner, public))
        self._conn.commit()

    def getBlob(self, id: str) -> tuple:
        self._cursor.execute(
            '''SELECT * 
            FROM %s 
            WHERE id=?''' % self.BLOBS, 
            (id,))
        return self._cursor.fetchone()
    
    def updateBlob(self, id: str, owner: str, public: bool = False) -> None:
        self._cursor.execute(
            '''UPDATE %s 
            SET owner=?, public=? 
            WHERE id=?''' % self.BLOBS, 
            (owner, public, id))
        self._conn.commit()

    def deleteBlob(self, id: str) -> None:
        self._cursor.execute(
            '''DELETE FROM %s 
            WHERE id=?''' % self.BLOBS,
            (id,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

DAO = __Dao()
