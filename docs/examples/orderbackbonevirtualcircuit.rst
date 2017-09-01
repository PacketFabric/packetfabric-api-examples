.. _example-ordervirtualcircuit-backbone:

Ordering a Backbone Virtual Circuit
==========================

Much like :ref:`Ordering a port <example-orderport>`, ordering a Virtual Circuit
is a series of API calls to gather all the information needed to complete the
order.

For this example, you need two ports in different markets. The assumption is that
these ports have already been ordered and activated.

We will be making a backbone connection. This is a self-to-self connection, meaning
that you control both ends. Another option that is available is a 3rd party
connection, where you can connect to any one else in the PacketFabric market place.

We are going to be creating an EVPL connection. This allows for multiple point to
point virtual connections between interfaces. Each port can have multiple EVPL circuits.

Another option is an EPL connection. This is a point to point ethernet virtual connection
between interfaces. It's also referred to as a pseudowire. Only one EPL circuit
can be created between selected interfaces. Once an interface is part of an EPL
circuit, that interface will no longer be available for any other circuit.
There is no rate limiting or white/blacklisting of MAC addresses using EPL mode.

.. _example-ordervirtualcircuit-billingid

Find our billing_id
-------------------

A new virtual circuit needs to be associated with your billing account. We accomplish this
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

.. _example-ordervirtualcircuit-productids

Finding product_ids
-------------------

The product you select is based on a couple factors, such as the subscription term
and speed of the port.

For this example, we are going to create a longhaul dedicated product. Other options
are shown in the `Get Products <https://docs.packetfabric.com/#api-Billing-GetBillingProducts>`__
documentation.

