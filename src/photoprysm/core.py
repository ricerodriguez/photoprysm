import re
import json
import requests
import logging
from typing import Optional
from urllib.parse import urljoin
from dataclasses import dataclass, InitVar, field, asdict
import contextlib

logger = logging.getLogger(__name__)

@dataclass
class Client:
    '''
    Dataclass for holding authentication information for the application's Client credentials.

    :param client_id: Client ID generated from `Photoprism CLI`_. See the note below.
    :param client_secret: Client secret generated from `Photoprism CLI`_. See the note below.
    '''
    client_id: InitVar[str]
    client_secret: InitVar[str]
    auth: tuple[str] = field(init = False)

    def __post_init__(self, client_id: str, client_secret: str):
        self.auth = (client_id, client_secret)

    def login(self, server_api: str) -> requests.Session:
        '''Login to the server as a Client

        :param str server_api: Base URL to the server API
        :raises `requests.HTTPError`_: If the credentials are invalid or the server is not accepting requests
        :returns: Pre-configured Session with the authentication token for this Client
        :rtype: `requests.Session`_
        '''
        self.__server_api = server_api
        resp = requests.post(
            url = urljoin(server_api, 'oauth/token'),
            auth = client.auth)
        resp.raise_for_status()
        self._session = requests.Session()
        self._session.auth = resp.json()['access_token']

    def request(self, **kwargs) -> requests.Response:
        '''Send a request to the server as a Client'''
        session = getattr(self, '_session', None)
        if not session:
            logger.info('No current session open. Starting one now...')
            self.login(server_api = kwargs.get('server_api'))
            session = self._session
        resp = request(session = session, **kwargs)
        self.logout()
        return resp

    def logout(self) -> None:
        '''Logout of the server as a Client'''
        resp = requests.post(
            url = urljoin(server_api, 'oauth/revoke'),
            auth = self.auth)
        resp.raise_for_status()
        self._session.close()

@dataclass
class User:
    username: str
    password: str = field(repr = False)
    uid: str | None = None
    download_token: str | None = None

    def login(self, server_api: str) -> requests.Session:
        '''Login to the server as a User

        :param str server_api: Base URL to the server API
        :raises `requests.HTTPError`_: If the credentials are invalid or the server is not accepting requests
        :returns: Pre-configured Session with the authentication token for this User
        :rtype: `requests.Session`_
        '''
        url = urljoin(server_api, 'session')
        self._url  = url
        data = json.dumps({'username': self.username, 'password': self.password})
        # data = '{"username":"'+self.username+'", '
        # data += '"password":"'+self.password+'"}'
        resp = requests.post(
            url,
            data=data,
            cookies={},
            auth=())
        resp.raise_for_status()
        self._session = requests.Session()
        self._session.auth = PhotoprismAccessToken(resp.json()['id'])
        self.uid = self.uid or resp.json()['user']['UID']
        self.download_token = self.download_token or resp.json()['config']['downloadToken']
        return self._session

    def request(self, **kwargs) -> requests.Response:
        '''Send a request to the server as a User'''
        session = getattr(self, '_session', None)
        if not session:
            logger.info('No current session open. Starting one now...')
            self.login(server_api = kwargs.get('server_api'))
            session = self._session
        resp = request(session = session, **kwargs)
        self.logout()
        return resp

    def logout(self) -> None:
        '''Logout of the server as a User'''
        resp = self._session.delete(self._url)
        resp.raise_for_status()
        self.download_token = None
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
        server_api: str) -> requests.Session:
    '''Context manager for creating and deleting a User session.
    
    :param User user: User to create the session with
    :param str server_api: Base URL of the server API
    '''
    session = user.login(server_api)
    try:
        yield session
    finally:
        user.logout()

@contextlib.contextmanager
def client_session(client: Client, server_api: str):
    '''Context manager for creating and deleting a Client session.
    
    :param Client client: Client to create the session with
    :param str server_api: Base URL of the server API
    '''
    session = client.login(server_api)
    try:
        yield session
    finally:
        client.logout()
    
# Public
def get_api_url(
        netloc: Optional[str] = None,
        scheme: Optional[str] = None) -> str:
    '''
    Constructs the base URL for the Photoprism server API. 

    :param netloc: Network location. This is the hostname, with the port if necessary. Defaults to ``'localhost:2342'``.
    :param scheme: Scheme to send requests with. Must be either ``'http'`` or ``'https'``.
    '''
    u_netloc = netloc or 'localhost:2342'
    u_scheme = scheme or 'http'
    if not (u_scheme in ['http', 'https']):
        raise TypeError('Scheme must be set to either \'http\' or \'https\'.')
    return f'{u_scheme}://{u_netloc}/api/v1/'

def request(
        session: requests.Session,
        url: str,
        method: str,
        headers: Optional[dict[str,str]] = None,
        params: Optional[dict[str,str]] = None,
        data: Optional[dict[str,str]] = None) -> requests.Response:
    '''Send the request from a pre-configured `requests.Session`_ instance.

    :param session: requests.Session handle with the access token pre-configured
    :type session: `requests.Session`_
    :param url: URL to send the requests to
    :param method: Method of request, e.g. GET, POST, PUT, DELETE
    :param headers: Headers to send the request with. Defaults to {'accept:application/json', 'Content-Type':'application/json'}
    :param params: Dictionary, list of tuples or bytes to send in the query string for the Request.
    :param data: Data to send with the request
    :returns: Response from the server after sending the request
    :rtype: `requests.Response`_
    '''
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
