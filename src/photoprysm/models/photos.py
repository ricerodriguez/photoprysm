from .base import ModelBase
from dataclasses import dataclass, field, fields, InitVar
from typing import Optional

@dataclass
class PhotoFile(ModelBase, required = ['uid', 'photo_uid']):
    '''Dataclass for holding data about a file.
    '''
    uid: str
    photo_uid: str

@dataclass
class Photo(ModelBase, required = ['uid']):
    '''Dataclass for holding data about a photo.

    :param str uid:
    :param json: (optional)
    :type json: dict[str,str]
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
    :param str _copyright: (optional)
    :param str copyright_src: (optional)
    :param str keywords: (optional)
    :param str keywords_src: (optional)
    :param str _license: (optional)
    :param str license_src: (optional)
    :param str notes: (optional)
    :param str notes_src: (optional)
    :param int photo_id: (optional)
    :param str subject: (optional)
    :param str subject_src: (optional)
    '''
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

