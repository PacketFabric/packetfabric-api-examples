.. _example-orderbundle-packetdirect:

Ordering a PacketDirect Bundle
==========================

Instead of ordering individual ports, virtual circuits and configuring those
to be connected to one another, a bundle can be ordered that handles the
setup of all associated services automatically. A PacketDirect bundle consists
of two ports in different facilities and a virtual circuit connecting the
two ports.

The example below will walk you through ordering a PacketDirect bundle.

.. _example-pd-billingid

Find our billing_id
-------------------

As with other services, we require a ``billing_id`` to order anything. We can
get this by

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

.. _example-pd-popids

Find pop_id for source and destination
---------------------------------------

The first thing you need in this process is to retrieve the ``pop_id`` for
both our source and destination. This is used to determine where the port will
be located.

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

This example found the ``pop_id`` of a site in the ``DA1`` market. Once I know
this id, it does not change. Future calls will be able to utilize the same value
and be in the same location.

Repeating the above code with another location (say ``DA2``), will return another
``pop_id``. Now that we have both a source and a destination, we can move forward.

.. _example-pd-mediatypes

Find available speeds and media types
-------------------------------------

Using the ``pop_id`` values from above, we can now figure out which ports are
available at both our source and destination.

**Note**: Speed much match in both source and destination. The media type does
not need to match, but speed does.

::

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

Here we can see that there are a total of 22 10Gbps ports and 6 40 Gbps ports
for ``pop_id`` of ``1``. These are split across multiple zones as well.

We're going to select a ``10Gbps:LR`` port in Zone ``A``. You can split out speed
and media type by using ``.split(":")``

Run the same block of code for ``pop_id`` of ``2`` to ensure there is a ``10Gbps``
port available. If there is, we can move ahead.

.. _example-pd-order

Order the PacketDirect bundle
-----------------------------

Ordering the bundle is pretty simple. One last decision that we need to make is
whether or not we want to specify the zone our ports will be placed in, or if
the default is acceptable. If we are going to specify the zone, then two
additional keys will need to be added to the ``params`` dictionary below. These
will be ``pd_zone_src`` and ``pd_zone_dest`` and should contain a value from
the ``zones`` key that was returned when we were looking for availability in
the previous step.

If you do not specify a zone, one will be automatically assigned.

::

    endpoint = '{}/bundles/packet-direct'.format(api_url)
    params = {
        'pd_pop_id_src': 1,
        'pd_pop_id_dest': 2,
        'pd_speed_src': '10Gbps',
        'pd_speed_dest': '10Gbps',
        'pd_media_src': 'LR',
        'pd_media_dest': 'LR',
        'subscription_term': 12,
        'billing_account': 70208,
        'pd_description': "PacketDirect Bundle from POP1 to POP2",
    }
    r = requests.post(gbl.generate_full_endpoint(endpoint, valid_secrets), json=params)

This will start the process of setting up the associated ports and virtual circuit.
It is going to take a couple minutes to complete. We'll be able to check the status
of the bundle's progress using the next session.

First, though, we need to get the ``pd_id`` from ``r.json()['pd_id']``. The id
is used to accept and provision the bundle, as well as check the status.

.. _example-pd-bundleinfo

Get bundle information
----------------------

Building a bundle takes multiple steps, behind the scenes. You are able to follow
this process by check the bundle's current state.

::

    pd_id = 77
    endpoint = '{}/bundles/packet-direct/{}'.format(api_url, pd_id)
    r = requests.get(gbl.generate_full_endpoint(endpoint, valid_secrets))

The status of a bundle is in ``r.json()['state']``. A list of possible statues
is available in the :ref:`Bundles Statuses <example-pd-bundlestatus>` section
of this page.

.. _example-pd-bundleprovision

Provision bundle
----------------

After a few minutes, a new bundle will stop in ``Testing`` status. To utilize
the bundle, you need to activate it.

::

    pd_id = 77
    endpoint = '{}/bundles/packet-direct/{}/accept'.format(api_url, pd_id)
    r = requests.post(gbl.generate_full_endpoint(endpoint, valid_secrets))

You'll receive the following response back::

    {u'message': u'PacketDirect accepted'}

It will go through a couple more statuses to finish setting up the bundle. These
statuses should go quickly. It will end in ``Active`` status. You can check the
progress at any point by :ref:`checking the bundle information <example-pd-bundleinfo>`


.. _example-pd-bundleconclusion

Finishing up
------------

Congratulations! You've now ordered and activated a bundle. You have a port in
your source, a port in your destination and a virtual circuit between the two.
This entire process should take a little over 2 minutes.

.. _example-pd-bundlestatus

Bundles Statuses
----------------

Setting up (and tearing down) a bundle involves multiple behind the scenes steps.
You are able to see the bundle progress through these steps by
:ref:`watching the bundle information <example-pd-bundleinfo>` and the ``state``
value as it builds. Below is the list of statuses the bundle will go through.

* ``Requested``: This is the first status a brand new bundle will be in. This
status indicates that a new order is ready for set up.
* ``IFDsCreated``: Ports are set up in both the source and destination
facilities
* ``VCCreated``: A virtual circuit is set up between the two new ports
* ``BillingAdded``: Billing information as been associated with the new ports
and new virtual circuit
* ``Testing``: Everything is set up and ready for the customer's final
authorization of provisioning
* ``BillingEnabled``: The customer is now being billed for this bundle
* ``Active``: The bundle is set up and ready for use

When a bundle is removed, it is also a multistep process. These statuses are
also visible to you, if you watch the bundle's information as it is removed.

* ``BillingRemoved``: Billing of this bundle has ended
* ``IFLsDestroyed``: Logical links have been removed
* ``VCDestroyed``: The virtual circuit between the two ports is deleted
* ``IFDsDestroyed``: The two ports have been removed and are no longer associated
with the customer
* ``Inactive``: The final status. Everything has been removed and is no longer
accessible to the customer.
