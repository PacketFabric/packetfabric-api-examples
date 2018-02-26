.. _example-ordervirtualcircuit-3rdparty:

Ordering a 3rd Party Virtual Circuit
==========================

Much like :ref:`ordering a port <example-orderport>`, ordering a Virtual Circuit
is a series of API calls to gather all the information needed to complete the
order.

In this example, we'll be requesting to connect one end of our virtual circuit
to a 3rd party in the PacketFabric market place. We'll cover authorizing the connection from
their point of view too.

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
are shown in the `get products <https://docs.packetfabric.com/#api-Billing-GetBillingProducts>`__
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

This step assumes that you know your port id. You can find this either in the portal or
via the `interfaces <https://docs.packetfabric.com/#api-Interface-GetInterfacesPhysical>`__
call. You want the ``ifd_id`` value from that response. If you have more than one port,
you will need to determine which port you want to use.

::

    src_ifd_id = 1388
    product_type = 'longhaul_dedicated'
    product_ids = 13820


    endpoint = '{}/interfaces/physical/:ifd_id/vlans'.format(api_url)
    src_endpoint = endpoint.replace(":ifd_id", str(src_ifd_id))
    params = {
        'api_key': api_key,
        }
    query_string = generate_query_string(params)
    r_src = requests.get("{}?{}&auth_hash={}".format(src_endpoint, query_string,
        generate_hash(api_secret, query_string)))
    src_vlan = r_src.json()['lowest_available_vlan']


.. _example-ordervirtualcircuit-createvc

Find 3rd party to connect to
----------------------------

We need to find the ``customer_crid`` (Connection Routing ID) of the 3rd party.
This is used to uniquely identify who we want to connect to within the
PacketFabric market place.

We can search by ``customer_id``, ``customer_name`` (exact match), ``partner_type``,
``market_code``, ``pop_id`` or partial matches of ``customer_name`` and ``description``

The `Customers Endpoint <https://docs.packetfabric.com/#api-Customer-GetCustomers>`__ provides
an example response.

In the sample below, we are going to search for a partial match of a customer name.

::

    params = {
        'search': 'Test Cust'
    }
    endpoint = '{}/customers'.format(api_url)

    query_string = generate_query_string(params)
    r = requests.get("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))
    crid = r.json()[0]['customer_crid']

In this example, we took the first result (``r.json()[0]``) and used their ``customer_crid``.


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

The last thing you need before we create a Virtual Circuit is the destination
``market_code`` that we want to connect to. Since a customer can have interfaces
in multiple markets, it's important to identify to the 3rd party *where* we want
to connect.

::

    billing_id = 70208
    src_ifd_id = 1388
    src_lowest_vlan = 1
    product_ids = [{'product_type': "longhaul_dedicated", 'product_id': 13820}]
    description = "Test Virtual Circuit"

    endpoint = '{}/virtual-circuits/third-party-connections/evpl'.format(api_url)

    vc_params = {
        "ifd_id": src_ifd_id,
        "description": description,
        "products": product_ids,
        "billing_account": billing_id,
        "vc_member_crid": crid,
        'market_code': destination_market_code
    }
    params = {
        'api_key': api_key,
        }

    vc_params['vlan_id_src'] = src_lowest_vlan      # Put the source on a VLAN

    query_string = generate_query_string(params)
    url = "{}?{}&auth_hash={}".format(src_endpoint, query_string,
        generate_hash(api_secret, query_string))
    r = requests.post(url, json=vc_params)

One important note, here, is that the final ``.post()`` is sent using the ``json``
parameter, not the ``data`` parameter. This is because we are sending an object
that has multiple layers, specifically on the ``products`` key.

At this point, the request for connection is available to the third party. The virtual
circuit will be unavailable until the connection is accepted. They have been alerted
to this request and it displays in their PacketFabric portal.

Accepting a 3rd party request
-----------------------------

The receiving party for the virtual circuit request needs to accept and provision
the request to activate the circuit. This can be accomplished either in the PacketFabric
portal, or via the API.

We can look at all of our received requests via the following. It is important to note
that the ``api_key`` in this section is the key of the *receiving* party.

::

    endpoint = '{}/virtual-circuits/requests/received'.format(api_url)
    params = {
        'api_key': api_key,     # THIS IS THE RECEIVING CUSTOMER'S API KEY
        }
    query_string = generate_query_string(params)
    url = "{}?{}&auth_hash={}".format(src_endpoint, query_string,
        generate_hash(api_secret, query_string))

    r = requests.get("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))

This endpoint returns a list of received requests. You can parse through them looking
for pending ones by doing this:

::

    for req in r.json():
        if req['vc_request_status'] == 'pending':
            # Next steps

Accepting a request
-------------------

In the loop mentioned above we have the option of either accepting or accepting *and* provisioning
a request.

Accepting a request acknowledges the request, but does not complete the connection. Remember, this
this would be within the loop started above.

::

    endpoint = '{}virtual-circuits/requests/:vc_request_id/accept'.format(api_url)
    params = {
        'api_key': api_key,     # THIS IS THE RECEIVING CUSTOMER'S API KEY
        }
    query_string = generate_query_string(params)
    action_url = endpoint.replace(':vc_request_id', str(req['vc_request_id']))
    url = "{}&auth_hash={}".format(src_endpoint, query_string,
        generate_hash(api_secret, query_string))
    r = requests.post(url)

Provisioning a request
----------------------

Provisioning a request sets up and completes the virtual circuit. Again, this will
be within the loop started above. For this to complete, the customer needs
an interface in the market requested. We also need to know the ``vlan_id`` we'll be
using. Both of those are assumed values in this example. Finding this information
can be found using sections above.

::

    prov_params = {
        'ifd_id': 1,
        'vlan_id': 1,
    }

    endpoint = '{}virtual-circuits/requests/:vc_request_id/provision'.format(api_url)
    params = {
        'api_key': api_key,     # THIS IS THE RECEIVING CUSTOMER'S API KEY
        }
    query_string = generate_query_string(params)
    action_url = endpoint.replace(':vc_request_id', str(req['vc_request_id']))
    url = "{}&auth_hash={}".format(src_endpoint, query_string,
        generate_hash(api_secret, query_string))
    r = requests.post(url, json=prov_params)



Finishing up
------------

Congratulations! You and your third party partner have established a virtual circuit
between one another.
