.. _example-orderbundle-packetcordedicated-aws:

Ordering a Dedicated PacketCOR (AWS)
==========================

A dedicated, exclusive connection to Amazon's public cloud resources can
be provisioned with the Dedicated PacketCOR product. In the near future, these
connection types will be available to other cloud providers too.

The example below will walk you through ordering a dedicated PacketCOR.

.. _example-pcawsdedicated-billingid

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

.. example-pcawsdedicated-region

Find Available AWS regions
--------------------------

To set up an AWS PacketCOR, we need to determine which regions are available.

::

    api_url = 'https://api.packetfabric.com'
    api_key = '1-1111111'
    api_secret = 'ABCDEF012345678'

    endpoint = '{}/packet-cor/aws/regions'.format(api_url)
    params = {'api_key': api_key}
    query_string = generate_query_string(params)
    r = requests.get("{}?{}&auth_hash={}".format(endpoint, query_string,
        generate_hash(api_secret, query_string)))
    region_id = r.json()[0]['region']

The result of ``r.json()`` will be a list of available AWS regions and a
short description to help you determine where it is located.

.. example-pcawsdedicated-order

Place the order
---------------

This step assumes that you know the source port id. You can find this either in the portal or
via the `interfaces <https://docs.packetfabric.com/#api-Interface-GetInterfacesPhysical>`__
call. You want the ``ifd_id`` value from that response. If you have more than two ports,
you will need to determine which port you want to use. You will also need the ``pop_id``
of your destination. This can be found via the `locations <https://docs.packetfabric.com/#api-Location-Getlocations>`__
call. The destination should have an ``aws_region`` equal to the value you previously
selected.

The available speeds are ``1Gbps`` or ``10Gbps``.

::

    endpoint = '{}/packet-cor/aws/dedicated'.format(api_url)
    params = {
        'pc_ifd_id_src': 1289,
        'pc_pop_id_dest': 2,
        'pc_speed': '10Gbps',
        'pc_zone_dest': 'A',
        'pc_vlan_id': 229,
        'pc_description': 'A description that is useful to you',
        'aws_region': region_id,
        'billing_account': billing_id,
        'subscription_term': 12,
    }
    r = requests.post(gbl.generate_full_endpoint(endpoint, valid_secrets), json=params)

Provisioning will take a few minutes.


.. _example-pcawsdedicated-conclusion

Finishing up
------------

Congratulations! You've now ordered and activated an AWS PacketCOR. This entire
process should take a little over 2 minutes.
