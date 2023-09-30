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

    @property
    def is_in_db(self) -> bool:
        return self._in_db

    def __init__(
            self, _id: str,
            /,
            owner = None,
            public: bool = False,
            allowed_users: list = None,
            in_db: bool = False) -> None:
        super().__init__(_id)

        self.owner = owner
        self.public = public
        self.allowed_users = allowed_users if allowed_users else []

        self._in_db = in_db

    @staticmethod
    def create(owner, public: bool = False, allowed_users: list = None) -> 'Blob':
        _b = Blob(str(uuid.uuid4()), owner, public, allowed_users)
        _b.insert()
        return _b

    @staticmethod
    def fetch(_id: str) -> 'Blob':
        _r = DAO.get_blob(_id)

        if _r is None:
            raise exceptions.BlobNotFoundError(id)

        _b = Blob(*_r, in_db=True)

        return _b

    def delete(self) -> None:
        super().delete()
        DAO.delete_blob(self.id_)
        self._in_db = False

    def update(self) -> None:
        DAO.update_blob(self.id_, self.owner, self.public)

    def insert(self) -> None:
        if self._in_db:
            return

        DAO.new_blob(self.id_, self.owner, self.public)
        self._in_db = True

    def __str__(self) -> str: # pragma: no cover
        _public = 'Public' if self.public else 'Private'
        _in_db = 'Yes' if self._in_db else 'No'
        return f'{_public} Blob {self.id_} owner: {self.owner}, in database: {_in_db}'
