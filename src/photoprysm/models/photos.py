from dataclasses import dataclass, field, InitVar
from typing import Optional

@dataclass
class Photo:
    '''Dataclass for holding data about a photo.
    '''
    uid: str
    json: Optional[dict[str,str]] = None

@dataclass
class PhotoFile:
    '''Dataclass for holding data about a file.
    '''
    uid: str
    photo_uid: str
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
    photo_id: Optional[int] = None,
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

