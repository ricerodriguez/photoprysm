"""Top-level package for Photoprism Python Client."""
__author__ = """Rice Rodriguez"""
__email__ = 'victoriarice@protonmail.com'
__version__ = '0.0.1'
from .core import *
from .albums import get_by_query as get_albums
from .albums import create as create_album
from .albums import get_by_uid as get_album
from .albums import delete as delete_album
from .albums import like as like_album
from .albums import unlike as unlike_album
