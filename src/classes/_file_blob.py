import io
import os


try:
    from classes._blob import _Blob
except ImportError:
    from src.classes._blob import _Blob


_SUFIX = 'blob'
_BLOBS_DIR = 'storage'

class _FileBlob(_Blob):

    _fp: io.FileIO = None

    @property
    def id(self) -> str:
        return self.__id

    def __init__(self, id: str) -> None:
        super().__init__()

        self.__id = id

        self.file_name = '%s.%s' % (id, _SUFIX)
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

    def delete(self) -> None:
        _r = super().delete()
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        return _r

__export__ = (_FileBlob,)
