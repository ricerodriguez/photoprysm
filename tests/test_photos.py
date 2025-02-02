#!/usr/bin/env python3
import json
import pytest
import responses
from urllib.parse import urljoin
from dataclasses import asdict

from photoprysm import core
from photoprysm import photos

from .test_core import *

@responses.activate
def test_get_by_uid(mock_photo, server_api, session):
    uid = mock_photo['json']['UID']
    responses.get(
        url = urljoin(server_api, f'photos/{uid}'),
        **mock_photo)
    photo = photos.get_by_uid(session, server_api, uid)
    assert photo.uid == uid
    
@pytest.fixture
def mock_approve_photo(mock_photo):
    rv = {}
    rv['status'] = mock_photo['status']
    rv['json'] = {'photo': mock_photo['json']}
    return rv

@responses.activate
def test_archive(mock_approve_photo, server_api, session):
    photo = mock_approve_photo['json']['photo']['UID']
    responses.post(
        url = urljoin(server_api, 'batch/photos/archive'),
        **mock_approve_photo)
    photos.archive(session, server_api, photo)
# @responses.activate
# def test_get_photos_count1_quality0(mock, server_api, session):
#     responses.get(
#         url = urljoin(server_api, 'photos?count=1&quality=0'),
#         status = 200,
#         json = mock
#     )
#     photos_list = photos.get(session, server_api, count = 1)
#     assert isinstance(photos_list, list)

# @responses.activate
# def test_get_photo_by_uid(mock, server_api, session):
#     uid = mock['UID']
#     responses.get(
#         url = urljoin(server_api, f'photos/{uid}'),
#         status = 200,
#         json = mock
#     )
#     photo = photos.get_by_uid(session, server_api, uid)
#     assert photo.uid == uid

# @responses.activate
# def test_approve_photo(mock, server_api, session):
#     photo_uid = mock['photo']['UID']
#     responses.post(
#         url = urljoin(server_api, f'photos/{photo_uid}/approve'),
#         status = 200,
#         json = mock
#     )
#     photo = photoprysm.Photo(uid = photo_uid)
#     photos.approve(session, server_api, photo)
