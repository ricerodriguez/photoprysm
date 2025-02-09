import re
import json
import pytest
from pathlib import Path
from typing import Any
import requests
from responses.matchers import multipart_matcher

__MOCK_RESPONSE_BASE_PATH__ = Path(__file__).resolve().with_name(
    'mock_responses')

# __SUBJECTS__ = list(
#     (__MOCK_RESPONSE_BASE_PATH__/'subject').glob('body*.json')
# )

def pytest_addoption(parser):
    parser.addoption(
        '--password',
        action='store',
        default='password',
        help='set user password')

def mock_this(body: dict[str,Any]):
    return {'status': 200, 'json': body}

@pytest.fixture
def user_password(request):
    return request.config.getoption('--password')

@pytest.fixture(params=list(
    (__MOCK_RESPONSE_BASE_PATH__/'album').glob('body*.json')
))
def mock_album(request):
    body = json.loads(Path(request.param).read_text())
    return mock_this(body)

@pytest.fixture(params=list(
    (__MOCK_RESPONSE_BASE_PATH__/'photo').glob('body*.json')
))
def mock_photo(request):
    body = json.loads(Path(request.param).read_text())
    return mock_this(body)

@pytest.fixture
def mock_file_path():
    f = requests.get('https://picsum.photos/200', stream = True)
    p = Path('mock_file_path.jpg')
    p.write_bytes(f.content)
    yield p
    p.unlink()

@pytest.fixture(params=list(
    (__MOCK_RESPONSE_BASE_PATH__/'file').glob('body*.json')
))
def mock_file(request):
    body = json.loads(Path(request.param).read_text())
    mock = mock_this(body)
    # mock['match'] = [multipart_matcher({'files':
    return mock

@pytest.fixture
def mock_i18n_response(request):
    param = __MOCK_RESPONSE_BASE_PATH__/'i18n_response/body.json'
    body = json.loads(Path(param).read_text())
    return mock_this(body)

@pytest.fixture
def mock_session(request):
    param = __MOCK_RESPONSE_BASE_PATH__/'user_session/body.json'
    body = json.loads(Path(param).read_text())
    return mock_this(body)
