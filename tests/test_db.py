import src.exceptions as exceptions

import unittest

from src.db.dao import DAO
from src import Blob
from sqlite3 import IntegrityError, ProgrammingError


class TestDB(unittest.TestCase):

    def setUp(self):
        DAO.connect(':memory:')
        self.default_blob = Blob('x', 'me')
        self.default_blob._insert()

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
        _b = Blob.create(self.default_blob.owner)
        self.assertEqual(_b.owner, self.default_blob.owner)
        self.assertTrue(TestDB._exists_in_db(_b.id_))

    def test_insert_on_existing_blob(self):
        self.assertIsNone(self.default_blob._insert())

    def test_id_readonly(self):
        _b = Blob.create(self.default_blob.owner)
        self.assertRaises(AttributeError, setattr, _b, 'id', '123456')

    def test_unique_id(self):
        self.assertRaises(IntegrityError, TestDB._raw_insert, self.default_blob.id_, None, None)

    def test_update_blob(self):
        _b = Blob.create(self.default_blob.owner)
        _old_owner = _b.owner
        _b.owner = _old_owner + '_new'
        _b.update()
        self.assertNotEqual(TestDB._raw_select(_b.id_)[0][1], _old_owner)

    def test_fetch_blob(self):
        _b = Blob.create(self.default_blob.owner)
        _fetched = Blob.fetch(_b.id_)
        self.assertEqual(_b.id_, _fetched.id_)

    def test_fetch_missing_blob(self):
        self.assertRaises(exceptions.BlobNotFoundError, Blob.fetch, 'not_existing')

    def test_delete_blob(self):
        self.default_blob.delete()
        self.assertFalse(TestDB._exists_in_db(self.default_blob.id_))

    def test_close(self):
        DAO.close()
        self.assertRaises(ProgrammingError, DAO.get_blob, 'x')

    def tearDown(self):
        DAO.close()
