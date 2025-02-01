import re
import enum
import json
import logging
import requests

from .. import core
from ..models.albums import Album, AlbumProperties
from ..models.links import ShareLink, ShareLinkProperties

from urllib.parse import urlparse, urljoin, quote as urlquote
from dataclasses import dataclass, field, InitVar
from typing import Optional

logger = logging.getLogger(__name__)

ValidSortOrderTypes = enum.StrEnum(
    'ValidSortOrderTypes',
    'FAVORITES,NAME,TITLE,ADDED,EDITED')

def get(
        session: requests.Session,
        server_api: str, *,
        # Keyword only
        count: int = 1,
        query: Optional[str] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None) -> list[Album]:
    '''
    Get albums matching the provided query.

    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    :param count: Maximum number of results
    :param query: Query to send to the server.
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
        rv.append(Album.fromjson(raw_album))
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
    return Album.fromjson(resp.json())

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
    return Album.fromjson(resp.json())

def update(
        session: requests.Session,
        server_api: str,
        album: Album | str,
        properties: AlbumProperties) -> Album:
    '''
    Update the album properties.

    :param requests.Session session: Session to make the request from
    :param str server_api: String with the base URL for the API
    :param Album|str album: Album to update
    :param AlbumProperties properties: Properties to update the album with
    :returns: Updated album
    :rtype: Album
    '''
    # Validate user input
    album_uid = core._extract_uid(album)
    if album_uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'albums/{album_uid}'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'PUT',
        data = properties.json)
    return Album.fromjson(resp.json())

def delete(
        session: requests.Session,
        server_api: str,
        *albums: Album | str) -> None:
    '''
    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    :param albums: One more Albums to delete
    '''
    uids = core._extract_uids(albums)
    if any([uid is None for uid in uids]):
        raise TypeError('One of the albums has neither a \'uid\' '
                        'attribute nor is it a str')
    selection = json.dumps({'albums': uids})
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
        album: Album | str,
        albums_to_copy: list[Album | str]) -> Album:
    '''
    Copies the photos from other albums to an existing album

    :param requests.Session session: Session to make the request from
    :param str server_api: String with the base URL for the API
    :param Album album: Album to which the pictures are to be added
    :param albums_to_copy: List of albums containing the photos that will be copied
    :type albums_to_copy: list[Album]
    '''
    # Validate user input
    uid = core._extract_uid(album)
    if uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    uids_to_copy = core._extract_uids(albums_to_copy)
    if any([uid is None for uid in uids_to_copy]):
        raise TypeError('One of the albums to copy has neither a \'uid\' '
                        'attribute nor is it a str')
    endpoint = f'albums/{uid}/clone'
    selection = json.dumps({'albums': uids_to_copy})
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST',
        data = selection
    )
    assert resp.json()['code'] == 200
    return Album.fromjson(resp.json()['album'])

def like(
        session: requests.Session,
        server_api: str,
        album: Album | str) -> None:
    '''
    Sets the favorite flag for an album.

    :param requests.Session session: Session to make the request from
    :param str server_api: String with the base URL for the API
    :param str uid: Album UID
    '''
    uid = core._extract_uid(album)
    if uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'albums/{uid}/like'
    core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST')

def unlike(
        session: requests.Session,
        server_api: str) -> None:
    '''
    Removes the favorite flag from an album.

    :param requests.Session session: Session to make the request from
    :param str server_api: String with the base URL for the API
    :param str uid: Album UID
    '''
    uid = core._extract_uid(album)
    if uid is None: raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'albums/{uid}/like'
    core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE')

def get_share_links(
        session: requests.Session,
        server_api: str,
        album: Album | str) -> list[ShareLink]:
    '''
    Returns all share links for the album matching the UID

    :param session: Session to make the request from
    :param server_api: String with the base URL for the API
    '''
    uid = core._extract_uid(album)
    if uid is None: raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'albums/{uid}/links'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'GET')
    rv = []
    for link in resp.json():
        rv.append(ShareLink.fromjson(resp.json()))
    return rv

def add_share_link(
        session: requests.Session,
        server_api: str,
        album: Album | str) -> ShareLink:
    uid = core._extract_uid(album)
    if uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'albums/{uid}/links'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST')
    return ShareLink.fromjson(resp.json())

def parse_share_link(
        session: requests.Session,
        server_api: str,
        url: str,
        album: Album | str) -> ShareLink:
    path_parts = urlparse(url).path.split('/')
    share_uid = core._extract_uid(album)
    if share_uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    token = path_parts[1]
    # We have to find the link UID
    links = get_share_links(session, server_api, album)
    for link in links:
        if link.token == token: return link

def update_share_link(
        session: requests.Session,
        server_api: str,
        share_link: ShareLink | str,
        link_props: ShareLinkProperties,
        album: Optional[Album | str] = None) -> ShareLink:
    '''Update share link with the given properties. Note that if you provide
    share_link as the URL itself, you must also provide the Album that the link
    is for.
    '''
    if isinstance(share_link, str) and album is None:
        raise ValueError('Must pass in which album the link is for if '
                         'supplying share_link as URL directly.')
    # First we need to get the share link if it was passed as URL
    if isinstance(share_link, str):
        link = parse_share_link(session, server_api, share_link, album)
    else: link = share_link
    endpoint = (f'albums/{link.share_uid}/'
                f'links/{link.uid}')
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'PUT',
        data = link_props.json
    )

def delete_share_link(
        session: requests.Session,
        server_api: str,
        share_link: ShareLink | str,
        album: Optional[Album | str] = None) -> None:
    if isinstance(share_link, str) and album is None:
        raise ValueError('Must pass in which album the link is for if '
                         'supplying share_link as URL directly.')
    # First we need to get the share link if it was passed as URL
    if isinstance(share_link, str):
        link = parse_share_link(session, server_api, share_link, album)
    else: link = share_link
    endpoint = (f'albums/{link.share_uid}/'
                f'links/{link.uid}')
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE'
    )
    return ShareLink.fromjson(resp.json())

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
