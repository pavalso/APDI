"""
This module contains the _FileBlob class, which represents a file blob that stores data in a file.
"""

import io
import os

from ._blob import _Blob


_SUFIX = 'blob'

class _FileBlob(_Blob):
    """
    A class representing a file blob, which is a type of binary large object (BLOB) 
    that stores data in a file.
    """
    _fp: io.FileIO = None
    _dir: str = os.getenv("STORAGE", "storage")

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
        self.file_path = os.path.join(self._dir, self.file_name)

    def read(self, /) -> bytes:
        """
        Reads the contents of the file.

        Returns:
            bytes: The contents of the file.
        """
        try:
            with open(self.file_path, 'rb') as self._fp:
                return super().read()
        except FileNotFoundError:
            return b''

    def write(self, __b: bytes) -> int:
        """
        Writes the specified bytes to the file.

        Args:
            __b: The bytes to write to the file.

        Returns:
            int: The number of bytes written to the file.
        """
        if not os.path.isdir(self._dir):
            os.makedirs(self._dir, exist_ok=True)

        with open(self.file_path, 'wb') as self._fp:
            return super().write(__b)

    def delete(self) -> None:
        """
        Deletes the file.
        """
        super().delete()
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)

    def __eq__(self, __value: object) -> bool:
        return issubclass(type(__value), self.__class__) and self.id_ == __value.id_

    def __hash__(self) -> int:
        return super().__hash__()

__export__ = (_FileBlob,)
