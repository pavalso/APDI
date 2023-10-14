"""
This module contains the _FileBlob class, which represents a file blob that stores data in a file.
"""

import io
import os


_SUFIX = 'blob'

class _FileBlob(io.FileIO):
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
        self.__id = _id

        self.file_name = f'{_id}.{_SUFIX}'
        self.file_path = os.path.join(self._dir, self.file_name)

        super().__init__(self.file_path, 'a+b')

    def delete(self) -> None:
        """
        Deletes the file.
        """
        super().close()
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)

    def __eq__(self, __value: object) -> bool:
        return issubclass(type(__value), self.__class__) and self.id_ == __value.id_

__export__ = (_FileBlob,)
