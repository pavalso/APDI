#!/usr/bin/env python3

'''
    GenTraf: actions
'''

import json
import random
import tempfile
from pathlib import Path

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from agent import BLOBID_KEY, MULTIPART_FILE_KEY, BLOB_SIZES, PUBLIC_KEY
from agent.tools import generate_file
from agent.types import TestInfo, TestFailed

def test_upload_blob(test: TestInfo) -> None:
    '''POST to /api/v1/blobs/ with valid AuthToken'''
    response = requests.post(test.endpoint('/api/v1/blobs/'), headers=test.valid_headers, json={
        PUBLIC_KEY: 'public'
    })
    if response.status_code != 201:
        raise TestFailed(f'Expected status code 201, but got {response.status_code}')
    try:
        response_data = json.loads(response.text)
    except Exception as error:
        raise TestFailed(f'Cannot decode JSON data ({error})') from error
    try:
        blob_id = response_data[BLOBID_KEY]
    except KeyError:
        raise TestFailed(f'Response JSON does not have "{BLOBID_KEY}" key')
    test.new_blob(blob_id)

def test_replace_blob(test: TestInfo) -> None:
    '''PUT to /api/v1/blobs/<blobId> with valid AuthToken'''
    with tempfile.TemporaryDirectory() as workspace:
        blob_id = random.choice(test.stored_blobs)
        file_to_post = Path(generate_file(workspace, random.choice(BLOB_SIZES)))
        fd = open(file_to_post, 'rb')
        encoder = MultipartEncoder(fields={
            MULTIPART_FILE_KEY: (file_to_post.name, fd, 'text/plain')
        })
        headers = test.valid_headers
        headers.update({'Content-Type': encoder.content_type})
        response = requests.put(test.endpoint(f'/api/v1/blobs/{blob_id}'), headers=headers, data=encoder)
        if response.status_code != 204:
            raise TestFailed(f'Expected status code 204, but got {response.status_code}')
        fd.close()

def test_delete_blob(test: TestInfo) -> None:
    '''DELETE to /api/v1/blobs/<blobId> with valid AuthToken'''
    response = requests.delete(test.endpoint(f'/api/v1/blobs/{test.last_blob}'), headers=test.valid_headers)
    if response.status_code != 204:
        raise TestFailed(f'Expected status code 204, but got {response.status_code}')
    test.forget_blob(test.last_blob)

def test_get_blobs(test: TestInfo) -> None:
    '''GET to /api/v1/blobs/ with valid AuthToken'''
    response = requests.get(test.endpoint('/api/v1/blobs/'), headers=test.valid_headers)
    if response.status_code != 200:
        raise TestFailed(f'Expected status code 200, but got {response.status_code}')
    try:
        response_data = json.loads(response.text)
    except Exception as error:
        raise TestFailed(f'Cannot decode JSON data ({error})') from error

    if 'blobs' not in response_data:
        raise TestFailed(f'Response JSON does not have "blobs" key')
    remote_blobs = [blob['blobId'] for blob in response_data['blobs']]
    if set(remote_blobs) != set(test.stored_blobs):
        raise TestFailed(f'Blobs in remote and local are different')

def test_get_blob(test: TestInfo) -> None:
    '''GET to /api/v1/blobs/<blobId> with valid AuthToken'''
    response = requests.get(test.endpoint(f'/api/v1/blobs/{test.last_blob}'), headers=test.valid_headers)
    if response.status_code != 200:
        raise TestFailed(f'Expected status code 200, but got {response.status_code}')

def test_get_blob_anonymous(test: TestInfo) -> None:
    '''GET to /api/v1/blobs/<blobId> with anonymous access'''
    blob_id = test.public_blob
    if not blob_id:
        test_upload_blob(test)
        blob_id = test.last_blob
    response = requests.get(test.endpoint(f'/api/v1/blobs/{blob_id}'), headers={})
    if response.status_code != 200:
        raise TestFailed(f'Expected status code 200, but got {response.status_code}')

def test_switch_blob_private(test: TestInfo) -> None:
    '''PUT to /api/v1/blobs/<blobId>/visibility'''
    method = random.choice([requests.put])
    data = json.dumps({PUBLIC_KEY: "private"}).encode('UTF-8')
    blob_id = test.public_blob
    if not blob_id:
        test_upload_blob(test)
        blob_id = test.last_blob
    headers = {'Content-Type': 'application/json'}
    headers.update(test.valid_headers)
    response = method(test.endpoint(f'/api/v1/blobs/{blob_id}/visibility'), headers=headers, data=data)
    if response.status_code != 204:
        raise TestFailed(f'Expected status code 204, but got {response.status_code}')
    test.make_blob_private(blob_id)

def test_switch_blob_public(test: TestInfo) -> None:
    '''PUT to /api/v1/blobs/<blobId>/visibility'''
    method = random.choice([requests.put])
    data = json.dumps({PUBLIC_KEY: "public"}).encode('UTF-8')
    blob_id = test.private_blob
    if not blob_id:
        test_upload_blob(test)
        blob_id = test.last_blob
    headers = {'Content-Type': 'application/json'}
    headers.update(test.valid_headers)
    response = method(test.endpoint(f'/api/v1/blobs/{blob_id}/visibility'), headers=headers, data=data)
    if response.status_code != 204:
        raise TestFailed(f'Expected status code 204, but got {response.status_code}')
    test.make_blob_public(blob_id)

def test_get_blob_hash(test: TestInfo) -> None:
    '''GET to /api/v1/blobs/<blobId>/hash with valid AuthToken'''
    response = requests.get(test.endpoint(f'/api/v1/blobs/{test.last_blob}/hash'), headers=test.valid_headers, params={'type': random.choice(['md5', 'sha256'])})
    if response.status_code != 200:
        raise TestFailed(f'Expected status code 200, but got {response.status_code}')
