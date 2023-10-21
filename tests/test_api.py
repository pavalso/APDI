import os
import io
import shutil
import requests
import unittest
import json
import flask

from unittest.mock import patch

from src import services
from src import exceptions
from src.db import _DAO
from src import _route_app


@staticmethod
def _remove_test_dir():
    _st = os.getenv('STORAGE')
    if _st and os.path.isdir(_st):
        shutil.rmtree(_st)

class TestServices(unittest.TestCase):

    @classmethod
    def setUp(self) -> None:
        os.environ['STORAGE'] = '.tests_storage'
        _DAO.connect(':memory:')

    @patch('requests.get')
    def test_create_blob_unauthorized(self, mock_get):
        response = requests.Response()

        response.status_code = 401

        mock_get.return_value = response

        with self.assertRaises(exceptions.adiauth.UserNotExists):
            services.create_blob('user_token')

    @patch('requests.get')
    def test_create_blob(self, mock_get):
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            'user': 'testuser'
        }).encode()

        mock_get.return_value = response

        blob = services.create_blob('user_token')
        self.assertIsNotNone(blob)
        self.assertEqual(blob.visibility, services.Visibility.PRIVATE)

    @patch('requests.get')
    def test_update_blob_unauthorized(self, mock_get):
        response = requests.Response()

        response.status_code = 401

        mock_get.return_value = response

        with self.assertRaises(exceptions.adiauth.UserNotExists):
            services.update_blob('blob_id', 'user_token', io.BytesIO(b'blob data'))

    @patch('requests.get')
    def test_update_blob(self, mock_get):
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            'user': 'testuser'
        }).encode()

        mock_get.return_value = response

        blob = services.create_blob('user_token')

        raw = io.BytesIO(b'blob data')

        blob = services.update_blob(blob.id_, 'user_token', raw)

        raw.seek(0)
        blob.seek(0)

        self.assertEqual(blob.read(), raw.read())

    @patch('requests.get')
    def test_update_blob_long(self, mock_get):
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            'user': 'testuser'
        }).encode()

        mock_get.return_value = response

        blob = services.create_blob('user_token')

        raw = io.BytesIO(b'blob data' * 100000)

        blob = services.update_blob(blob.id_, 'user_token', raw)

        raw.seek(0)
        blob.seek(0)

        self.assertEqual(blob.read(), raw.read())

    @patch('requests.get')
    def test_update_unknown_blob(self, mock_get):
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            'user': 'testuser'
        }).encode()

        mock_get.return_value = response

        with self.assertRaises(exceptions.BlobNotFoundError):
            services.update_blob('blob_id', 'user_token', io.BytesIO(b'blob data'))

    @patch('requests.get')
    def test_delete_blob_unauthorized(self, mock_get):
        response = requests.Response()

        response.status_code = 401

        mock_get.return_value = response

        with self.assertRaises(exceptions.adiauth.UserNotExists):
            services.delete_blob('blob_id', 'user_token')

    @patch('requests.get')
    def test_delete_unknown_blob(self, mock_get):
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            'user': 'testuser'
        }).encode()

        mock_get.return_value = response

        with self.assertRaises(exceptions.BlobNotFoundError):
            services.delete_blob('blob_id', 'user_token')

    @patch('requests.get')
    def test_delete_blob(self, mock_get):
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            'user': 'testuser'
        }).encode()

        mock_get.return_value = response

        blob = services.create_blob('user_token')

        blob.close()

        services.delete_blob(blob.id_, 'user_token')

    @patch('requests.get')
    def test_get_user_blobs_unauthorized(self, mock_get):
        response = requests.Response()

        response.status_code = 401

        mock_get.return_value = response

        with self.assertRaises(exceptions.adiauth.UserNotExists):
            services.get_user_blobs('user_token')

    @patch('requests.get')
    def test_get_user_blobs(self, mock_get):
        response = requests.Response()

        response.status_code = 200
        response._content = json.dumps({
            'user': 'testuser'
        }).encode()

        mock_get.return_value = response

        blob = services.create_blob('user_token')

        blobs = services.get_user_blobs('user_token')

        self.assertEqual(len(blobs), 1)
        self.assertEqual(blobs[0], blob.id_)

    def tearDown(self) -> None:
        _remove_test_dir()
        _DAO.close()

class TestServer(unittest.TestCase):

    def setUp(self) -> None:
        self.app = flask.Flask('test_server')
        self.client = self.app.test_client()
        _route_app(self.app)

    def test_app_runs(self):
        res = self.client.get('/api/v1/status/')
        self.assertEqual(res.status_code, 200)
