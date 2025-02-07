=====
Usage
=====

Requirements
------------

1. You must have a working instance of Photoprism up and running. See
   Photoprism's `Getting Started`_ page for steps on doing that.
2. You must have the login credentials for a user with access to the
   media on the Photoprism server. 

.. tip:: You can use your admin credentials, but you may want to
   create a user account specifically for accessing through this
   library using the `User Management Commands`_ so that you can limit
   the scope of the user for your purposes.


Quickstart
----------

Make sure you have properly installed and configured Photoprism
somewhere. To interact with the Photoprism server in any capacity, you
need an access token. You can request this from the server either as a
:class:`User` or a :class:`Client`. To create either of these objects,
you will need to pass the base URL to the API. You can either use the
:func:`get_api_url` function or you can type the URL manually.

To use Photoprysm in a project::

    import photoprysm

    user = photoprysm.User('my_username','my_password')
    server_api = photoprysm.get_api_url('localhost:2342')

    with user_session(user, server_api) as session:
        album = photoprysm.get_album_by_name(session, server_api, 'Summer Vacation')

>>> print(album)
Album(uid='example-uid', title='Summer Vacation', favorite=False, private=False, description='')

You can also use the request function to manually put in the endpoints::

    with user_session(user, server_api) as session:
        resp = photoprysm.request(session, server_api, 'GET', 'session')
        assert resp.json()['id'] == session.headers['Authorization'].removeprefix('Bearer ')


.. _`Getting Started`: https://docs.photoprism.app/getting-started/
.. _`User Management Commands`: https://docs.photoprism.app/user-guide/users/cli/
