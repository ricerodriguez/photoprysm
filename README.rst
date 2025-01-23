========================
Photoprism Python Client
========================


.. image:: https://img.shields.io/pypi/v/photoprysm.svg
        :target: https://pypi.python.org/pypi/photoprysm

.. image:: https://readthedocs.org/projects/photoprysm/badge/?version=latest
        :target: https://photoprysm.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A Python client for interacting the the Photoprism REST API.


* Free software: GNU General Public License v3
* Documentation: https://photoprysm.readthedocs.io.


Features
--------

* Made to work with the popular Requests_ package
* Session management for both Users and Clients

.. _Requests: https://requests.readthedocs.io

Quickstart
----------

To start, you need a :class:`User` or :class:`Client` instance.

>>> import photoprysm
>>> user = photoprysm.User('username', 'password')
>>> server_api = photoprysm.get_api_url('localhost:2342')

You can either login with the `User` or `Client` handle and log out later...

>>> session = user.login(server_api)
>>> # Do some stuff
>>> user.logout()

Or you can use the context manager so that it will log out automatically when you are done.

>>> with photoprysm.user_session(user, server_api) as session:
>>>     # Do some stuff
>>> # Logged out

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
