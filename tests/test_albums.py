#!/usr/bin/env python3
import json
import pytest
import responses
from urllib.parse import urljoin
from dataclasses import asdict

from photoprysm import core
from photoprysm import albums

from .test_core import *
from .mock_responses.loader import get_mock_response

@responses.activate
def test_create_album(mock, server_api, session):
    title = mock['Title']
    responses.post(
        url = urljoin(server_api, 'albums'),
        status = 200,
        json = mock)
    album = albums.create(session, server_api, title)
    assert album.uid == mock['UID']

def test_real_create_albums(user, server_api):
    mock = get_mock_response('create_album')
    title = mock['Title']
    with core.user_session(user, server_api) as session:
        album = albums.create(session, server_api, title)
    assert isinstance(album, albums.Album)

@responses.activate
def test_get_albums_q3(mock, server_api, session):
    responses.get(
        url = urljoin(server_api, 'albums?count=3'),
        status = 200,
        json = mock
    )
    albums_list = albums.get(session, server_api, count = 3)
    assert len(albums_list) == 3

def test_properties():
    properties = albums.AlbumProperties(title = 'Test Album')
    assert properties.json == json.dumps({'Title': 'Test Album'})

@responses.activate
def test_update_album(mock, server_api, session):
    uid = mock['UID']
    new_title = mock['Title']
    responses.put(
        url = urljoin(server_api, f'albums/{uid}'),
        status = 200,
        json = mock)
    properties = albums.AlbumProperties(title = new_title)
    updated_album = albums.update(session, server_api, uid, properties)
    assert updated_album.title == new_title

@responses.activate
def test_clone_album(mock, server_api, session):
    uid = mock['album']['UID']
    cloned_uid = mock['added'][0]['AlbumUID']
    responses.post(
        url = urljoin(server_api, f'albums/{uid}/clone'),
        status = 200,
        json = mock)
    clone = albums.clone(session, server_api, uid, [cloned_uid])
    assert True

@responses.activate
def test_like_album(mock, server_api, session):
    responses.post(
        url = urljoin(server_api, f'albums/example/like'),
        status = 200,
        json = mock)
    assert albums.like(session, server_api, 'example') == None

def test_real_get_albums(user, server_api):
    with core.user_session(user, server_api) as session:
        albums_list = albums.get(session, server_api, query = 'Test Album')
    assert albums_list[0].title == 'Test Album'

@responses.activate
def test_delete_album(mock, server_api, session):
    uid = mock['UID']
    responses.delete(
        url = urljoin(server_api, f'albums/{uid}'),
        status = 200,
        json = mock)
    album = albums.Album(uid = uid)
    assert albums.delete(session, server_api, album) is None

@responses.activate
def test_add_album_link(mock, server_api, session):
    uid = mock['UID']
    responses.post(
        url = urljoin(server_api, f'albums/{uid}/links'),
        status = 200,
        json = mock)
    link = albums.add_share_link(session, server_api, uid)
    assert json.loads(link.json) == mock

# @responses.activate
# def test_get_share_links(user, server_api, session):
#     pass
