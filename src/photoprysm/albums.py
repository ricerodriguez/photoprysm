import re
import enum
import json
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
    '''Dataclass for holding data about an album.

    :param str uid: UID of the album
    :param str title: (optional) Title of the album
    :param bool favorite: (optional) True if the current authenticated User has set the album as a favorite
    :param bool private: (optional) True if the album has been marked private
    :param description: (optional) Description for the album
    :type description: str or None
    :param json: (optional) Album response that was received as JSON data
    :type json: dict[str,str] or None
    '''
    uid: str
    title: Optional[str] = None
    favorite: Optional[bool] = None
    private: Optional[bool] = None
    description: Optional[str] = None
    json: Optional[dict[str,str]] = None

@dataclass
class AlbumProperties:
    '''This is for updating album properties.
    
    :param str|None caption: (optional)
    :param str|None category: (optional)
    :param str|None country: (optional)
    :param str|None description: (optional)
    :param bool|None favorite: (optional)
    :param str|None filter: (optional) Pass to the constructor as ``_filter``. Access as ``filter``.
    :param str|None location: (optional)
    :param str|None notes: (optional)
    :param str|None order: (optional)
    :param bool|None private: (optional)
    :param str|None template: (optional)
    :param str|None thumb: (optional)
    :param str|None thumb_src: (optional)
    :param str|None title: (optional)
    :param str|None type: (optional) Pass to the constructor as ``_type``. Access as ``type``.
    '''
    caption: Optional[str] = None
    category: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    favorite: Optional[bool] = None
    _filter: InitVar[Optional[str]] = None
    filter: Optional[str] = field(init = False)
    location: Optional[str] = None
    notes: Optional[str] = None
    order: Optional[str] = None
    private: Optional[bool] = None
    template: Optional[str] = None
    thumb: Optional[str] = None
    thumb_src: Optional[str] = None
    title: Optional[str] = None
    _type: InitVar[Optional[str]] = None
    type: Optional[str] = field(init = False)

    def __post_init__(self, _filter, _type):
        self.filter = _filter
        self.type = _type

@dataclass
class ShareLink:
    '''Data class for holding information about a share link

    :param str comment: Comment that was added when the share link was created
    :param str|datetime.datetime created_at: Time when the link was created
    :param str created_by:
    :param int expires: (optional) Seconds until the link expires
    :param int max_views: (optional) Maximum number of views until the link expires
    :param str|datetime.datetime modified_at: Time when the link was last modified
    :param int perm: ???
    :param str share_uid: UID of the share link
    :param str slug: URL slug of the album the share link is for
    :param str token: Token of the share link, used to construct the URL
    :param str uid: Album UID the share link is for
    :param bool verify_password: (optional) Set to True to require user to verify password when they visit the share link
    :param int views: (optional) Number of views the share link has so far
    '''
    comment: str
    created_at: str|datetime.datetime
    modified_at: str|datetime.datetime
    created_by: str
    share_uid: str
    slug: str
    token: str
    uid: str
    expires: int = 0
    max_views: int = 0
    perm: int = 0
    verify_password: bool = True
    views: int = 0

    def __post_init__(self):
        if isinstance(self.created_at, str):
            # TODO: Convert to datetime.datetime
            pass
        if isinstance(self.modified_at, str):
            # TODO: Convert to datetime.datetime
            pass
        

@dataclass
class ShareLinkProperties:
    '''Share link properties. This is for setting and updating properties of share links.
    
    :param bool can_comment: (optional) Allow visitors using the share link to comment.
    :param bool can_edit: (optional) Allow visitors using the share link to edit.
    :param int expires: (optional) Set expiration time for the link in seconds. Defaults to 0 to disable expiration.
    :param int max_views: (optional) Set maximum number of views before link is disabled. Defaults to 0 to disable limit.
    :param str password: (optional) Set a password that visitors must enter before they can view the media
    '''
    can_comment: Optional[bool] = None
    can_edit: Optional[bool] = None
    expires: Optional[int] = 0
    max_views: Optional[int] = 0
    slug: Optional[str] = None
    token: Optional[str] = None
    password: Optional[str] = None

def _parse_to_album(**kwargs) -> Album:
    '''Convert a dict of key value pairs to an Album.'''
    attrs = {}
    for k in ['UID', 'Title', 'Description', 'Favorite', 'Private']:
        if kwargs.get(k) is None: continue
        attrs[k.lower()] = kwargs.get(k)
    return Album(json = kwargs, **attrs)

def _parse_to_share_link(**kwargs) -> ShareLink:
    '''Convert a dict of key value pairs to an ShareLink.'''
    share_link_dict = core._askwargs(**kwargs)
    return ShareLink(**share_link_dict)

