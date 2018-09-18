.. _example-orderport:

Ordering a Port
===============

Ordering a port is a series of API calls. These calls are to gather all the required
information needed to make the completed order, then finally placing the order.

.. _example-orderport-billingid

Find our billing_id
-------------------

A new port needs to be associated with your billing account. We accomplish this
by finding your ``billing_id``

::

    api_url = 'https://api.packetfabric.com'
    api_key = '1-1111111'
    api_secret = 'ABCDEF012345678'

    endpoint = '{}/billing/accounts'.format(api_url)
    params = {'api_key': api_key}
    query_string = generate_query_string(params)
    r = requests.get("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))
    billing_id = r.json()[0]['Id']

The result of ``r.json()`` contains a list of possible billing accounts. In this
example, there is only a single result::

    [{u'Id': u'70208', u'Name': u"Playground"}]


.. _example-orderport-popid

Getting pop_id
--------------

The first thing you need in this process is to retrieve the ``pop_id``. This is
used to determine where the port will be located.

::

    endpoint = '{}/locations'.format(api_url)
    params = {'market': 'DA1', 'api_key': api_key}
    query_string = generate_query_string(params)
    r = requests.get("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))

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
move to the next step in ordering a port.

.. _example-orderport-orderport

Order the port
--------------

With all the information gathered above, we can order a port now. For this example,
we'll be ordering a port located at ``DA1``, that is ``10Gbps``, and has a subscription term
of 12 months. We've gathered all this information with the snippets above.

::

    pop_id = 1
    billing_account = 70208
    speed = "10Gbps"
    media_type = "LR"
    subscription_term = 12
    description = "My Port Name"
    zone = "A"

    endpoint = '{}/ports'.format(api_url)

    phy_params = {
        'billing_account': billing_id,
        'description': description,
        'media': media_type,
        'pop_id': pop_id,
        'speed': speed,
        'subscription_term': subscription_term,
        'zone': zone
    }
    params = {'api_key': api_key}
    query_string = generate_query_string(params)
    r = requests.post("{}?{}&auth_hash={}".format(endpoint, query_string, generate_hash(api_secret, query_string)),
        json=phy_params)

One important note, here, is that the final ``.post()`` is sent using the ``json`` parameter, not
the ``data`` parameter. This is because we are sending an object that has multiple layers, specifically on the
``products`` key.

.. _example-orderport-conclusion

Finishing up
------------

Congratulations! You've now ordered and activated a single port. This entire process
should take about a minute, with the majority of that time spent waiting
for provisioning to complete. Billing for this new port will begin automatically
after 15 days.
