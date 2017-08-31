.. _example-login:

Login
=====

Explicitly logging in via the API is only needed if you are using the
:ref:`Session Token & Cookie <session-token-cookie>` method to communicate with
the API.

    import requests
    session = requests.Session()
    login_url = "https://docs.packetfabric.com/login"
    params = {
        'user_login': 'ValidUserName',
        'user_password': 'ValidPassword'
    }
    session.post(login_url, data=params)

After this block of code, your ``session_token`` will be automatically sent with
your requests, as long as you use ``session`` instead of ``requests``

As an example, the following block will query the
`/customer <https://docs.packetfabric.com/#api-Customer-GetCustomer>`__ end point
and the data will be accessible in ``r.json()`` at the completion of the request

    r = session.get('https://api.packetfabric.com/customer')

**Note**: In all other examples, if you choose to utilize this method, instead
of API Keys, you will only need to change ``requests`` to ``session`` in your
calls.
