import os
import re
import enum
import logging
import requests

from .. import core
from ..models.albums import Album, AlbumProperties
from ..models.photos import Photo, PhotoFile, PhotoDetails, PhotoProperties

from urllib.parse import urljoin, quote as urlquote
from typing import Optional

logger = logging.getLogger(__name__)

def get(
        session: requests.Session,
        server_api: str,
        *,
        count: int = 1,
        quality: int = 0,
        merged: Optional[bool] = None,
        query: Optional[str] = None,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        public: Optional[bool] = None,
        album: Optional[Album | str] = None,
        path: Optional[os.PathLike] = None,
        video: Optional[bool] = None) -> list[Photo]:
    '''Get list of Photos by query.

    :param session: Pre-configured `requests.Session`_ object to send the request with
    :param server_api: Base URL of the server API
    :param int count: (optional) Number of matches to return. Defaults to 1.
    :param int quality: (optional) Minimum quality score. Defaults to 0 to disable limit. Must be within range of 1-7.
    :param bool merged: (optional) If True, consecutive files with the same photo ID are merged into a single result with the Files property containing the related files.
    :param str query: (optional) Query to search for. See documentation for valid `Photoprism Search Filters`_.
    :param int offset: (optional) Search result offset
    :param str order: (optional) Sort order. Choose from favorites, name, title, added, or edited.
    :param bool public: (optional) Limit searches to those with public access.
    :param Album|str album: (optional) Album to search under. You can provide a handle to an Album instance or you can provide the UID as a string directly.
    :param os.PathLike path: (optional) Path to the photo
    :param bool video: (optional) True if result should be of type video
    :raises requests.HTTPError: If the request is poorly formed or the server is not accepting requests
    :returns: List of Photos that match from the query
    '''
    # Validate user input
    if quality is not None and quality not in range(0,7):
        raise TypeError('Quality is out of range. It must be between 0 and 7.')
    _merged = None if merged is None else str(merged).lower()
    _params = {'count': count,
               'quality': quality,
               'q': query,
               'merged': _merged,
               's': core._extract_uid(album),
               'path': None if path is None else str(path),
               'video': video}
    params = {}
    for k,v in _params.items():
        if v is None: continue
        params[k] = v
    resp = core.request(
        session = session,
        url = urljoin(server_api, 'photos'),
        method = 'GET',
        params = params)
    rv = []
    for raw_photo in resp.json():
        rv.append(Photo.fromjson(raw_photo))
    return rv

def get_by_uid(
        session: requests.Session,
        server_api: str,
        uid: str) -> Photo:
    '''Get Photo handle by UID.

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param str uid: UID of the Photo to retrieve
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: Photo with matching UID
    :rtype: Photo
    '''
    endpoint = f'photos/{urlquote(uid)}'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'GET')
    return Photo.fromjson(resp.json())

def get_by_file(
        session: requests.Session,
        server_api: str,
        _file: PhotoFile) -> Photo:
    # /files/{sha-1 hash}
    raise NotImplementedError('This has not yet been implemented.')    
    
def archive(
        session: requests.Session,
        server_api: str,
        *photos: Photo | str) -> None:
    '''Archive one or more photos.

    :param session: Pre-configured `requests.Session`_ object to send the request with
    :param server_api: Base URL of the server API
    :param photos: One or more Photo objects or UIDs to archive
    '''
    # Validate user input
    uids = core._extract_uids(photos)
    if any([uid is None for uid in uids]):
        raise TypeError('One of the photos has neither a \'uid\' '
                        'attribute nor is it a str')
    core.request(
        session = session,
        url = urljoin(server_api, 'batch/photos/archive'),
        method = 'POST',
        data = json.dumps({'photos': uids}))

def restore(
        session: requests.Session,
        server_api: str,
        *photos: Photo | str) -> None:
    # Validate user input
    uids = core._extract_uids(photos)
    if any([uid is None for uid in uids]):
        raise TypeError('One of the photos has neither a \'uid\' '
                        'attribute nor is it a str')
    endpoint = 'batch/photos/restore'
    data = json.dumps({'photos': uids})
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST',
        data = data)

