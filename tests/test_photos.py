#!/usr/bin/env python3
import json
import pytest
import responses
from urllib.parse import urljoin
from dataclasses import asdict

from photoprysm import core
from photoprysm import photos
from .test_core import *
from .mock_responses.loader import get_mock_response

@responses.activate
def test_get_photos(user, server_api, session):
    responses.get(
        url = urljoin(server_api, 'photos?count=1&quality=0'),
        status = 200,
        json = get_mock_response('get_photos_count1_quality0')
    )
    photos_list = photos.get(session, server_api, count = 1)
    assert isinstance(photos_list, list)

@responses.activate
def test_get_photo_by_uid(user, server_api, session):
    uid = get_mock_response('get_photo_by_uid')['UID']
    responses.get(
        url = urljoin(server_api, f'photos/{uid}'),
        status = 200,
        json = get_mock_response('get_photo_by_uid')
    )
    photo = photos.get_by_uid(session, server_api, uid)
    assert photo.uid == uid
