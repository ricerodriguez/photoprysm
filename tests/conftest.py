import pytest

def pytest_addoption(parser):
    parser.addoption(
        '--password',
        action = 'store',
        default = 'password',
        help = 'set user password')

@pytest.fixture
def user_password(request):
    return request.config.getoption('--password')
        
