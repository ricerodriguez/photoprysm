"""Top-level package for Photoprysm."""
__author__ = """Rice Rodriguez"""
__email__ = 'victoriarice@protonmail.com'
__version__ = '0.0.1'

# Make the public members of the core accessible from the top
from .core import Client
from .core import User
from .core import user_session
from .core import client_session
from .core import get_api_url
from .core import request
from .core import start_index
from .core import start_import

# Make the API accessible from the top
from .api import albums
from .api import photos

# Make the models accessible from the top
from .models.albums import *
from .models.links import *
from .models.photos import *

# Add aliases from the top
from .api.albums import get as get_albums
from .api.albums import create as create_album
from .api.albums import get_by_uid as get_album_by_uid
from .api.albums import delete as delete_album
from .api.albums import like as like_album
from .api.albums import unlike as unlike_album
from .api.albums import update as update_album
from .api.albums import clone as clone_album
from .api.albums import get_share_links as get_album_share_links
from .api.albums import add_share_link as add_album_share_link
from .api.albums import parse_share_link as parse_album_share_link
from .api.albums import update_share_link as update_album_share_link

from .api.photos import get as get_photos
from .api.photos import get_by_uid as get_photo_by_uid
from .api.photos import archive as archive_photo
from .api.photos import restore as restore_photo
from .api.photos import clear_from_archive as clear_photo_from_archive
from .api.photos import delete as delete_photo
from .api.photos import update as update_photo
from .api.photos import approve as approve_photo
from .api.photos import set_primary_file as set_photo_primary_file
from .api.photos import set_private as set_photo_as_private
from .api.photos import pop_file as pop_photo_file
from .api.photos import like as like_photo
from .api.photos import unlike as unlike_photo
