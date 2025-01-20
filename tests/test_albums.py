#!/usr/bin/env python3
import json
import pytest
import responses
from urllib.parse import urljoin
from dataclasses import asdict

from photoprysm import core
from photoprysm import albums
from .test_core import *

# This is from the demo API docs
__GET_ALBUMS_JSON = {
    "UID": "artiskh2amkzizr6",
    "ParentUID": "",
    "Thumb": "bf2a691e21b3403fc93a0e4ce2f33307cace2faf",
    "Slug": "berlin",
    "Type": "album",
    "Title": "Berlin",
    "Location": "",
    "Category": "",
    "Caption": "",
    "Description": "",
    "Notes": "",
    "Filter": "",
    "Order": "oldest",
    "Template": "",
    "Path": "",
    "State": "",
    "Country": "zz",
    "Year": 0,
    "Month": 0,
    "Day": 0,
    "Favorite": True,
    "Private": False,
    "PhotoCount": 7,
    "LinkCount": 0,
    "CreatedAt": "2023-04-22T14:07:29Z",
    "UpdatedAt": "2023-04-22T14:08:45.461421502Z",
    "DeletedAt": "0001-01-01T00:00:00Z"
}

@responses.activate
def test_create_albums(user, server_api, session):
    responses.post(
        url = urljoin(server_api, 'albums'),
        status = 200,
        json = __GET_ALBUMS_JSON)
    album = albums.create(session, server_api, 'TEST ALBUM')
    assert album.uid == __GET_ALBUMS_JSON['UID']

def test_real_create_albums(user, server_api):
    with core.user_session(user, server_api) as session:
        album = albums.create(session, server_api, 'TEST ALBUM')
    assert isinstance(album, albums.Album)

@responses.activate
def test_get_albums(user, server_api, session):
    responses.get(
        url = urljoin(server_api, 'albums?count=1&q=1'),
        status = 200,
        json = [__GET_ALBUMS_JSON]
    )
    albums_list = albums.get_by_query(session, server_api, 1)
    assert isinstance(albums_list, list)
    for k,v in {
        'uid': __GET_ALBUMS_JSON['UID'],
        'title': __GET_ALBUMS_JSON['Title'],
        'description': __GET_ALBUMS_JSON['Description'],
        'favorite': __GET_ALBUMS_JSON['Favorite'],
        'private': __GET_ALBUMS_JSON['Private']}.items():
        assert asdict(albums_list[0])[k] == v

# Make sure to use actual credentials in the user fixture with the actual URL
# in the server_api fixture
def test_real_get_albums(user, server_api):
    with core.user_session(user, server_api) as session:
        albums_list = albums.get_by_query(session, server_api, 'Test Album')
    assert albums_list[0].title == 'Test Album'

@responses.activate
def test_delete_album(user, server_api, session):
    responses.delete(
        url = urljoin(server_api, f'albums/{__GET_ALBUMS_JSON["UID"]}'),
        status = 200,
        json = __GET_ALBUMS_JSON)
    album = albums.Album(uid = __GET_ALBUMS_JSON['UID'])
    assert albums.delete(session, server_api, album) is None

# @responses.activate
# def test_get_share_links(user, server_api, session):
#     pass
