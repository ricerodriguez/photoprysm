import datetime

from dataclasses import dataclass
from typing import Optional, Self
from urllib.parse import urljoin

from .base import ModelBase

@dataclass
class ShareLink(ModelBase,
                required = [
                    'token',
                    'share_uid',
                    'slug',
                    'uid']):
    '''Data class for holding information about a share link

    :param token: Token of the share link, used to construct the URL
    :param share_uid: UID of the album the link points to
    :param slug: URL slug of the album the share link is for
    :param uid: UID of the share link itself
    :param str comment: (optional) Comment that was added when the share link was created
    :param str created_at: (optional) Time when the link was created
    :param str created_by: (optional) UID of the User who created this ShareLink
    :param int expires: (optional) Seconds until the link expires
    :param int max_views: (optional) Maximum number of views until the link expires
    :param str modified_at: (optional) Time when the link was last modified
    :param int perm: (optional) I literally do not know what this is.
    :param bool verify_password: (optional) Set to True to require user to verify password when they visit the share link
    :param int views: (optional) Number of views the share link has so far
    '''
    token: str
    share_uid: str
    slug: str
    uid: str
    comment: Optional[str] = None
    created_at: Optional[str] = None 
    modified_at: Optional[str] = None
    created_by: Optional[str] = None
    expires: Optional[int] = None
    max_views: Optional[int] = None
    perm: Optional[int] = None
    verify_password: Optional[bool] = None
    views: Optional[int] = None

    def __post_init__(self):
        if isinstance(self.created_at, str):
            # TODO: Convert to datetime.datetime
            pass
        if isinstance(self.modified_at, str):
            # TODO: Convert to datetime.datetime
            pass

    def get_url(self, host: Optional[str] = None, https: Optional[bool] = None) -> str:
        '''
        Construct the URL of the ShareLink.

        :param str host: (optional) Hostname where the Photoprism server is. Defaults to 'localhost'.
        :param bool https: (optional) Set to True to use https. Defaults to False.
        '''
        u_host = host or 'localhost'
        scheme = 'https' if https == True else 'http'
        base = f'{scheme}://{u_host}/s/'
        return urljoin(urljoin(base, self.token), self.slug)

@dataclass
class ShareLinkProperties(ModelBase):
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

