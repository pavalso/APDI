import unittest
import os
import shutil

from blobsapdi.objects._file_blob import _FileBlob



@staticmethod
def _remove_test_dir():
    _st = os.getenv('STORAGE')
    if _st and os.path.isdir(_st):
        shutil.rmtree(_st)

class TestBlob(unittest.TestCase):

    def setUp(self):
        os.environ['STORAGE'] = '.tests_storage'
        self.default_blob = _FileBlob('123456')

    def test_empty_read(self):
        self.default_blob = _FileBlob('123456')
        assert self.default_blob.read() == b''

    def test_chain_write(self):
        _bytes = b'123456' * 1000
        assert self.default_blob.write(_bytes) == len(_bytes)
        _bytes = b'abcd'
        assert self.default_blob.write(_bytes) == len(_bytes)

    def test_write_read(self):
        _bytes = b'123456' * 1000
        self.default_blob.write(_bytes)
        self.default_blob.seek(0)
        assert self.default_blob.read() == _bytes

    def test_chain_create_read(self):
        _bytes = b'123456' * 1000
        with _FileBlob('123456') as _blob:
            _blob = _FileBlob('123456')
            _blob.write(_bytes)
            _blob.seek(0)
            assert _blob.read() == _bytes

            with _FileBlob('123456') as _blob2:
                assert _blob2.read() == _blob.read()

    def test_empty_delete(self):
        assert self.default_blob._fp == None
        self.default_blob.delete()
        assert os.path.isfile(self.default_blob.file_path) == False

    def test_delete(self):
        _bytes = b'123456' * 1000
        self.default_blob.write(_bytes)
        self.default_blob.delete()
        assert os.path.isfile(self.default_blob.file_path) == False

    def tearDown(self):
        self.default_blob.delete()
        _remove_test_dir()
