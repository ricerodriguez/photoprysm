# import io
from .base import ModelBase
from dataclasses import dataclass, field, fields, InitVar
from typing import Optional
from datetime import datetime

@dataclass
class PhotoFile(ModelBase, required = ['uid', 'photo_uid']):
    '''Dataclass for holding data about a file.

    :param uid:
    :param photo_uid:
    :param str name: (optional)
    :param str root: (optional)
    :param str hash: (optional)
    :param int size: (optional)
    :param bool primary: (optional)
    :param int time_index: (optional)
    :param str media_id: (optional)
    :param int media_utc: (optional)
    :param str instance_id: (optional)
    :param str codec: (optional)
    :param str file_type: (optional)
    :param str media_type: (optional)
    :param str mime: (optional)
    :param int width: (optional)
    :param int height: (optional)
    :param int orientation: (optional)
    :param str orientation_src: (optional)
    :param float aspect_ratio: (optional)
    :param str color_profile: (optional)
    :param str main_color: (optional)
    :param str colors: (optional)
    :param str luminance: (optional)
    :param int diff: (optional)
    :param int chroma: (optional)
    :param str software: (optional)
    :param int mod_time: (optional)
    :param datetime created_at: (optional)
    :param datetime created_in: (optional)
    :param datetime updated_at: (optional)
    :param list markers: (optional)
    '''
    uid: str
    photo_uid: str
    name: Optional[str] = None
    root: Optional[str] = None
    hash: Optional[str] = None
    size: Optional[int] = None
    primary: Optional[bool] = None
    time_index: Optional[int] = None
    media_id: Optional[str] = None
    media_utc: Optional[int] = None
    instance_id: Optional[str] = None
    codec: Optional[str] = None
    file_type: Optional[str] = None
    media_type: Optional[str] = None
    mime: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    orientation: Optional[int] = None
    orientation_src: Optional[str] = None
    aspect_ratio: Optional[float] = None
    color_profile: Optional[str] = None
    main_color: Optional[str] = None
    colors: Optional[str] = None
    luminance: Optional[str] = None
    diff: Optional[int] = None
    chroma: Optional[int] = None
    software: Optional[str] = None
    mod_time: Optional[int] = None
    created_at: Optional[datetime] = None
    created_in: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    markers: Optional[list] = None
    # stream: Optional[InitVar[bytes]] = None

    # def __post_init__(self, stream):
    #     self.stream = stream

    # @property
    # def stream() -> io.BytesIO:
    #     return self._stream

    # @stream.setter
    # def _ (value: bytes) -> None:
    #     self._stream = io.BytesIO(value)

@dataclass
class Photo(ModelBase, required = ['uid']):
    '''Dataclass for holding data about a photo.

    :param uid:
    :param str path: (optional)
    :param str name: (optional)
    :param str title: (optional)
    :param str description: (optional)
    :param str file_uid: (optional)
    :param str file_name: (optional)
    :param str file_hash: (optional)
    :param int width: (optional)
    :param int height: (optional)
    :param files: (optional)
    :type files: list[PhotoFile]
    '''
    uid: str
    path: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    file_uid: Optional[str] = None
    file_name: Optional[str] = None
    file_hash: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    files: Optional[list[PhotoFile]] = None

@dataclass
class PhotoDetails(ModelBase):
    '''Details from the PhotoProperties

    :param str artist: (optional)
    :param str artist_src: (optional)
    :param str copyright: (optional)
    :param str copyright_src: (optional)
    :param str keywords: (optional)
    :param str keywords_src: (optional)
    :param str license: (optional)
    :param str license_src: (optional)
    :param str notes: (optional)
    :param str notes_src: (optional)
    :param int photo_id: (optional)
    :param str subject: (optional)
    :param str subject_src: (optional)
    '''
    artist: Optional[str] = None,
    artist_src: Optional[str] = None,
    copyright: Optional[str] = None,
    copyright_src: Optional[str] = None,
    keywords: Optional[str] = None,
    keywords_src: Optional[str] = None,
    license: Optional[str] = None,
    license_src: Optional[str] = None,
    notes: Optional[str] = None,
    notes_src: Optional[str] = None,
    photo_id: Optional[int] = None,
    subject: Optional[str] = None,
    subject_src: Optional[str] = None

@dataclass
class PhotoProperties(ModelBase):
    '''Properties of the Photo object

    :param int altitude: (optional)
    :param int camera_id: (optional)
    :param str camera_src: (optional)
    :param int cell_accuracy: (optional)
    :param str cell_id: (optional)
    :param str country: (optional)
    :param int day: (optional)
    :param str description: (optional)
    :param str description_src: (optional)
    :param PhotoDetails details: (optional)
    :param str exposure: (optional)
    :param int f_number: (optional)
    :param bool favorite: (optional)
    :param int focal_length: (optional)
    :param int iso: (optional)
    :param int lat: (optional)
    :param int lens_id: (optional)
    :param int lng: (optional)
    :param int month: (optional)
    :param str original_name: (optional)
    :param bool panorama: (optional)
    :param str place_id: (optional)
    :param str place_src: (optional)
    :param bool private: (optional)
    :param bool scan: (optional)
    :param int stack: (optional)
    :param str taken_at: (optional)
    :param str taken_at_local: (optional)
    :param str taken_src: (optional)
    :param str time_zone: (optional)
    :param str title: (optional)
    :param str title_src: (optional)
    :param str type: (optional)
    :param str type_src: (optional)
    :param int year: (optional)
    '''
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

