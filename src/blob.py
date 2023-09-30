import uuid

try:
    import exceptions
except ImportError:
    from src import exceptions


try:
    from db.dao import DAO
    from classes._file_blob import _FileBlob
except ImportError:
    from src.db.dao import DAO
    from src.classes._file_blob import _FileBlob


class Blob(_FileBlob):

    def __init__(self, id: str, owner = None, public: bool = False, allowedUsers: list = None) -> None:
        super().__init__(id)

        self.owner = owner
        self.public = public
        self.allowedUsers = allowedUsers if allowedUsers else []

        self._in_db = False

    @staticmethod
    def create(owner, public: bool = False, allowedUsers: list = None) -> 'Blob':
        _b = Blob(str(uuid.uuid4()), owner, public, allowedUsers)
        _b._insert()
        return _b
    
    @staticmethod
    def fetch(id: str) -> 'Blob':
        _r = DAO.getBlob(id)

        if _r is None:
            raise exceptions.BlobNotFoundError(id)

        _b = Blob(*_r)
        _b._in_db = True

        return _b

    def read(self) -> bytes:
        return super().read()
    
    def write(self, data: bytes) -> None:
        super().write(data)

    def delete(self) -> None:
        super().delete()
        DAO.deleteBlob(self.id)
        self._in_db = False

    def update(self) -> None:
        DAO.updateBlob(self.id, self.owner, self.public)

    def _insert(self) -> None:
        if self._in_db:
            return

        DAO.newBlob(self.id, self.owner, self.public)
        self._in_db = True

    def __str__(self) -> str: # pragma: no cover
        return '%s Blob %s owner: %s, in database: %s' % (
            'Public' if self.public else 'Private', 
            self.id, 
            self.owner, 
            'Yes' if self._in_db else 'No')
