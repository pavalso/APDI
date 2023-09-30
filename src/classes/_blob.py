import abc
import hashlib
import io


class _Blob(abc.ABC):

    def __init__(self, stream: io.BytesIO = None) -> None:
        self._fp = stream

    @abc.abstractmethod
    def read(self, /) -> bytes:
        self._fp.seek(0)
        return self._fp.read()

    @abc.abstractmethod
    def write(self, __b: bytes) -> int:
        self._fp.truncate(0)
        _r = self._fp.write(__b)
        self._fp.seek(0)
        return _r

    @abc.abstractmethod
    def delete(self) -> None:
        if self._fp is None:
            return
        self._fp.close()

    def __hash__(self) -> int:
        return int(hashlib.sha256(self.read()).hexdigest(), 16)

__export__ = (_Blob,)
