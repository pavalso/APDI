import pytest
import os

from src.classes.file_blob import FileBlob


@pytest.fixture
def default_blob():
    return FileBlob('123456', 'me')

def test_empty_read(default_blob):
    assert default_blob.read() == b''

def test_chain_write(default_blob):
    _bytes = b'123456' * 1000
    assert default_blob.write(_bytes) == len(_bytes)
    _bytes = b'abcd'
    assert default_blob.write(_bytes) == len(_bytes)

def test_write_read(default_blob):
    _bytes = b'123456' * 1000
    default_blob.write(_bytes)
    assert default_blob.read() == _bytes