def get_by_query(
        session: requests.Session,
        server_api: str,
        query: str,
        count: int = 1,
        offset: Optional[int] = None,
        order: Optional[str] = None) -> list[Album]:
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
    _params = {'count': count, 'q': query, 'offset': offset, 'order': order}
    params = {}
    if order is not None:
        if order not in ValidSortOrderTypes:
            raise ValueError('Invalid value provided sort sort order.')
        _params.update({'order': order})
    for k,v in _params.items():
        if v is None: continue
        params[k] = v
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'GET',
        params = params)
    rv = []
    for raw_album in resp.json():
        print(raw_album)
        rv.append(_parse_to_album(**raw_album))
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
    :returns: Newly created Album
    :rtype: Album
    '''
    endpoint = 'albums'
    # Swagger Docs says these are the only two data supported
    data = json.dumps({'Title': title, 'Favorite': favorite})
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST',
        data = data)
    return _parse_to_album(**resp.json())

def get_by_uid(
        session: requests.Session,
        server_api: str,
        uid: str) -> Album:
    '''
    Gets the Album handle from the provided UID.

    :param client: Client to make the request from
    :param uid: UID of the album to get
    :returns: Album with matching UID
    :rtype: Album
    '''
    endpoint = f'albums/{urlquote(uid)}'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'GET')
    return _parse_to_album(**resp.json())

def update(
        session: requests.Session,
        server_api: str,
        album: Album,
        properties: AlbumProperties) -> Album:
    '''
    Update the album properties.

    :param requests.Session session: Session to make the request from
    :param str server_api: String with the base URL for the API
    :param Album album: Album to update
    :param AlbumProperties properties: Properties to update the album with
    :returns: Updated album
    :rtype: Album
    '''
    endpoint = f'albums/{urlquote(album.uid)}'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'PUT',
        data = core.asjson(properties))
    return _parse_to_album(**resp.json())

def delete(
        session: requests.Session,
        server_api: str,
        album: Album) -> None:
    '''
    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    :param Album album: Album to delete
    '''
    endpoint = f'albums/{urlquote(album.uid)}'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE')

def batch_delete(
        session: requests.Session,
        server_api: str,
        albums: list[Album]) -> None:
    '''
    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    :param albums: List of albums to delete
    :type albums: list[Album]
    '''
    selection = json.dumps({'albums': [album.uid for album in albums]})
    endpoint = 'batch/albums/delete'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE',
        data = selection
    )

def clone(
        session: requests.Session,
        server_api: str,
        album: Album,
        albums_to_copy: list[Album]) -> None:
    '''
    Copies the photos from other albums to an existing album

    :param requests.Session session: Session to make the request from
    :param str server_api: String with the base URL for the API
    :param Album album: Album to which the pictures are to be added
    :param albums_to_copy: List of albums containing the photos that will be copied
    :type albums_to_copy: list[Album]
    '''
    endpoint = f'albums/{urlquote(album.uid)}/clone'
    selection = json.dumps(
        {'albums': [album_to_copy.uid for album_to_copy in albums_to_copy]}
    )
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST',
        data = selection
    )

def like(
        session: requests.Session,
        server_api: str,
        album: Album) -> Album:
    '''
    Sets the favorite flag for an album.

    :param requests.Session session: Session to make the request from
    :param str server_api: String with the base URL for the API
    :param str uid: Album UID
    '''
    endpoint = f'albums/{urlquote(album.uid)}/like'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST')
    return _parse_to_album(**resp.json())

def unlike(
        session: requests.Session,
        server_api: str) -> Album:
    '''
    Removes the favorite flag from an album.

    :param requests.Session session: Session to make the request from
    :param str server_api: String with the base URL for the API
    :param str uid: Album UID
    '''
    endpoint = f'albums/{urlquote(album.uid)}/like'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE')
    return _parse_to_album(**resp.json())

def get_share_links(
        session: requests.Session,
        server_api: str,
        album: Album) -> list[ShareLink]:
    '''
    Returns all share links for the album matching the UID

    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    '''
    endpoint = f'albums/{urlquote(album.uid)}/links'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'GET')
    rv = []
    for link in resp.json():
        rv.append(_parse_to_share_link(**resp.json()))
    return rv

def add_share_link(
        session: requests.Session,
        server_api: str,
        album: Album) -> ShareLink:
    endpoint = f'albums/{urlquote(album.uid)}/links'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST')
    return ShareLink(_parse_to_share_link(**resp.json()))

def update_share_link(
        session: requests.Session,
        server_api: str,
        share_link: ShareLink,
        link_props: ShareLinkProperties) -> ShareLink:
    endpoint = (f'albums/{urlquote(share_link.uid)}/'
                f'links/{urlquote(share_link.share_uid)}')
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'PUT',
        data = core.asjson(linkprops)
    )
    return ShareLink(_parse_to_share_link(**resp.json()))

def delete_share_link(
        session: requests.Session,
        server_api: str,
        share_link: ShareLink) -> None:
    endpoint = (f'albums/{urlquote(share_link.uid)}/'
                f'links/{urlquote(share_link.share_uid)}')
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE'
    )
    return ShareLink(_parse_to_share_link(**resp.json()))

def get_cover_image(
        user: core.User,
        server_api: str,
        album: Album):
    '''Get the album cover image. Note that because this requires a download
    token, we have to pass the handle to the User instead of just the Session
    like usual.

    :param core.User user: User to send the request from
    :param str server_api: Base URL to the server API
    :param Album album: Album to get the cover image of
    '''
    raise NotImplementedError('This has not been implemented yet.')
