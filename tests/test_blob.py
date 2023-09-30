import pytest
import unittest
import os

from src.classes._file_blob import _FileBlob


class TestBlob(unittest.TestCase):

    def setUp(self):
        self.default_blob = _FileBlob('123456')

    def test_empty_read(self):
        assert self.default_blob.read() == b''

    def test_chain_write(self):
        _bytes = b'123456' * 1000
        assert self.default_blob.write(_bytes) == len(_bytes)
        _bytes = b'abcd'
        assert self.default_blob.write(_bytes) == len(_bytes)

    def test_write_read(self):
        _bytes = b'123456' * 1000
        self.default_blob.write(_bytes)
        assert self.default_blob.read() == _bytes

    def test_empty_delete(self):
        assert self.default_blob._fp == None
        self.default_blob.delete()
        assert os.path.isfile(self.default_blob.file_path) == False

    def test_delete(self):
        _bytes = b'123456' * 1000
        self.default_blob.write(_bytes)
        assert self.default_blob._fp != None
        self.default_blob.delete()
        assert os.path.isfile(self.default_blob.file_path) == False

    def test_hash(self):
        _bytes = b'123456' * 1000
        self.default_blob.write(_bytes)
        assert hash(self.default_blob) == 1404332994597457676

    def tearDown(self):
        self.default_blob.delete()
