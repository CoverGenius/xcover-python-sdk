.. xCover Python SDK documentation master file, created by
   sphinx-quickstart on Mon Dec  3 12:46:41 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to xCover Python SDK's documentation!
=============================================

To use this library


.. code-block:: python

   from xcovlib.http.auth import SignatureAuth
   from xcovlib.http.http_requests import HttpRequest
   from xcovlib.registry import registry
   from xcovlib.api.quotes import Quote


   credentials = SignatureAuth(key=xcov_key secret=xcov_secret)

   host = 'https://127.0.0.1:8001' # host for xCover
   conn = HttpRequest(host, auth=credentials,)
   registry.setup({'http_handler': conn})

Now you can continue to use the methods below normally

Quotes
======
.. automodule:: xcovlib.api.quotes
    :members:

Bookings
========
.. automodule:: xcovlib.api.bookings
    :members:

Renewals
========
.. automodule:: xcovlib.api.renewals
    :members:



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
