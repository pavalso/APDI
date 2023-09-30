import pytest
import os

from src.classes.file_blob import FileBlob


@pytest.fixture
def default_blob():
    return FileBlob('123456', 'me')

def test_empty_read(default_blob):
    assert default_blob.read() == b''

