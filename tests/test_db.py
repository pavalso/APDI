import unittest

from sqlite3 import ProgrammingError, IntegrityError

from src import exceptions
from src.db import _DAO
from src.entities import Blob


@staticmethod
def _raw_select_blob(id):
    _DAO._cursor.execute('SELECT * FROM blobs WHERE id=?', (id,))
    return _DAO._cursor.fetchone()
    
@staticmethod
def _raw_insert_blob(id, owner, visibility):
    _DAO._cursor.execute('INSERT INTO blobs VALUES (?, ?, ?)', (id, owner, visibility))
    
@staticmethod
def _exists_in_db_blob(id):
    _r = _raw_select_blob(id)
    return bool(_r)

class TestDB(unittest.TestCase):

    def setUp(self):
        _DAO.connect(':memory:')
        self.default_id = '123456'
        self.default_owner = 'me'
        _raw_insert_blob(self.default_id, self.default_owner, 0)

    def test_new_blob(self):
        _blob = Blob.create(self.default_owner)
        self.assertTrue(_exists_in_db_blob(_blob.id_))
        self.assertEqual(_raw_select_blob(self.default_id)[1], self.default_owner)

    def test_fetch_blob(self):
        _fetched = Blob.fetch(self.default_id)
        self.assertEqual(self.default_id, _fetched.id_)

    def test_fetch_missing_blob(self):
        self.assertRaises(exceptions.BlobNotFoundError, Blob.fetch, 'not_existing')

    def test_id_readonly(self):
        _b = Blob.fetch(self.default_id)
        self.assertRaises(AttributeError, setattr, _b, 'id_', '123456')

    def test_unique_id(self):
        self.assertRaises(IntegrityError, _raw_insert_blob, self.default_id, None, None)
        self.assertRaises(exceptions.BlobAlreadyExistsError, _DAO.new_blob, self.default_id, None, None)

    def test_update_blob(self):
        _old_owner = self.default_owner
        _new_owner = _old_owner + '_new'
        Blob.update(self.default_id, owner=_new_owner)
        self.assertNotEqual(Blob.fetch(self.default_id).perms.owner, _old_owner)

    def test_delete_blob(self):
        Blob.delete(self.default_id)
        self.assertFalse(_exists_in_db_blob(self.default_id))

    def test_delete_missing_blob(self):
        self.assertRaises(exceptions.BlobNotFoundError, Blob.delete, 'not_existing')

    def test_get_blobs(self):
        blob = Blob.create(self.default_owner)
        self.assertIn(blob, Blob.fetch_user_blobs(self.default_owner))

    def test_close(self):
        _DAO.close()
        self.assertRaises(ProgrammingError, _DAO.get_blob, 'x')

    def tearDown(self):
        _DAO.close()

class TestPerms(unittest.TestCase):

    def setUp(self):
        _DAO.connect(':memory:')
        self.default_owner = 'me'

    def test_add_perms(self):
        blob = Blob.create(self.default_owner)
        blob.add_permissions('user')
        self.assertIsNotNone(_DAO.get_user_perms(blob.id_, 'user'))

    def test_read_perms(self):
        blob = Blob.create(self.default_owner)
        blob.add_permissions('user')
        self.assertTrue(blob.has_permissions('user'))

    def test_remove_perms(self):
        blob = Blob.create(self.default_owner)
        blob.add_permissions('user')
        blob.remove_permissions('user')
        self.assertIsNone(_DAO.get_user_perms(blob.id_, 'user'))

    def tearDown(self):
        _DAO.close()
