"""
This module defines the _Blob class, 
which is an abstract base class for binary large object (blob) storage.
"""

import io


class _Blob:
    """
    Abstract base class for binary large object (blob) storage.
    """

    @property
    def stream(self) -> io.BytesIO:
        """
        Returns the stream of the blob (read_only).
        """
        return self._fp or io.BytesIO()

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
        return self._fp.read()

    def write(self, __b: bytes) -> int:
        """
        Abstract method to write the blob data.

        Args:
            __b: The blob data to be written.

        Returns:
            int: The number of bytes written.
        """
        return self._fp.write(__b)

    def delete(self) -> None:
        """
        Abstract method to delete the blob data.
        """
        if self._fp is None:
            return
        self._fp.close()

__export__ = (_Blob,)
