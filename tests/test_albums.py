#!/usr/bin/env python3
import json
import pytest
import responses
from urllib.parse import urljoin
from dataclasses import asdict
from pprint import pprint as pp

from photoprysm import core
from photoprysm import albums

from .test_core import *

@responses.activate
def test_get_by_uid(mock_album, server_api, session):
    uid = mock_album['json']['UID']
    responses.get(
        url = urljoin(server_api, f'albums/{uid}'),
        **mock_album)
    album = albums.get_by_uid(session, server_api, uid)
    assert album.uid == uid

@pytest.mark.parametrize('favorite', [True, False])
@responses.activate
def test_create_album(mock_album, server_api, session, favorite):
    title = mock_album['json']['Title']
    req_kwargs = {'Title': title, 'Favorite': favorite}
    responses.post(
        url = urljoin(server_api, 'albums'),
        match=[responses.matchers.json_params_matcher(req_kwargs)],
        **mock_album)
    album = albums.create(session, server_api, title, favorite)
    assert album

@responses.activate
def test_delete_album(mock_album, mock_i18n_response, server_api, session):
    uid = mock_album['json']['UID']
    req_kwargs = {'albums': [uid]}
    responses.post(
        url = urljoin(server_api, 'batch/albums/delete'),
        match=[responses.matchers.json_params_matcher(req_kwargs)],
        **mock_i18n_response)
    album = albums.delete(session, server_api, uid)

@pytest.mark.parametrize(
    ('count', 'query', 'offset', 'order'),
    [(1, 'test', 0, 'name'),
     (2, None, None, None),
     (3, None, None, 'not real')]
)
@responses.activate
def test_get_albums(mock_album, server_api, session, count, query, offset, order):
    mock_album_list = {}
    mock_album_list['status'] = mock_album['status']
    mock_album_list['json'] = {}
    for i in range(0,count):
        mock_album_list['json'][i] = mock_album['json']
    responses.get(
        url = urljoin(server_api, 'albums'),
        **mock_album_list)

    if order not in albums.ValidSortOrderTypes and order is not None:
        with pytest.raises(ValueError) as err:
            albums_list = albums.get(session,
                                     server_api,
                                     count = count,
                                     query = query,
                                     offset = offset,
                                     order = order)
    else:
        albums_list = albums.get(session,
                                 server_api,
                                 count = count,
                                 query = query,
                                 offset = offset,
                                 order = order)

# @responses.activate
# def test_get_albums_q3(mock, server_api, session):
#     responses.get(
#         url = urljoin(server_api, 'albums?count=3'),
#         status = 200,
#         json = mock
#     )
#     albums_list = albums.get(session, server_api, count = 3)
#     assert len(albums_list) == 3

# def test_properties():
#     properties = albums.AlbumProperties(title = 'Test Album')
#     assert properties.json == json.dumps({'Title': 'Test Album'})

# @responses.activate
# def test_update_album(mock, server_api, session):
#     uid = mock['UID']
#     new_title = mock['Title']
#     responses.put(
#         url = urljoin(server_api, f'albums/{uid}'),
#         status = 200,
#         json = mock)
#     properties = albums.AlbumProperties(title = new_title)
#     updated_album = albums.update(session, server_api, uid, properties)
#     assert updated_album.title == new_title

# @responses.activate
# def test_clone_album(mock, server_api, session):
#     uid = mock['album']['UID']
#     cloned_uid = mock['added'][0]['AlbumUID']
#     responses.post(
#         url = urljoin(server_api, f'albums/{uid}/clone'),
#         status = 200,
#         json = mock)
#     clone = albums.clone(session, server_api, uid, [cloned_uid])
#     assert True

# @responses.activate
# def test_like_album(mock, server_api, session):
#     responses.post(
#         url = urljoin(server_api, f'albums/example/like'),
#         status = 200,
#         json = mock)
#     assert albums.like(session, server_api, 'example') == None

# @responses.activate
# def test_delete_album(mock, server_api, session):
#     uid = mock['UID']
#     responses.delete(
#         url = urljoin(server_api, f'albums/{uid}'),
#         status = 200,
#         json = mock)
#     album = albums.Album(uid = uid)
#     assert albums.delete(session, server_api, album) is None

# @responses.activate
# def test_add_album_link(mock, server_api, session):
#     uid = mock['UID']
#     responses.post(
#         url = urljoin(server_api, f'albums/{uid}/links'),
#         status = 200,
#         json = mock)
#     link = albums.add_share_link(session, server_api, uid)
#     assert json.loads(link.json) == mock

# @responses.activate
# def test_get_share_links(user, server_api, session):
#     pass
