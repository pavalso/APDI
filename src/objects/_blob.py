"""
This module defines the _Blob class, 
which is an abstract base class for binary large object (blob) storage.
"""

import hashlib
import io


class _Blob:
    """
    Abstract base class for binary large object (blob) storage.
    """

    def __init__(self, stream: io.BytesIO = None) -> None:
        """
        Constructor for _Blob class.

        Args:
            stream: A BytesIO object representing the blob data.
        """
        self._fp = stream

    def read(self, /) -> bytes:
        """
        Abstract method to read the blob data.

        Returns:
            bytes: The blob data.
        """
        self._fp.seek(0)
        return self._fp.read()

    def write(self, __b: bytes) -> int:
        """
        Abstract method to write the blob data.

        Args:
            __b: The blob data to be written.

        Returns:
            int: The number of bytes written.
        """
        _r = self._fp.write(__b)
        self._fp.seek(0)
        return _r

    def delete(self) -> None:
        """
        Abstract method to delete the blob data.
        """
        if self._fp is None:
            return
        self._fp.close()

    def __hash__(self) -> int:
        """
        Method to compute the hash value of the blob data.
        """
        return int(hashlib.sha256(self.read()).hexdigest(), 16)

__export__ = (_Blob,)
