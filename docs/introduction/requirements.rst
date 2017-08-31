.. _requirements:

Requirements
============

.. _requirement-python:

Python and requests
-------------------

The examples provided in this documentation all use Python. The examples also
use `requests <http://docs.python-requests.org/>`__ , which you should install
via::

    pip install requests

Everything in these examples should work for Python 2.7 and 3.4 or higher.

.. _requirement-apikey

API Keys
--------

If you are using the :ref:`API Key & Hash <api-key-hash>` method instead of the
:ref:`Session Token & Cookie <session-token-cookie>` method, you will need an
API key and secret. You can do this via the portal.

 - Log into the `portal <https://portal.packetfabric.com>`__
 - Click "Admin Settings" along the top navigation bar
 - Click "API Keys" along the left navigation bar
 - In the "Select Users" box, find the user ID you'll be associating this
 key with and select it
 - Press "Generate Key for user"

The ``Key ID`` and ``Key Secret``, along with an expiration date, will be shown
in the table below. The ``Key ID`` will be transmitted with all of your API calls
in the ``api_key`` parameter. The ``Key Secret`` **should never be transmitted**.
It is used to generate the ``auth_hash``, but is **not** sent to the API.
