===
API
===
.. module:: photoprysm

..
   You can either use the functions to interact with the API endpoints, such as:

   >>> with user_session(user, server_api) as session:
   >>>     album = photoprysm.albums.get_by_uid(session, server_api, 'example_uid')

   Or you can use the request function to manually put in the endpoints.

   >>> with user_session(user, server_api) as session:
   >>>     resp = photoprysm.request(session, server_api, 'GET', 'session')
   >>>     assert resp.json()['id'] == session.headers['Authorization'].removeprefix('Bearer ')

``photoprysm``
--------------

To interact with the Photoprism server in any capacity, you need an
access token. You can request this from the server either as a
:class:`User` or a :class:`Client`. To create either of these objects,
you will need to pass the base URL to the API. You can either use the
:func:`get_api_url` function or you can type the URL manually.

.. note:: Some API endpoints are restricted to :class:`User` sessions
          only. This includes all endpoints that need scope access to
          albums or photos.

.. autoclass:: User
   :members:

.. autoclass:: Client               
   :members:

.. note::
   ..  _client-auth-note:

   To create :class:`Client` sessions, you will need to generate the
   client ID and secret from the `Photoprism CLI`_. From within
   the Photoprism environment, run the following command:

   >>> photoprism clients add [client_name]

   with the name of the client in the placeholder. See
   Photoprism's `Client Credentials`_ page for more
   information.
          
.. autofunction:: user_session

>>> with user_session(user, server_api) as session:
>>>     # Do stuff

.. autofunction:: client_session                  

>>> with client_session(client, server_api) as session:
>>>     # Do stuff

.. autofunction:: get_api_url
.. autofunction:: request

Albums
------
.. note:: Despite the existence of an "albums" scope listed in the
          Photoprism documentation on Client `Authorization Scopes`_,
          interfacing with albums requires :class:`User` access. **It
          will not work using a Client session, even if you have given
          the Client the "albums" scope.**

Models
^^^^^^

These dataclasses hold information about various models to be used for
interfacing with. They do not have many (if any) methods and are
purely for holding data in a convenient way.

.. autoclass:: Album
   :members:
.. autoclass:: AlbumProperties
   :members:

Functions
^^^^^^^^^
.. autofunction:: get_albums
.. autofunction:: get_album_by_uid
.. autofunction:: create_album
.. autofunction:: delete_album
.. autofunction:: like_album
.. autofunction:: unlike_album
.. autofunction:: update_album
.. autofunction:: clone_album

Share Links
~~~~~~~~~~~

As of writing, the `Link Sharing`_ feature in the `latest Photoprism
release`_ is limited to sharing albums. Currently, **share links
cannot be generated for anything except albums.**

Models
""""""

.. autoclass:: ShareLink
   :members:
.. autoclass:: ShareLinkProperties
   :members:

Functions
"""""""""

.. autofunction:: get_album_share_links
.. autofunction:: add_album_share_link
.. autofunction:: parse_album_share_link
.. autofunction:: update_album_share_link   

Photos
------

Models
^^^^^^

.. autoclass:: Photo
   :members:
.. autoclass:: PhotoFile
   :members:
.. autoclass:: PhotoDetails
   :members:
.. autoclass:: PhotoProperties
   :members:

Functions
^^^^^^^^^

.. autofunction:: archive_photo
.. autofunction:: get_photos
.. autofunction:: get_photo_by_uid
..
  COMING SOON
  -.. autofunction:: get_by_file
.. autofunction:: update_photo
.. autofunction:: approve_photo
.. autofunction:: set_photo_primary_file
.. autofunction:: pop_photo_file
.. autofunction:: like_photo
.. autofunction:: unlike_photo
.. autofunction:: delete_photo
.. autofunction:: restore_photo
.. autofunction:: clear_photo_from_archive           
.. autofunction:: set_photo_as_private

.. Links
.. _`Photoprism CLI`: https://docs.photoprism.app/getting-started/docker-compose/#command-line-interface
.. _`Client Credentials`: https://docs.photoprism.app/developer-guide/api/auth/#client-credentials
.. _`requests.Session`: https://requests.readthedocs.io/en/latest/api/#requests.Session
.. _`requests.Response`: https://requests.readthedocs.io/en/latest/api/#requests.Response
.. _`requests.HTTPError`: https://requests.readthedocs.io/en/latest/api/#requests.HTTPError
.. _`Photoprism Search Filters`: https://docs.photoprism.app/user-guide/search/filters/
.. _`Authorization Scopes`: https://docs.photoprism.app/developer-guide/api/auth/#authorization-scopes
.. _`latest Photoprism release`: https://docs.photoprism.app/release-notes/#september-15-2024
.. _`Link Sharing`: https://docs.photoprism.app/user-guide/share/
