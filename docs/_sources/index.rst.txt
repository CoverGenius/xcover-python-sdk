.. xCover Python SDK documentation master file, created by
   sphinx-quickstart on Mon Dec  3 12:46:41 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to xCover Python SDK's documentation!
=============================================

To use this library


.. code-block:: python

   from xcovlib.client import Client

   key = 'KEY'
   secret = 'SECRET'
   host = '127.0.0.1'
   client = Client(key, secret, host)

Now you can continue to use the methods below normally

Client
======
.. automodule:: xcovlib.client.Client
    :members: create_quote, get_quote, create_booking, get_booking, create_renewal

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`search`
