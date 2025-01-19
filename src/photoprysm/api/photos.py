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

def get_by_query(
        session: requests.Session,
        server_api: str,
        query: str,
        count: int = 1,
        merged: bool = True,
        quality: int = 0,
        offset: Optional[int] = None,
        order: Optional[str] = None,
        public: Optional[bool] = None,
        album: Optional[Album] = None,
        path: Optional[os.PathLike] = None,
        video: Optional[bool] = None) -> list[Photo]:
    '''Get list of Photos by query.

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param str query: Query to search for
    :param int count: (optional) Number of matches to return. Defaults to 1.
    :param bool merged: (optional) If True, consecutive files with the same photo ID are merged into a single result with the Files property containing the related files.
    :param int quality: (optional) Minimum quality score. Defaults to 0 to disable limit. Must be within range of 1-7.
    :param Album album: (optional) Album to search under
    :param os.PathLike path: (optional) Path to the photo
    :param bool is_video: (optional) True if result should be of type video
    :raises requests.HTTPError: If the request is poorly formed or the server is not accepting requests
    :returns: List of Photos that match from the query
    :rtype: list[Photo]
    '''
    raise NotImplementedError('This has not yet been implemented.')

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
    raise NotImplementedError('This has not yet been implemented.')
    
def update(
        session: requests.Session,
        server_api: str,
        photo: Photo,
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
    raise NotImplementedError('This has not yet been implemented.')
    
def approve(
        session: requests.Session,
        server_api: str,
        photo: Photo) -> Photo:
    '''Mark a Photo in review as approved

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to approve
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: Approved Photo
    :rtype: Photo
    '''
    raise NotImplementedError('This has not yet been implemented.')
    
def set_primary_file(
        session: requests.Session,
        server_api: str,
        photo: Photo,
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

def pop_file(
        session: requests.Session,
        server_api: str,
        photo: Photo,
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
        photo: Photo) -> None:
    '''Mark a Photo as a favorite

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to mark as favorite
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: None
    '''
    raise NotImplementedError('This has not yet been implemented.')

def unlike(
        session: requests.Session,
        server_api: str,
        photo: Photo) -> None:
    '''Unmark a Photo as a favorite

    :param requests.Session session: Pre-configured `requests.Session`_ object to send the request with
    :param str server_api: Base URL of the server API
    :param Photo photo: Photo to unmark as favorite
    :raises requests.HTTPError: If it runs into an HTTP error while sending the request
    :returns: None
    '''
    raise NotImplementedError('This has not yet been implemented.')
    
