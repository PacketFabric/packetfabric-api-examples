.. _functions-helpfulids:

Finding Useful IDs
==================

When ordering products or interacting with purchased products, you'll need
several different IDs, so that you are referencing the correct items. This page will
show how to find several of these. They will utilize the :ref:`Helpful Functions <functions-helpful>`.

Each of these will require that you have access to your API Key ID and Key Secret. These will be
stored in the variable ``valid_secrets`` as a tuple (which is how the helpful functions are expecting them).

::

    valid_secrets = (KEY_ID, KEY_SECRET)

.. _functions-billingid:

Find billing_id
---------------

All products ordered need to be associated with a ``billing_id``. This is to
ensure you are properly billed. You will

::

    endpoint = 'billing/accounts'
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets))

The result of ``r.json()`` contains a list of possible billing accounts. Select
the billing account you wish to utilize from the list that is returned. You'll utilize
that ``Id`` when ordering a product.

An account with only a single ``billing_id`` will have a result similar to this, which
can be accessed by ``r.json()[0]['Id']`` and will have a value of ``70208``.

::

    [{u'Id': u'70208', u'Name': u"Playground"}]

.. _functions-popid:

Find pop_id
-----------

``pop_id``s are used to identify where a product will originate from or terminate at. They
are identified in documentation as ``pop_id``, ``pop_id_src`` or ``pop_id_dest``, depending
on if one id is needed or multiple.

::

    endpoint = 'locations'
    params = {'market': 'DA1'}
    query_string = generate_query_string(params)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This will return, in ``r.json()``, a list of dictionaries for all pops in the ``DA1`` market.

``r.json()`` will look something like this::

    [{u'market_code': u'DA1',
      u'market_description': u'Dallas LAB1',
      u'pop_id': 1,
      u'pop_latitude': u'31.566523',
      u'pop_longitude': u'-97.102661',
      u'pop_name': u'LAB1',
      u'sites': [{u'pcode': 3725900,
                  u'site_address1': u'1649 W Frankford Rd',
                  u'site_address2': u'',
                  u'site_city': u'Carrollton',
                  u'site_country': u'US',
                  u'site_id': 175,
                  u'site_latitude': u'32.795581',
                  u'site_longitude': u'-96.783443',
                  u'site_name': u'PacketFabric LAB1',
                  u'site_postal': u'75007',
                  u'site_state': u'TX',
                  u'site_status': u'Active',
                  u'vendor_id': 9,
                  u'vendor_name': u'PacketFabric'}]}]

In this example, you want to save the value of ``r.json()[0]['pop_id']`` before we
move to the next step.
