.. _functions-helpful:

Functions
=========

There are several tasks that are done repeatedly when interacting with the API.
These include generating the ``auth_hash`` and building a query string from a
dictionary object.

.. _functions-buildhash

Building a hash
---------------

Building an ``auth_hash`` requires the API key secret. This is generated when
you create your :ref:`API Key <requirement-apikey>`.

::

    import hmac
    import urllib
    import hashlib
    import base64

    def generate_hash(key_secret, query_string=None):
        """
        key_secret: The secret key associated with the API key you'll be passing in the `api_key` parameter
        query_string: A URL query string

            query_string format: "param1=value1&param2=value2&api_key=API_KEY"

            Note that this does not have the leading "?" and that the api_key is included
        """
        hash = hmac.new(key_secret, query_string, hashlib.sha256).digest()
        hash = base64.b64encode(hash)
        hash = urllib.quote_plus(hash)
        return hash

.. _functions-buildquerystring

Generating Query string
-----------------------

``requests`` can take dictionary objects when using ``.post()``, ``.put()`` or ``.patch()`` methods. It
may be easier to utilize the same code structure when using ``.get()`` as well. This function will convert
a dictionary object into a query string, which can be passed to ``generate_hash()``

::

    def generate_query_string(query_dict):
        """
        query_dict: A dictionary of key:value pairs

            Format:
                {
                    'param1': 'value1',
                    'param2': 100,
                    'param3': 'value2'
                }

            Result: "param3=value2&param2=100&param1=value1"
        """
        if isinstance(query_dict, basestring):
            return query_dict
        else:
            q = ''.join("{k}={v}&".format(k=k, v=v) for k, v in query_dict.items() if v)
            return q[:-1]   # Strip trailing "&"
