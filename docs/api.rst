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

.. autofunction:: get_api_url

.. autofunction:: request
      

.. note::
   ..  _client-auth-note:

   To create :class:`Client` sessions, you will need to generate the
   client ID and secret from the `Photoprism CLI`_. From within
   the Photoprism environment, run the following command:

   >>> photoprism clients add [client_name]

   with the name of the client in the placeholder. See
   Photoprism's `Client Credentials`_ page for more
   information.
          
   .. _`Photoprism CLI`: https://docs.photoprism.app/getting-started/docker-compose/#command-line-interface
   .. _`Client Credentials`: https://docs.photoprism.app/developer-guide/api/auth/#client-credentials

``photoprysm.albums``
---------------------
.. module:: photoprysm.albums

All functions and dataclasses for interfacing with the album API
endpoints can be found in the ``photoprysm.albums`` module.

.. autoclass:: Album
   :members:

.. autoclass:: AlbumProperties
   :members:

.. Links
.. _`requests-session`: https://requests.readthedocs.io/en/latest/api/#requests.Session