::

    subscription_term = 12
    product_type = 'longhaul_dedicated'

    endpoint = '{}/billing/products'.format(api_url)
    params = {
        'api_key': api_key,
        'subscription_term': subscription_term,
        'product_type': product_type
        }
    query_string = generate_query_string(params)
    r = requests.get("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))
    product_id = [{'product_type': "longhaul_dedicated",
        'product_id': r.json()[0]['Id']}]

``r.json()`` is going to contain a list of all products that match this criteria. The
index shown above will match the product you wish to select. (The ``0`` will change
to match your selection)

**Important Note**: Not everything in this list is available for your ports. It is
important that you select a product that matches or is *slower* than the speed of the
slowest port that will be in this virtual circuit. Exceeding that speed with result
in an error back from the API saying the product isn't available when you attempt
to create the virtual circuit.

The results will look similar to this::

    [
     ...
     {u'Id': u'13820',
      u'Name': u'LONGHAUL-DEDICATED-1G-MRC-12M',
      u'PortSpeed': u'1G',
      u'ProductType': u'longhaul_dedicated',
      u'Rate': [u'$425.00'],
      u'RatingMethodObj': {u'Id': u'38444',
                           u'RatingMethodPricingType': u'Standard Pricing',
                           u'RatingMethodType': u'Subscription'},
      u'subscriptionTerm': u'12'},
      ...
    ]

.. _example-ordervirtualcircuit-findvlan

Find next available VLAN ID (optional)
--------------------------------------

The next step is to determine if you want this virtual circuit to utilize VLANs on
either end of the circuit. If you *do*, we need to find the next available VLAN. If you
do *not* use a VLAN, the end of the circuit that isn't in a VLAN will be unavailable for
further connections.

This step assumes that you know your port ids. You can find this either in the portal or
via the `interfaces <https://docs.packetfabric.com/#api-Interface-GetInterfacesPhysical>`__
call. You want the ``ifd_id`` value from that response. If you have more than two ports,
you will need to determine which port you want to use.

::

    src_ifd_id = 1388
    dest_ifd_id = 1389
    product_type = 'longhaul_dedicated'
    product_ids = 13820


    endpoint = '{}/interfaces/physical/:ifd_id/vlans'.format(api_url)
    src_endpoint = endpoint.replace(":ifd_id", str(src_ifd_id))
    dest_endpoint = endpoint.replace(":ifd_id", str(dest_ifd_id))
    params = {
        'api_key': api_key,
        }
    query_string = generate_query_string(params)
    r_src = requests.get("{}?{}&auth_hash={}".format(src_endpoint, query_string,
        generate_hash(api_secret, query_string)))
    r_dest = requests.get("{}?{}&auth_hash={}".format(src_endpoint, query_string,
        generate_hash(api_secret, query_string)))
    src_vlan = r_src.json()['lowest_available_vlan']
    dest_vlan = r_dest.json()['lowest_available_vlan']


.. _example-ordervirtualcircuit-createvc

Create Virtual Circuit
----------------------

With the information we've gathered above, we can now provision a virtual circuit
between our two ports. As a reminder, we're making an
`EVPL connection <https://docs.packetfabric.com/#api-Virtual_Circuits-PostVirtualCircuitsBackboneConnectionsEVPL>`__.

If you are using VLANs for the source, destination or both you will need to add
``vlan_id_src`` and/or ``vlan_id_dest`` keys to the ``vc_params`` dictionary below.

If you are using an untagged (non-VLAN) source, destination or both you will need
to add ``untagged_src`` and/or ``untagged_dest`` keys to the ``vc_params` dictionary
below.

::

    billing_id = 70208
    src_ifd_id = 1388
    dest_ifd_id = 1389
    src_lowest_vlan = 1
    dest_lowest_vlan = 1
    product_ids = [{'product_type': "longhaul_dedicated", 'product_id': 13820}]
    description = "Test Virtual Circuit"

    endpoint = '{}/virtual-circuits/backbone-connections/evpl'.format(api_url)

    vc_params = {
        "ifd_id_src": src_ifd_id,
        "ifd_id_dest": dest_ifd_id,
        "description": description,
        "products": product_ids,
        "billing_account": billing_id
    }
    params = {
        'api_key': api_key,
        }

    vc_params['vlan_id_src'] = src_lowest_vlan      # Put the source on a VLAN
    vc_params['untagged_dest'] = "true"     # The destination will be untagged

    query_string = generate_query_string(params)
    url = "{}?{}&auth_hash={}".format(src_endpoint, query_string,
        generate_hash(api_secret, query_string))
    print url
    r = requests.post(url, json=vc_params)

One important note, here, is that the final ``.post()`` is sent using the ``json``
parameter, not the ``data`` parameter. This is because we are sending an object
that has multiple layers, specifically on the ``products`` key. Our payload
looks like this::

    {
        "ifd_id_src": 1388,
        "ifd_id_dest": 1389,
        "description": "Test Virtual Circuit",
        "products": [{'product_type': "longhaul_dedicated", 'product_id': 13820}],
        "billing_account": 70208,
        "vlan_id_src": 1,
        "untagged_dest": "true"
    }

We receive a payload back, as well. The payload contains information about the
``service_order`` and the ``tasks`` this order generated.

::

    {u'service_order': {u'customer_id': 435,
                    u'document_attr': {u'vc_circuit_id': u'PF-BC-DA1-DA2-3604'},
                    u'document_data': None,
                    u'document_description': u"Andy's Test Playground service order PF-87749201709010305",
                    u'document_id': 1470,
                    u'document_mime_type': u'application/pdf',
                    u'document_name': u'service-order-PF-87749201709010305.pdf',
                    u'document_size': 37911,
                    u'document_type': u'service_order',
                    u'temp_file_path': None,
                    u'time_created': u'2017-08-31T22:05:13-05:00',
                    u'time_updated': u'2017-08-31T22:05:13-05:00',
                    u'user_id': 439},
    u'tasks': [{u'customer_id': 435,
             u'task_action': u'logical_interface_create_evpl',
             u'task_description': u"Create virtual circuit for Andy's Test Playground",
             u'task_id': u'4844',
             u'task_request_data': {u'customer_id': 435,
                                    u'customer_name': u"Andy's Test Playground",
                                    u'device_id': 3,
                                    u'iface_name': u'xe-0/0/2:2',
                                    u'ifd_id': 1388,
                                    u'ifd_speed': u'10G',
                                    u'ifl_id': 1241,
                                    u'ifl_mac_blacklist': None,
                                    u'ifl_mac_whitelist': None,
                                    u'ifl_rate_limit_in': 0,
                                    u'ifl_rate_limit_out': 0,
                                    u'ifl_vlan_id': 1,
                                    u'pop_id': 1,
                                    u'request_id': 1506051,
                                    u'vc_circuit_id': u'PF-BC-DA1-DA2-3604',
                                    u'vc_id': 1815},
             u'task_response_data': None,
             u'task_status': u'active',
             u'time_created': u'2017-08-31T22:05:12-05:00',
             u'time_updated': u'2017-08-31T22:05:12-05:00'},
             {u'customer_id': 435,
              u'task_action': u'logical_interface_create_evpl',
              u'task_description': u"Create virtual circuit for Andy's Test Playground",
              u'task_id': u'4845',
              u'task_request_data': {u'customer_id': 435,
                                     u'customer_name': u"Andy's Test Playground",
                                     u'device_id': 2,
                                     u'iface_name': u'xe-0/0/1:0',
                                     u'ifd_id': 1389,
                                     u'ifd_speed': u'10G',
                                     u'ifl_id': 1242,
                                     u'ifl_mac_blacklist': None,
                                     u'ifl_mac_whitelist': None,
                                     u'ifl_rate_limit_in': 0,
                                     u'ifl_rate_limit_out': 0,
                                     u'ifl_vlan_id': 0,
                                     u'pop_id': 2,
                                     u'request_id': 1506051,
                                     u'vc_circuit_id': u'PF-BC-DA1-DA2-3604',
                                     u'vc_id': 1815},
              u'task_response_data': None,
              u'task_status': u'active',
              u'time_created': u'2017-08-31T22:05:12-05:00',
              u'time_updated': u'2017-08-31T22:05:12-05:00'}]}


Each of the ``['tasks']['task_id']`` keys can be used to check the status of this
order. Provisioning of a virtual circuit should only take a few seconds.

No further activation is required for this longhaul connection.

Finishing up
------------

Congratulations! You've now ordered and activated a dedicated longhaul backbone
connection between two of your own ports. This entire process should take a couple
seconds or less. 
