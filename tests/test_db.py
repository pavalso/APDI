import unittest

from sqlite3 import ProgrammingError

from src import exceptions
from src.db import _DAO
from src.entities import Blob


class TestDB(unittest.TestCase):

    def setUp(self):
        _DAO.connect(':memory:')
        self.default_blob = Blob('x', 'me')
        self._raw_insert(self.default_blob.id_, self.default_blob.perms.owner, self.default_blob.perms.visibility.value)

    @staticmethod
    def _raw_select(id):
        _DAO._cursor.execute('SELECT * FROM blobs WHERE id=?', (id,))
        return _DAO._cursor.fetchone()
    
    @staticmethod
    def _raw_insert(id, owner, visibility):
        _DAO._cursor.execute('INSERT INTO blobs VALUES (?, ?, ?)', (id, owner, visibility))
    
    @staticmethod
    def _exists_in_db(id):
        _r = TestDB._raw_select(id)
        return bool(_r)

    def test_new_blob(self):
        Blob.create('y', self.default_blob.perms.owner)
        self.assertTrue(TestDB._exists_in_db('y'))
        self.assertEqual(TestDB._raw_select(self.default_blob.id_)[1], self.default_blob.perms.owner)

    def test_fetch_blob(self):
        _fetched = Blob.fetch(self.default_blob.id_)
        self.assertEqual(self.default_blob.id_, _fetched.id_)

    def test_fetch_missing_blob(self):
        self.assertRaises(exceptions.BlobNotFoundError, Blob.fetch, 'not_existing')

    def test_id_readonly(self):
        _b = Blob.fetch(self.default_blob.id_)
        self.assertRaises(AttributeError, setattr, _b, 'id_', '123456')

    def test_unique_id(self):
        self.assertRaises(exceptions.BlobAlreadyExistsError, Blob.create, self.default_blob.id_, None)

    def test_update_blob(self):
        _old_owner = self.default_blob.perms.owner
        _new_owner = _old_owner + '_new'
        Blob.update(self.default_blob.id_, owner=_new_owner)
        self.assertNotEqual(Blob.fetch(self.default_blob.id_).perms.owner, _old_owner)

    def test_delete_blob(self):
        Blob.delete(self.default_blob.id_)
        self.assertFalse(TestDB._exists_in_db(self.default_blob.id_))

    def test_delete_missing_blob(self):
        self.assertRaises(exceptions.BlobNotFoundError, Blob.delete, 'not_existing')

    def test_close(self):
        _DAO.close()
        self.assertRaises(ProgrammingError, _DAO.get_blob, 'x')

    def tearDown(self):
        _DAO.close()
