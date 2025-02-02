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

@pytest.mark.parametrize(
    'count',
    list(range(1,5)))
@responses.activate
def test_restore(mock_i18n_response, mock_photo, server_api, session, count):
    uids = [mock_photo['json']['UID']] * count
    responses.post(
        url = urljoin(server_api, 'batch/photos/restore'),
        **mock_i18n_response)
    photos.restore(session, server_api, *uids)

@pytest.mark.parametrize(
    'count',
    list(range(1,5)))
@responses.activate
def test_clear_from_archive(mock_i18n_response, mock_photo, server_api, session, count):
    uids = [mock_photo['json']['UID']] * count
    responses.post(
        url = urljoin(server_api, 'batch/photos/delete'),
        **mock_i18n_response)
    photos.clear_from_archive(session, server_api, *uids)

@pytest.mark.parametrize(
    'count',
    list(range(1,5)))
@responses.activate
def test_delete(mock_i18n_response, mock_photo, server_api, session, count):
    uids = [mock_photo['json']['UID']] * count
    responses.post(
        url = urljoin(server_api, 'batch/photos/archive'),
        **mock_i18n_response)
    responses.post(
        url = urljoin(server_api, 'batch/photos/delete'),
        **mock_i18n_response)
    photos.delete(session, server_api, *uids)
