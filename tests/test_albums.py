#!/usr/bin/env python3
import pytest
import responses
from urllib.parse import urljoin
from dataclasses import asdict
from photoprysm import core
from photoprysm import albums

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

@pytest.fixture
def server_api():
    return core.get_api_url(
        netloc = 'localhost:2342',
        scheme = 'http'
    )

@pytest.fixture
def client():
    return core.Client(
        client_id = 'example_id',
        client_secret = 'example_secret'
    )

@pytest.fixture
def user():
    return core.User(
        username='admin',
        password='password'
    )

@pytest.fixture
def session(user, server_api):
    with responses.RequestsMock() as mock:
        mock.add(
            method = responses.POST,
            url = urljoin(server_api, 'session'),
            json = {
                "access_token": "example_token",
                "expires_in": 1209599,
                "id": "example_id",
                "provider": "local",
                "scope": "",
                "session_id": "example_session_id",
                "status": "success",
                "token_type": "Bearer",
                "user": {
                    "ID": 1,
                    "UID": "example_uid",
                    "AuthProvider": "local",
                    "AuthMethod": "",
                    "AuthID": "",
                    "Name": "admin",
                    "DisplayName": "Admin",
                    "Email": "",
                    "Role": "admin",
                    "Attr": "",
                    "SuperAdmin": True,
                    "CanLogin": True,
                }
            }
        )
        mock.add(
            method = responses.DELETE,
            url = urljoin(server_api, 'session'),
            json = {
                "session_id": "example_token",
                "status": "deleted"
            }
        )
        with core.user_session(user, server_api) as session:
            yield session

@responses.activate
def test_get_albums(user, server_api, session):
    responses.get(
        url = urljoin(server_api, 'albums?count=1'),
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
        albums_list = albums.get_by_query(session, server_api, 1)
        assert isinstance(albums_list, list)
