#!/usr/bin/env python3
import pytest
import responses
from urllib.parse import urljoin
from photoprysm import core
from pathlib import Path
# from .mock_responses.loader import get_mock_response

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
def user(user_password):
    return core.User(
        username='admin',
        password=user_password
    )

@pytest.fixture
def session(user, server_api):
    with responses.RequestsMock() as mock:
        mock.add(
            method = responses.POST,
            url = urljoin(server_api, 'session'),
            json = {
                "access_token": "example_token",
                "config": {
                    "mode": "user",
                    "name": "PhotoPrism",
                    "about": "PhotoPrism®",
                    "edition": "plus",
                    "tier": 1,
                    "membership": "ce",
                    "customer": "",
                    "mapKey": "",
                    "downloadToken": "example_dl_token",
                    "previewToken": "example_pv_token"
                },
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

@pytest.mark.parametrize('count', list(range(0,3)))
@responses.activate
def test_import(mock_i18n_response, mock_album, server_api, session, count):
    albums_list = [mock_album['json']['UID']] * count
    path = '/path/to/import'
    req_kwargs = {
        'albums': albums_list,
        'move': False,
        'path': path
    }
    responses.post(
        url = urljoin(server_api, 'import'),
        match=[responses.matchers.json_params_matcher(req_kwargs)],
        **mock_i18n_response)
    core.start_import(session, server_api, path, False, *albums_list)
