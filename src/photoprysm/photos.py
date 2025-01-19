import os
import re
import enum
import logging
import requests
import datetime
from . import core
from . import albums
from urllib.parse import urljoin, quote as urlquote
from dataclasses import dataclass, field, InitVar
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class PhotoFile:
    '''Dataclass for holding data about a file.
    '''
    uid: str
    photo_uid: str
    json: Optional[dict[str,str]] = None

@dataclass
class Photo:
    '''Dataclass for holding data about a photo.
    '''
    uid: str
    json: Optional[dict[str,str]] = None

@dataclass
class PhotoDetails:
    '''Details from the PhotoProperties'''
    artist: Optional[str] = None,
    artist_src: Optional[str] = None,
    _copyright: Optional[InitVar[str]] = None,
    copyright: Optional[str] = field(init = False)
    copyright_src: Optional[str] = None,
    keywords: Optional[str] = None,
    keywords_src: Optional[str] = None,
    _license: Optional[InitVar[str]] = None,
    license: Optional[str] = field(init = False, default = None),
    license_src: Optional[str] = None,
    notes: Optional[str] = None,
    notes_src: Optional[str] = None,
    photo_id: Optional[int] = None = None,
    subject: Optional[str] = None,
    subject_src: Optional[str] = None

@dataclass
class PhotoProperties:
    '''Properties of the Photo object'''
    altitude: Optional[int] = None,
    camera_id: Optional[int] = None,
    camera_src: Optional[str] = None,
    cell_accuracy: Optional[int] = None,
    cell_id: Optional[str] = None,
    country: Optional[str] = None,
    day: Optional[int] = None,
    description: Optional[str] = None,
    description_src: Optional[str] = None,
    details: Optional[PhotoDetails] = None,
    exposure: Optional[str] = None,
    f_number: Optional[int] = None,
    favorite: Optional[bool] = None,
    focal_length: Optional[int] = None,
    iso: Optional[int] = None,
    lat: Optional[int] = None,
    lens_id: Optional[int] = None,
    lng: Optional[int] = None,
    month: Optional[int] = None,
    original_name: Optional[str] = None,
    panorama: Optional[bool] = None,
    place_id: Optional[str] = None,
    place_src: Optional[str] = None,
    private: Optional[bool] = None,
    scan: Optional[bool] = None,
    stack: Optional[int] = None,
    taken_at: Optional[str] = None,
    taken_at_local: Optional[str] = None,
    taken_src: Optional[str] = None,
    time_zone: Optional[str] = None,
    title: Optional[str] = None,
    title_src: Optional[str] = None,
    type: Optional[str] = None,
    type_src: Optional[str] = None,
    year: Optional[int] = None

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
        album: Optional[albums.Album] = None,
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
    
