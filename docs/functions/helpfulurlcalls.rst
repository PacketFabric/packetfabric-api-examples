.. _functions-helpfulurlcalls:

Helpful URL Calls
=================

If you are utilizing the :ref:```generate_full_endpoint`` <functions-generatefullendpoint>` method,
then this page will help you see the different ways you can easily query the API.

Each of these will require that you have access to your API Key ID and Key Secret. These will be
stored in the variable ``valid_secrets`` as a tuple (which is how the helpful functions are expecting them).

::

    valid_secrets = (KEY_ID, KEY_SECRET)

.. _functions-get-noparams

Get Information without parameters
----------------------------------

Querying information from the API, and receiving a list of items back, is an
``HTTP GET`` request. One of the most common endpoints you'll do this with, is
when finding your ``billing_id`` <functions-billingid>`.

::

    endpoint = 'billing/accounts'
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets))

This will return a list of dictionaries that you will need to iterate through.

.. _functions-get-withparams

Get Information with parameters
-------------------------------

Often times you'll want to narrow down your search criteria. An example of this
could be when you are trying to find the ``pop_id`` so that you will order a product
to the right location. This type of request is also an ``HTTP GET``

We do this by creating a dictionary with our criteria, and then using that dictionary
to pass parameters to the API.

::

    endpoint = 'locations'
    params = {'market': 'DA1'}
    query_string = generate_query_string(params)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This will return, in ``r.json()``, a list of dictionaries for all pops in the ``DA1`` market.


.. _functions-post-params

Create an item with parameters
------------------------------

When you order a new product, create a new user, or add a new virtual circuit, you
will be doing an ``HTTP POST`` request and passing parameters to the API that
indicate what you are doing.

A ``POST`` request, with parameters, is very similar to getting information with
parameters.

::

    endpoint = 'ports'
    params = {
        'billing_account': 1234567890,
        'description': "A Brand new port",
        'media': "LR",
        'pop_id': 1,
        'speed': "10Gbps",
        'subscription_term': 12,
        'zone': "A"
    }
    r = requests.post(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This call will provision a new 10Gbps post in Zone A of ``pop_id`` 1. It is for a
12 month term.

Notice the only difference between this call and the call to get information with
parameters is changing the ``.get(...)`` to ``.post(...)``
