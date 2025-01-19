===
API
===
.. module:: photoprysm

Quickstart
----------

To start, you need a :class:`User` or :class:`Client` instance.

>>> import photoprysm
>>> user = photoprysm.User('username', 'password')
>>> server_api = photoprysm.get_api_url('localhost:2342')

You can either login with the :class:`User` or :class:`Client` handle and log out later...

>>> session = user.login(server_api)
>>> # Do some stuff
>>> user.logout()

Or you can use the context manager so that it will log out automatically when you are done.

>>> with photoprysm.user_session(user, server_api) as session:
>>>     # Do some stuff
>>> # Logged out

..
   You can either use the functions to interact with the API endpoints, such as:

   >>> with user_session(user, server_api) as session:
   >>>     album = photoprysm.albums.get_by_uid(session, server_api, 'example_uid')

   Or you can use the request function to manually put in the endpoints.

   >>> with user_session(user, server_api) as session:
   >>>     resp = photoprysm.request(session, server_api, 'GET', 'session')
   >>>     assert resp.json()['id'] == session.headers['Authorization'].removeprefix('Bearer ')

Core
----

To interact with the Photoprism server in any capacity, you need an
access token. You can request this from the server either as a
:class:`User` or a :class:`Client`. To create either of these objects,
you will need to pass the base URL to the API. You can either use the
`photoprysm.get_api_url` function or you can type the URL manually.

.. note:: Some API endpoints are restricted to :class:`User` sessions
          only. This includes all endpoints that need scope access to
          albums or photos.

.. autoclass:: photoprysm.User
   :members:

.. autoclass:: photoprysm.Client               
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
          
   .. _`Photoprism CLI`: https://docs.photoprism.app/getting-started/docker-compose/#command-line-interface
   .. _`Client Credentials`: https://docs.photoprism.app/developer-guide/api/auth/#client-credentials

Albums
------
.. automodule:: photoprysm.albums
   :members:
