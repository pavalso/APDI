import io
import os

try:
    from src.classes.blob import Blob
except ImportError:
    from classes.blob import Blob


_SUFIX = 'blob'
_BLOBS_DIR = 'storage'

class FileBlob(Blob):

    _fp: io.FileIO = None

    def __init__(self, id: str, owner, public: bool = False, allowedUsers: list = None) -> None:
        super().__init__(id)

        self.owner = owner
        self.public = public
        self.allowedUsers = allowedUsers if allowedUsers else []

        self.file_name = '%s.%s' % (self.id, _SUFIX)
        self.file_path = os.path.join(_BLOBS_DIR, self.file_name)

    def _open(func) -> None:
        def f(blob, *args, **kwargs):
            blob.open()
            return func(blob, *args, **kwargs)
        return f

    def open(self) -> None:
        if self._fp is not None and not self._fp.closed:
            return

        os.makedirs(_BLOBS_DIR, exist_ok=True)

        self._fp = io.FileIO(
            self.file_path, 
            mode='a+b')

    def read(self, /) -> bytes:
        if self._fp is None or self._fp.closed:
            return b''
        return super().read()

    @_open
    def write(self, __b: bytes) -> int:
        return super().write(__b)

    def update(self) -> None:
        return super().update()

    def delete(self) -> None:
        _r = super().delete()
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        return _r
