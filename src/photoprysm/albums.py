import re
import enum
import logging
import requests
import datetime
from . import core
from urllib.parse import urljoin, quote as urlquote
from dataclasses import dataclass, field, InitVar
from typing import Optional

logger = logging.getLogger(__name__)

ValidSortOrderTypes = enum.StrEnum(
    'ValidSortOrderTypes',
    'FAVORITES,NAME,TITLE,ADDED,EDITED')

@dataclass
class Album:
    uid: str
    title: str
    description: str
    favorite: bool
    private: bool
    # This is the rest of the JSON response
    json: Optional[dict[str,str]] = None

@dataclass
class AlbumSelection:
    albums: list[str]
    _all: bool = True
    files: Optional[list[str]] = None
    labels: Optional[list[str]] = None
    photos: Optional[list[str]] = None
    places: Optional[list[str]] = None
    subjects: Optional[list[str]] = None

    def asjsondict(self) -> dict[str,str]:
        d = asdict(self)
        d['all'] = d.pop('_all')
        return d

@dataclass
class AlbumProperties:
    '''This is for updating album properties.'''
    caption: Optional[str] = None
    category: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    favorite: Optional[bool] = False
    _filter: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    order: Optional[str] = None
    private: Optional[str] = None
    template: Optional[str] = None
    thumb: Optional[str] = None
    thumb_src: Optional[str] = None
    title: Optional[str] = None
    _type: Optional[str] = None

    def asjsondict(self) -> dict[str,str]:
        d0 = asdict(self)
        d1 = {}
        for k,v in d0.items():
            if v is None: continue
            elif k == '_filter': key = 'Filter'
            elif k == '_type': key = 'Type'
            elif k == 'thumb_src': key = 'ThumbSrc'
            else: key = k.title()
            d1[key] = v
        return d1

@dataclass
class ShareLink:
    comment: str
    created_at: datetime.datetime
    created_by: str
    expires: int
    max_views: int
    modified_at: datetime.datetime
    perm: int
    share_uid: str
    slug: str
    token: str
    uid: str
    verify_password: bool
    views: int

@dataclass
class ShareLinkProperties:
    can_comment: bool = True,
    can_edit: bool = True,
    expires: int = 0,
    max_views: int = 0,
    password: str = '',
    slug: str = '',
    token: str = ''

    def asjsondict(self) -> dict[str,str]:
        d0 = asdict(self)
        d1 = {}
        for k,v in d0.items():
            if v is None: continue
            elif k == 'can_comment': key = 'CanComment'
            elif k == 'can_edit': key = 'CanEdit'
            elif k == 'max_views': key = 'MaxViews'
            else: key = k.title()
            d1[key] = v
        return d1
    
def parse_to_album(**kwargs) -> Album:
    '''Convert a dict of key value pairs to an Album.'''
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    album_dict = {}
    for k, v in kwargs.items():
        key = re.sub('UID', 'Uid', k)
        key = pattern.sub('_', key).lower()
        if key in ['uid', 'title', 'description', 'favorite', 'private']:
            album_dict[key] = v
    return Album(json = kwargs, **album_dict)

def parse_to_share_link(**kwargs) -> ShareLink:
    '''Convert a dict of key value pairs to an ShareLink.'''
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    share_link_dict = {}
    for k, v in kwargs.items():
        key = re.sub('UID', 'Uid', k)
        key = pattern.sub('_', key).lower()
        share_link_dict[key] = v
    return ShareLink(**share_link_dict)

def get_by_query(
        session: requests.Session,
        server_api: str,
        count: int,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        q: Optional[str] = None) -> list[Album]:
    '''
    Get albums matching the provided query.

    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    :param count: Maximum number of results
    :param offset: Search result offset
    :param order: Sort order. Choose from favorites, name, title, added, or edited.
    :raises ValueError: If an invalid order is provided
    :raises requests.HTTPError: If the HTTP request fails
    '''
    # Build the URL with the query
    endpoint = 'albums'
    params = {'count': count}
    if offset is not None:
        params.update({'offset': offset})
    if order is not None:
        if order not in ValidSortOrderTypes:
            raise ValueError('Invalid value provided sort sort order.')
        params.update({'order': order})
    if q is not None:
        params.update({'q': q})
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'GET',
        params = params)
    rv = []
    for raw_album in resp.json():
        print(raw_album)
        rv.append(parse_to_album(**raw_album))
    return rv
            
def create(
        session: requests.Session,
        server_api: str,
        title: str,
        favorite: bool = False) -> Album:
    '''
    Creates a new album.

    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    :param title: Title of the new album
    :param favorite: Mark as favorite or not
    '''
    endpoint = 'albums'
    # Swagger Docs says these are the only two data supported
    data = {'Title': title, 'Favorite': favorite}
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST',
        data = data)
    return parse_to_album(**resp.json())

def get_by_uid(
        session: requests.Session,
        server_api: str,
        uid: str) -> Album:
    '''
    Gets the Album handle from the provided UID.

    :param client: Client to make the request from
    :param uid: UID of the album to get
    '''
    endpoint = f'albums/{urlquote(uid)}'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'GET')
    return parse_to_album(**resp.json())

def update(
        session: requests.Session,
        server_api: str,
        uid: str,
        properties: AlbumProperties) -> Album:
    '''
    Update the album properties.

    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    :param uid: UID of the album to update
    :param properties: Properties to update the album with
    '''
    endpoint = f'albums/{urlquote(uid)}'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'PUT',
        data = properties.asjsondict())
    return parse_to_album(**resp.json())

def delete(
        session: requests.Session,
        server_api: str,
        uid: str) -> None:
    '''
    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    '''
    endpoint = f'albums/{urlquote(uid)}'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE')

def clone(
        session: requests.Session,
        server_api: str,
        uid: str,
        selection: AlbumSelection) -> None:
    '''
    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    '''
    endpoint = f'albums/{urlquote(uid)}/clone'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST',
        data = selection.asjsondict()
    )

def like(
        session: requests.Session,
        server_api: str,
        uid: str) -> Album:
    '''
    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    '''
    endpoint = f'albums/{urlquote(uid)}/like'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST')
    return parse_to_album(**resp.json())

def unlike(
        session: requests.Session,
        server_api: str,
        uid: str) -> Album:
    '''
    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    '''
    endpoint = f'albums/{urlquote(uid)}/like'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE')
    return parse_to_album(**resp.json())

def get_share_links(
        session: requests.Session,
        server_api: str,
        uid: str) -> list[ShareLink]:
    '''
    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    '''
    endpoint = f'albums/{urlquote(uid)}/links'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'GET')
    rv = []
    for link in resp.json():
        rv.append(parse_to_share_link(**resp.json()))
    return rv

def add_share_link(
        session: requests.Session,
        server_api: str,
        uid: str) -> ShareLink:
    endpoint = f'albums/{urlquote(uid)}/links'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST')
    return ShareLink(parse_to_share_link(**resp.json()))
    
        
