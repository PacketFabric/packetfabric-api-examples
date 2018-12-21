.. _functions-helpful:

Functions
=========

There are several tasks that are done repeatedly when interacting with the API.
These include generating the ``auth_hash``, building a query string from a
dictionary object and generating the full URL endpoint.

.. _functions-buildhash:

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
        key_secret: The secret key associated with the API key you'll be passing in the `api_key` parameter. It is a tuple
            with the following format: (KEY_ID, KEY_SECRET)
        query_string: A URL query string

            query_string format: "param1=value1&param2=value2&api_key=API_KEY"

            Note that this does not have the leading "?" and that the api_key is included
        """
        hash = hmac.new(key_secret[1], query_string, hashlib.sha256).digest()
        hash = base64.b64encode(hash)
        hash = urllib.quote_plus(hash)
        return hash

.. _functions-buildquerystring:

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

.. _functions-generatefullendpoint:

Generate Full API Endpoint
--------------------------

This function will build the full URL we will call. It will utilize a combination
of ``generate_hash`` and ``generate_query_string`` to properly build the URL.

::

    def generate_full_endpoint(api_url, endpoint, key_secret=None, query_string=None):
        """Build the full API end point with query string and auth hash

        api_url: The base URL for the API
        endpoint: The URL that will be queried
        key_secret: The key associated with the user making this call. It is a tuple
            with the following format: (KEY_ID, KEY_SECRET)
        query_string: The query string that will be used to make this call

        Returns the full URL of the API, with auth_hash, query string and api_key
        for this call
        """
        if query_string:
            query_string = "{query_string}&".format(query_string=query_string)
        else:
            query_string = ""
        if key_secret:
            query_string += "api_key={api_key}".format(api_key=key_secret[0])
            query_string += "&auth_hash={hash}".format(
                hash=generate_hash(key_secret, query_string))
        query_string = "?{query_string}".format(query_string=query_string)

        url = "{api}{endpoint}{query_string}".format(
            api=api_url,
            endpoint=endpoint,
            query_string=query_string)
        return url

With this function (and the previous two) we can handle any type of URL we need
when interacting with the PacketFabric API.
