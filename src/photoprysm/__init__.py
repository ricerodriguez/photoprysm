"""Top-level package for Photoprism Python Client."""
__author__ = """Rice Rodriguez"""
__email__ = 'victoriarice@protonmail.com'
__version__ = '0.0.1'
from .core import *

# Make the API accessible from the top
from .api import albums
from .api import photos

# Make the models accessible from the top
from .models.albums import *
from .models.links import *
from .models.photos import *

# Add aliases from the top
from .api.albums import get_by_query as get_albums_by_query
from .api.albums import create as create_album
from .api.albums import get_by_uid as get_album_by_uid
from .api.albums import delete as delete_album
from .api.albums import like as like_album
from .api.albums import unlike as unlike_album
