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

.. _example-orderport-availports

Getting available ports
-----------------------

Using the ``pop_id`` from above, we can now figure out which ports are available
at our destination::

    pop_id = 1
    endpoint = '{}/interfaces/physical/availability'.format(api_url)
    params = {'pop_id': pop_id, 'api_key': api_key}
    query_string = generate_query_string(params)
    r = requests.get("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))

The results of this call will look similar to this::

    {u'interfaces': {u'10Gbps:LR': 22, u'40Gbps:LR4': 6},
     u'media': {u'LR': 22, u'LR4': 6},
     u'speed': {u'10Gbps': 22, u'40Gbps': 6},
     u'zones': {u'A': {u'10Gbps:LR': 10, u'40Gbps:LR4': 3},
                u'B': {u'10Gbps:LR': 2, u'40Gbps:LR4': 3}}
    }

Here we can see that there are a total of 22 10Gbps ports and 6 40 Gbps ports. These
are split across multiple zones as well. From here, we need to determine which
type of port we want to order. We'll use this to get the associated ``product_ids``
to complete the order.

We're going to select a ``10Gbps:LR`` port in Zone ``A``. You can split out speed
and media type by using ``.split(":")``

.. _example-orderport-productids

Finding product_ids
-------------------

There are multiple products associated with a new port. These include non-recurring costs,
monthly recurring costs and any media fees. We'll order a port with a subscription term
of 12 months.

We are providing enough information in our search for pricing, that only a single
result should be returned for each check.

::

    speed = "10Gbps"
    media_type = "LR"
    subscription_term = 12
    endpoint = '{}/billing/product/pricing'.format(api_url)

    product_ids = []
    speed = speed.replace("bps","")

    nrc_params = {      # These are non-recurring costs
        'product_type': 'port',
        'rating_type': 'NRC',
        'speed': speed,
        'subscription_term': subscription_term,
        'api_key': api_key
        }
    mrc_params = {      # These are monthly recurring costs
        'product_type': 'port',
        'rating_type': 'MRC',
        'speed': speed,
        'subscription_term': subscription_term,
        'api_key': api_key
        }
    media_params = {    # These are costs associated with the media
        'product_type': 'media',
        'media': media_type,
        'speed': speed,
        'subscription_term': subscription_term,
        'api_key': api_key
        }

    nrc_query_string = generate_query_string(nrc_params)
    mrc_query_string = generate_query_string(mrc_params)
    media_query_string = generate_query_string(media_params)
    nrc = requests.get("{}?{}&auth_hash={}".format(endpoint, nrc_query_string, generate_hash(api_secret, nrc_query_string)))
    mrc = requests.get("{}?{}&auth_hash={}".format(endpoint, mrc_query_string, generate_hash(api_secret, mrc_query_string)))
    media = requests.get("{}?{}&auth_hash={}".format(endpoint, media_query_string, generate_hash(api_secret, media_query_string)))

    product_ids.append(('port', nrc.json()[0]['Id']))
    product_ids.append(('port', mrc.json()[0]['Id']))
    product_ids.append(('media', media.json()[0]['Id']))

The results of ``nrc.json()``, ``mrc.json()`` and ``media.json()`` will each look
similar to this::

    [{u'Id': u'13790',
      u'Name': u'ACCESS-10G-NRC-12M',
      u'PortSpeed': u'10G',
      u'ProductType': u'port',
      u'Rate': [u'$250.00'],
      u'RatingMethodObj': {u'Id': u'38414',
                           u'RatingMethodPricingType': u'Standard Pricing',
                           u'RatingMethodType': u'One Time Charge'},

      u'subscriptionTerm': u'12'}]

The only information needed for ordering a port is the ``Id``. The other information
may be useful to you, though.

.. _example-orderport-orderport

Order the port
--------------

With all the information gathered above, we can order a port now. For this example,
we'll be ordering a port located at ``DA1``, that is ``10Gbps``, and has a subscription term
of 12 months. We've gathered all this information with the snippets above.

::

    pop_id = 1
    billing_id = 70208
    speed = "10Gbps"
    media_type = "LR"
    subscription_term = 12
    product_ids = [('port', u'13790'), ('port', u'13844'), ('media', u'13875')]
    description = "My Port Name"
    zone = "A"

    endpoint = '{}/interfaces/physical'.format(api_url)
    products = []

    for p in product_ids:   # Create the list of products we need to pass
        products.append({'product_type': p[0], 'product_id': p[1]})

    phy_params = {
        'billing_account': billing_id,
        'description': description,
        'media': media_type,
        'pop_id': pop_id,
        'products': products,
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
``products`` key. Our pay load looks like this::

    {'billing_account': 70208,
     'description': 'My Port Name',
     'media': 'LR',
     'pop_id': 1,
     'products': [{'product_id': u'13790', 'product_type': 'port'},
                  {'product_id': u'13844', 'product_type': 'port'},
                  {'product_id': u'13875', 'product_type': 'media'}],
     'speed': '10Gbps',
     'subscription_term': 12,
     'zone': 'A'}

We receive a payload back, as well. The payload contains information about the
``service_order`` and the ``task`` this order generated.

::

    {u'service_order': {u'customer_id': 435,
                        u'document_attr': {u'ifd_id': 1388,
                                           u'pop_id': 1,
                                           u'port_circuit_id': u'PF-AP-LAB1-3597',
                                           u'site_id': u'175'},
                        u'document_data': None,
                        u'document_description': u"Playground service order PF-87749201708311851",

                        u'document_id': 1464,
                        u'document_mime_type': u'application/pdf',
                        u'document_name': u'service-order-PF-87749201708311851.pdf',
                        u'document_size': 39035,
                        u'document_type': u'service_order',
                        u'temp_file_path': None,
                        u'time_created': u'2017-08-31T13:51:14-05:00',
                        u'time_updated': u'2017-08-31T13:51:14-05:00',
                        u'user_id': 439},
     u'task': {u'customer_id': 435,
               u'task_action': u'physical_interface_create',
               u'task_description': u"Create physical interface for Playground",
               u'task_id': u'4837',
               u'task_request_data': {u'customer_id': 435,
                                      u'customer_name': u"Playground",
                                      u'device_id': 3,
                                      u'iface_name': u'xe-0/0/2:2',
                                      u'ifd_id': 1388,
                                      u'ifd_mtu': 9096,
                                      u'pop_id': 1,
                                      u'port_circuit_id': u'PF-AP-LAB1-3597',
                                      u'request_id': 1504036},
               u'task_response_data': None,
               u'task_status': u'active',
               u'time_created': u'2017-08-31T13:51:13-05:00',
               u'time_updated': u'2017-08-31T13:51:13-05:00'}}

The ``['task']['task_id']`` can be used to check the status of this order. It takes about
15 seconds for a port to be provisioned.

The ``['task']['task_request_data']['ifd_id']`` will be used to activate this port. When
initially created, the port is in a ``Testing Mode`` state. It needs to be activated.

.. _example-orderport-orderstatus

Check the status of task
------------------------

Provisioning takes about 15 seconds. This means that you need to wait for provisioning to
complete before you can perform more actions on your newly ordered port. To know when it's
ready, you have to check the status of your task::

    task_id = 4837
    endpoint = '{}/tasks/:task_id'.format(api_url)
    endpoint = endpoint.replace(":task_id", str(task_id))
    params = {'api_key': api_key}
    query_string = generate_query_string(params)
    r = requests.get("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))

``r.json()`` returns the current status of your task (along with other data)::

    {u'customer_id': 435,
     u'task_action': u'physical_interface_create',
     u'task_description': u"Create physical interface for Andy's Test Playground",
     u'task_id': 4837,
     u'task_request_data': {u'customer_id': 435,
                            u'customer_name': u"Andy's Test Playground",
                            u'device_id': 3,
                            u'iface_name': u'xe-0/0/2:2',

                            u'ifd_id': 1388,
                            u'ifd_mtu': 9096,
                            u'pop_id': 1,
                            u'port_circuit_id': u'PF-AP-LAB1-3597',
                            u'request_id': 1504036},
     u'task_response_data': {u'data': {u'message': u'success'},
                             u'status': u'success',
                             u'task_id': 4837},
     u'task_status': u'success',
     u'time_created': u'2017-08-31T13:51:14-05:00',
     u'time_updated': u'2017-08-31T13:51:16-05:00'}

The important bit here is ``['task_status']``. When it is ``success``, provisioning is
complete and you can activate your port.

.. _example-orderport-activateport

Activating the port
-------------------

Upon creation, a new port sits in ``Testing Mode``. To utilize the port, you need to
activate it. First, you need to ensure that provisioning has completed successfully.
Once it has, you can activate it::

    ifd_id = 1388

    endpoint = '{}/interfaces/physical/:ifd_id/accept'.format(api_url)
    endpoint = endpoint.replace(":ifd_id", str(ifd_id))
    params = {'api_key': api_key}
    query_string = generate_query_string(params)
    r = requests.post("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))

This returns details about the port you've just activated. It contains the same
information that the API call to get information about a
`specific interface <https://docs.packetfabric.com/#api-Interface-GetInterfacePhysical>`__
contains.

.. _example-orderport-conclusion

Finishing up
------------

Congratulations! You've now ordered and activated a single port. This entire process
should take a little over 15 seconds, with the majority of that time spent waiting
for provisioning to complete.
