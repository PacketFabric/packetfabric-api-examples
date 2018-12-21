.. _example-ordervirtualcircuit-backbone:

Ordering a Backbone Virtual Circuit
==========================

Much like :ref:`ordering a port <example-orderport>`, ordering a Virtual Circuit
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

A new virtual circuit needs to be associated with your billing account. This can be accomplished
by :ref:`finding your billing_id <functions-billingid>`.

.. _example-ordervirtualcircuit-productids

Determining which billing_product_type to use
---------------------------------------------

A virtual circuit can be one of three types: ``longhaul_dedicated``,
``longhaul_usage`` or ``virtual_circuit_metro``. A ``longhaul_dedicated``
circuit is charged based on a monthly basis regardless of how much it is used. A
``longhaul_usage`` circuit is charged based on how much data is transferred per
month at a flatrate. A ``virtual_circuit_metro`` circuit is only viable for two
ports in the same metro area but different physical locations.

For this example, we're going to use the ``longhaul_dedicated``.

With this option, we need to supply ``billing_speed`` and ``billing_term``
parameters as well.

For this example, we'll select a ``billing_speed`` of ``10Gbps`` and a
``billing_term`` of ``12``. This will provision a 10Gbps virtual circuit between
our two ports for a period of 1 year.


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
    src_lowest_vlan = 4
    dest_lowest_vlan = 4
    description = "Test Virtual Circuit"

    endpoint = '{}/virtual-circuits/backbone-connections/evpl'.format(api_url)

    vc_params = {
        "ifd_id_src": src_ifd_id,
        "ifd_id_dest": dest_ifd_id,
        "description": description,
        "billing_product_type": "longhaul_dedicated",
        "billing_speed": "10Gbps",
        "billing_term": 12,
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
        "billing_product_type": "longhaul_dedicated",
        "billing_speed": "10Gbps",
        "billing_term": 12,
        "billing_account": 70208,
        "vlan_id_src": 4,
        "untagged_dest": "true"
    }

We receive a payload back, as well. The payload contains information about the
virtual circuit provisioned.

::

    {
        'connected': False,
        'customer_id': 759,
        'description': 'Test Virtual Circuit',
        'disabled_interfaces': [],
        'enabled_interfaces': [],
        'members': [],
        'object_id': 161900,
        'product_id': 1,
        'product_name': 'Backbone Connection',
        'state': 'Requested',
        'time_created': '2018-09-11T07:47:43-05:00',
        'time_updated': '2018-09-11T07:47:43-05:00',
        'user_id': 821,
        'vc_attr': {'billing': {'account_id': 70907,
                             'product_type': 'longhaul_dedicated',
                             'speed': '10Gbps',
                             'subscription_term': 12},
                 'settings': {'ifd_id_dest': 1389,
                              'ifd_id_src': 1388,
                              'no_service_order': False,
                              'untagged_dest': False,
                              'untagged_src': False,
                              'vlan_id_dest': 4,
                              'vlan_id_src': 4},
                 'tasks': []},
        'vc_circuit_id': 'PF-BC-DA1-DA2-161900',
        'vc_id': 135303,
        'vc_mode': 'evpl',
        'vc_multipoint': False,
        'vc_service_class': 'longhaul'
    }

No further activation is required for this longhaul connection.

Finishing up
------------

Congratulations! You've now ordered and activated a dedicated longhaul backbone
connection between two of your own ports. This entire process should take a couple
seconds or less.
