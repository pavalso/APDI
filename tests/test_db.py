import src.exceptions as exceptions

import unittest

from src.db.dao import DAO
from src.entity import Blob
from sqlite3 import IntegrityError, ProgrammingError


class TestDB(unittest.TestCase):

    def setUp(self):
        DAO.connect(':memory:')
        self.default_blob = Blob('x', 'me')
        self._raw_insert(self.default_blob.id_, self.default_blob.owner, self.default_blob.public)

    @staticmethod
    def _raw_select(id):
        DAO._cursor.execute('SELECT * FROM blobs WHERE id=?', (id,))
        return DAO._cursor.fetchone()
    
    @staticmethod
    def _raw_insert(id, owner, public):
        DAO._cursor.execute('INSERT INTO blobs VALUES (?, ?, ?)', (id, owner, public))
    
    @staticmethod
    def _exists_in_db(id):
        _r = TestDB._raw_select(id)
        return bool(_r)

    def test_new_blob(self):
        Blob.create('y', self.default_blob.owner)
        self.assertTrue(TestDB._exists_in_db('y'))
        self.assertEqual(TestDB._raw_select(self.default_blob.id_)[1], self.default_blob.owner)

    def test_fetch_blob(self):
        _fetched = Blob.fetch(self.default_blob.id_)
        self.assertEqual(self.default_blob.id_, _fetched.id_)

    def test_fetch_missing_blob(self):
        self.assertRaises(exceptions.BlobNotFoundError, Blob.fetch, 'not_existing')

    def test_id_readonly(self):
        _b = Blob.fetch(self.default_blob.id_)
        self.assertRaises(AttributeError, setattr, _b, 'id_', '123456')

    def test_unique_id(self):
        self.assertRaises(IntegrityError, TestDB._raw_insert, self.default_blob.id_, None, None)

    def test_update_blob(self):
        _old_owner = self.default_blob.owner
        self.default_blob.owner = _old_owner + '_new'
        self.default_blob.update()
        self.assertNotEqual(Blob.fetch(self.default_blob.id_).owner, _old_owner)

    def test_delete_blob(self):
        self.default_blob.delete()
        self.assertFalse(TestDB._exists_in_db(self.default_blob.id_))

    def test_close(self):
        DAO.close()
        self.assertRaises(ProgrammingError, DAO.get_blob, 'x')

    def tearDown(self):
        DAO.close()
