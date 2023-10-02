"""
This module contains the _FileBlob class, which represents a file blob that stores data in a file.
"""

import io
import os


try:
    from objects._blob import _Blob
except ImportError:
    from src.objects._blob import _Blob


_SUFIX = 'blob'
_BLOBS_DIR = 'storage'

def _open(func) -> None:
    """
    A decorator function that opens a file blob before calling the decorated function.
    """
    def wrapper(blob, *args, **kwargs):
        blob.open()
        return func(blob, *args, **kwargs)
    return wrapper

class _FileBlob(_Blob):
    """
    A class representing a file blob, which is a type of binary large object (BLOB) 
    that stores data in a file.
    """
    _fp: io.FileIO = None

    @property
    def id_(self) -> str:
        """
        Returns the ID of the file blob (read_only).
        """
        return self.__id

    def __init__(self, _id: str) -> None:
        """
        Initializes a new instance of the _FileBlob class.

        Args:
            _id: The ID of the file blob.
        """
        super().__init__()

        self.__id = _id

        self.file_name = f'{_id}.{_SUFIX}'
        self.file_path = os.path.join(_BLOBS_DIR, self.file_name)

    def open(self) -> None:
        """
        Opens the file for reading and writing.
        """
        if self._fp is not None and not self._fp.closed:
            return

        os.makedirs(_BLOBS_DIR, exist_ok=True)

        self._fp = io.FileIO(
            self.file_path,
            mode='a+b')

    def read(self, /) -> bytes:
        """
        Reads the contents of the file.

        Returns:
            bytes: The contents of the file.
        """
        if self._fp is None or self._fp.closed:
            return b''
        return super().read()

    @_open
    def write(self, __b: bytes) -> int:
        """
        Writes the specified bytes to the file.

        Args:
            __b: The bytes to write to the file.

        Returns:
            int: The number of bytes written to the file.
        """
        return super().write(__b)

    def delete(self) -> None:
        """
        Deletes the file.
        """
        _r = super().delete()
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        return _r

__export__ = (_FileBlob,)
