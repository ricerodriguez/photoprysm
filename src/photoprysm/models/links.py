import datetime
from dataclasses import dataclass
from typing import Optional

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

