.. _authmethods:

Authentication Methods
======================

Authenticating via the API can be accomplished in two different ways::

-  Using a Session Token & Cookie
-  Using an API Key & Hash

.. _session-token-cookie:

Session Token & Cookie
----------------------

The session token and cookie is the method utilized by our own portal. (Yes, we
use the API that you use.) This method requires you to explicitly login by
passing an authorized username and password and then storing the ``session_token``
the API returns to you. All of your calls after this must include the ``session_token``

**Note**: We only allow one authenticated session at a time. If you use this method,
the PacketFabric portal will require you to login again.

The example below will store a session token for you. Assuming you have passed
a valid username and password, your future calls to the API can be accomplished
by utilizing the ``session`` variable::

    session = requests.Session()
    login_url = "https://docs.packetfabric.com/login"
    params = {
        'user_login': 'ValidUserName',
        'user_password': 'ValidPassword'
    }
    session.post(login_url, data=params)

A call to the `/customer <https://docs.packetfabric.com/#api-Customer-GetCustomer>`__
end point, would then look like this::

    r = session.get('https://api.packetfabric.com/customer')

Your results would be available in ``r.json()``

.. _api-key-hash:

API Key & Hash
--------------

This method requires that you have generated an API key with appropriate permissions
prior to use. The API Secret is utilized on each call to create a hash value of
the query string.

**Note**: Using the API Key and hash will not log you out of the portal if you
have an automated process that runs while you are navigating the portal.

A call to the `/customer <https://docs.packetfabric.com/#api-Customer-GetCustomer>`__
end point, would then look like this::

    url = generate_full_endpoint('customer', key_secret='1-1111111')
    r = request.get(url)

Your results would be available in ``r.json()``

If you are curious about the function called in the previous example, see
the Helpful Functions section.
