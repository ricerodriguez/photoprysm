import requests
import logging
from typing import Optional
from urllib.parse import urlparse, urljoin, ParseResult
from dataclasses import dataclass, InitVar, field
import contextlib

logger = logging.getLogger(__name__)

@dataclass
class ServerAPI:
    host: InitVar[str]
    port: InitVar[int]
    scheme: InitVar[str]
    url: ParseResult = field(init = False)

    def __post_init__(self, host: str, port: int, scheme: str):
        self.url = urlparse(f'{scheme}://{host}:{port!s}/api/v1')

@dataclass
class Client:
    client_id: InitVar[str]
    client_secret: InitVar[str]
    auth: tuple[str] = field(init = False)

    def __post_init__(self, client_id: str, client_secret: str):
        self.auth = (client_id, client_secret)

    def login(self, server_api: ServerAPI) -> requests.Session:
        self.__server_api = server_api
        url = get_api_url('oauth/token', server_api)
        resp = requests.post(
            url,
            auth = client.auth)
        resp.raise_for_status()
        self._session = requests.Session()
        self._session.auth = resp.json()['access_token']

    def request(self, **kwargs) -> requests.Response:
        session = getattr(self, '_session', None)
        if not session:
            logger.info('No current session open. Starting one now...')
            self.login(server_api = kwargs.get('server_api'))
            session = self._session
        resp = request(session = session, **kwargs)
        self.logout()
        return resp

    def logout(self) -> None:
        url = get_api_url('oauth/revoke', self.__server_api)
        resp = requests.post(
            url,
            auth = self.auth)
        resp.raise_for_status()
        self._session.close()

@dataclass
class User:
    username: str
    password: str = field(repr = False)
    uid: str | None = None

    def login(self, server_api: ServerAPI) -> requests.Session:
        url = get_api_url('session', server_api)
        self._url  = url
        data = '{"username":"'+self.username+'", '
        data += '"password":"'+self.password+'"}'
        resp = requests.post(
            url,
            data=data,
            cookies={},
            auth=())
        resp.raise_for_status()
        self._session = requests.Session()
        self._session.auth = PhotoprismAccessToken(resp.json()['id'])
        return self._session

    def request(self, **kwargs) -> requests.Response:
        session = getattr(self, '_session', None)
        if not session:
            logger.info('No current session open. Starting one now...')
            self.login(server_api = kwargs.get('server_api'))
            session = self._session
        resp = request(session = session, **kwargs)
        self.logout()
        return resp

    def logout(self) -> None:
        resp = self._session.delete(self._url)
        resp.raise_for_status()
        self._session.close()

class PhotoprismAccessToken(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request: requests.Request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request
    
@contextlib.contextmanager
def user_session(
        user: User,
        server_api: ServerAPI) -> requests.Session:
    session = user.login(server_api)
    try:
        yield session
    finally:
        user.logout()

@contextlib.contextmanager
def client_session(client: Client, server_api: ServerAPI):
    session = client.login(server_api)
    try:
        yield session
    finally:
        client.logout()
    
def get_api_url(
        endpoint: str,
        server_api: ServerAPI,
        download_token: Optional[str] = None):
    '''
    Build the url to the API as "<scheme>://<host>/api/v1/<endpoint>"
    :param endpoint: Endpoint to put at the end of the URL
    :param scheme: Scheme to use for the URL. Defaults to 'http'. Can only be 'http' or 'https'.
    :param host: Host where the PhotoPrism server is receiving API requests. Defaults to 'localhost'.
    :param port: Port to connect to the Photoprism server. Defaults to 2342.
    :param download_token: Optional download token to include if the response is expected to return a 
    '''
    u_scheme = server_api.url.scheme or 'http'
    # Validate scheme
    if u_scheme not in ['http', 'https']:
        raise TypeError('Scheme can only be \'http\' or \'https\'.')
    u_host = server_api.url.hostname or 'localhost'
    u_port = server_api.url.port or 2342
    base = f'{u_scheme}://{u_host}:{u_port!s}/api/v1/'
    url = urljoin(base, endpoint)
    if download_token is not None:
        if not url.endswith('/dl'):
            raise TypeError('Endpoint must be requesting to download a file '
                            '(ending in \'dl\') in order to add the download '
                            'token.')
        url = urljoin(url, f'?t={download_token}')
    return url

def request(
        session: requests.Session,
        server_api: ServerAPI,
        method: str,
        endpoint: str,
        headers: Optional[dict[str,str]] = None,
        params: Optional[dict[str,str]] = None,
        data: Optional[dict[str,str]] = None):
    '''
    Send the request from a user created session.
    :param user: User to make the session for the request from.
    :param method: Method of request, e.g. GET, POST, PUT, DELETE
    :param endpoint: API endpoint to request to
    :param params: (optional) Dictionary, list of tuples or bytes to send in the query string for the Request.
    :param data: (optional) Data to send with the request
    :returns requests.Response: Response received
    '''
    url = get_api_url(endpoint, server_api)
    u_headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    if headers: u_headers.update(headers)
    resp = session.request(
        method = method,
        url = url,
        params = params,
        data = data,
        headers = u_headers)
    # Raises the error if one occurred
    resp.raise_for_status()
    return resp