def clear_from_archive(
        session: requests.Session,
        server_api: str,
        *photos: Photo | str) -> None:
    '''Permanently delete one or more Photos from the archive.

    :param session: Pre-configured `requests.Session`_ object to send the request with
    :param server_api: Base URL of the server API
    :param photos: One or more Photos to remove from the archive
    '''
    # Validate user input
    uids = core._extract_uids(photos)
    if any([uid is None for uid in uids]):
        raise TypeError('One of the photos has neither a \'uid\' '
                        'attribute nor is it a str')
    data = json.dumps({'photos': uids})
    resp = core.request(
        session = session,
        url = urljoin(server_api, 'batch/photos/delete'),
        method = 'POST',
        data = data)

def delete(
        session: requests.Session,
        server_api: str,
        *photos: Photo | str) -> None:
    # Validate user input
    uids = core._extract_uids(photos)
    if any([uid is None for uid in uids]):
        raise TypeError('One of the photos has neither a \'uid\' '
                        'attribute nor is it a str')
    batch_archive(session, server_api, uids)
    data = json.dumps({'photos': uids})
    resp = core.request(
        session = session,
        url = urljoin(server_api, 'batch/photos/delete'),
        method = 'POST',
        data = data)

def update(
        session: requests.Session,
        server_api: str,
        photo: Photo | str,
        photo_props: PhotoProperties) -> Photo:
    '''Update a photo with new properties

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to update
    :param PhotoProperties photo_props: Properties to update the Photo with
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: Updated Photo
    :rtype: Photo
    '''
    # Validate user input
    uid = core._extract_uid(photo)
    if uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'photos/{uid}'
    data = json.dumps(photo_props.json)
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'PUT',
        data = data)
    return Photo.fromjson(resp.json())
    
def approve(
        session: requests.Session,
        server_api: str,
        photo: Photo | str) -> Photo:
    '''Mark a Photo in review as approved

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to approve
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: Approved Photo
    :rtype: Photo
    '''
    # Validate user input
    uid = core._extract_uid(photo)
    if uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'photos/{uid}/approve'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST')
    return [Photo(photo) for photo in resp.json()['photo']][0]
    
def set_primary_file(
        session: requests.Session,
        server_api: str,
        photo: Photo | str,
        _file: PhotoFile) -> Photo:
    '''Set the primary file for the Photo

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to set primary file for
    :param PhotoFile _file: File to set as primary for the Photo
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: Updated Photo
    :rtype: Photo
    '''
    raise NotImplementedError('This has not yet been implemented.')

def set_private(
        session: requests.Session,
        server_api: str,
        *photos: Photo | str) -> None:
    '''Set multiple photos as private.

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param photos: Photos to set as private
    :type photos: list[Photo]
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: None
    '''
    # Validate user input
    uids = core._extract_uids(photos)
    if any([uid is None for uid in uids]):
        raise TypeError('One of the photos has neither a \'uid\' '
                        'attribute nor is it a str')
    endpoint = f'batch/photos/private'
    data = json.dumps({'photos': uids})
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST',
        data = data)

def pop_file(
        session: requests.Session,
        server_api: str,
        photo: Photo | str,
        _file: PhotoFile) -> PhotoFile:
    '''Pop a file off the stack for the Photo

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to get the file from
    :param PhotoFile _file: File to pop off the stack
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: File that was popped off the stack
    :rtype: PhotoFile
    '''
    raise NotImplementedError('This has not yet been implemented.')

def like(
        session: requests.Session,
        server_api: str,
        photo: Photo | str) -> None:
    '''Mark a Photo as a favorite

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to mark as favorite
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: None
    '''
    uid = core._extract_uid(photo)
    if uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'photos/{uid}/like'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'POST')

def unlike(
        session: requests.Session,
        server_api: str,
        photo: Photo | str) -> None:
    '''Unmark a Photo as a favorite

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to unmark as favorite
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: None
    '''
    uid = core._extract_uid(photo)
    if uid is None:
        raise TypeError('Must pass in UID as str or as attribute of object')
    endpoint = f'photos/{uid}/like'
    resp = core.request(
        session = session,
        url = urljoin(server_api, endpoint),
        method = 'DELETE')
    
