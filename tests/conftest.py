import re
import json
import pytest
from pathlib import Path


__ALBUMS__ = list(
    (Path(__file__).resolve().with_name(
        'mock_responses')/'album').glob('body*.json')
)


__PHOTOS__ = list(
    (Path(__file__).resolve().with_name(
        'mock_responses')/'photo').glob('body*.json')
)


__SUBJECTS__ = list(
    (Path(__file__).resolve().with_name(
        'mock_responses')/'subject').glob('body*.json')
)


__I18N_RESPONSE__ = list(
    (Path(__file__).resolve().with_name(
        'mock_responses')/'i18n_response').glob('body*.json')
)


def pytest_addoption(parser):
    parser.addoption(
        '--password',
        action='store',
        default='password',
        help='set user password')


@pytest.fixture
def user_password(request):
    return request.config.getoption('--password')


@pytest.fixture(params=__ALBUMS__)
def mock_album(request):
    body = json.loads(Path(request.param).read_text())
    mock = {'status': 200, 'json': body}    
    return mock

@pytest.fixture(params=__PHOTOS__)
def mock_photo(request):
    body = json.loads(Path(request.param).read_text())
    mock = {'status': 200, 'json': body}    
    return mock

@pytest.fixture(params=__I18N_RESPONSE__)
def mock_i18n_response(request):
    body = json.loads(Path(request.param).read_text())
    mock = {'status': 200, 'json': body}    
    return mock
