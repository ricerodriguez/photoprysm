from .base import ModelBase
from dataclasses import dataclass, InitVar, field
from typing import Optional, Self, Any

@dataclass
class Album(ModelBase, required = ['uid']):
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
        
@dataclass
class AlbumProperties(ModelBase):
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
