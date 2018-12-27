.. _example-orderbundle-packetcorhosted:

Hosted PacketCOR Products
=========================

PacketCOR is PacketFabric’s array of cloud on-ramp solutions, offering private,
secure, and cost-effective connectivity to your preferred Cloud Service
Providers. From any of the on-net locations, you can connect to one of a cloud
service partners at speeds starting at 1Gbps.

PacketFabric's cloud providers include Amazon, Google, Microsoft, Packet and more
being added as you read this.

PacketCOR is an add-on product; you'll need an Physical Interface to gain
access to the fabric. Each instance of PacketCOR allows you to connect to a
single cloud provider. With your Physical Interface, you can order multiple
PacketCORs for services offered by multiple cloud providers (storage offered
by AWS, and compute offered by Azure, for just one example).

There are two different pricing models for PacketCOR. Not all partners offer
both methods. However, for those that do, you have the options of either
``Hosted`` or ``Dedicated``. The difference between these two models can be
seen on the `PacketFabric PacketCOR  <https://packetfabric.com/packetcor>`__

Let's go through how to order different PacketCOR products to different cloud
service providers.

The first step with all of these will be to find our ``billing_id``. This can be
accomplished by :ref:`finding your billing_id <functions-billingid>`.

.. _example-orderbundle-awshostedpublic:

AWS PacketCOR Hosted - Public
-----------------------------

We want to find where we can connect. This will be
similar to :ref:`finding your pop_id <functions-popid>`, but we want to search
by cloud provider instead of by market. If you know your market, you can follow
those steps and get the ``pop_id``. For this example, we're going to see what
is available though.

::

    endpoint = 'locations'
    params = {'cloud_provider': 'aws', 'cloud_port_type': 'hosted'}
    query_string = generate_query_string(params)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This is going to return a list of all sites that have AWS Dedicated PacketCOR
functionality. Select the ``pop_id`` you wish to use. You will also need to get
the value of ``['sites']['aws_region']`` for the site you will use. AWS requires
this when building the connection.

Next you'll need to know which interface you want to use to connect to Amazon.
In this example, we'll be using ``ifd_id`` 4257. We received this when we
:ref:`created a port <example-orderport-orderport>`, but you could also find it
by iterating of your `available interfaces <https://docs.packetfabric.com/#api-Interface-GetInterfacesPhysical>`__

After this, you'll need to gather your ``asn``, ``aws_account_id`` and need to know
your router's IP address, the Amazon IP address and route prefixes you want to advertise.

Last, you'll need a ``bgp_key`` for this connection.

::

    pc_hosted_aws = {
        "ifd_id":4257,
        "description":"AWS Hosted Public",
        "asn":YOURASN,
        "aws_account_id":"YOURACCOUNTID",
        "aws_region":"us-east-1",
        "aws_vif_type":"public",
        "billing_account":"70907",
        "bgp_key":"YOURBGPKEY",
        "speed":"3Gbps",
        "vlan_id":95,
        "aws_router_peer_ip":"10.100.5.198/30",
        "cust_router_peer_ip":"10.100.5.197/30",
        "aws_route_filter_prefixes":["10.100.5.196/30"]
    }

This payload will create a public 3Gbps connection to Amazon's us-east-1 region and your
PacketFabric interface with an ``ifd_id`` of 4257.

::

    endpoint = "packet-cor/aws/hosted"
    params = pc_hosted_aws
    r = requests.post(gbl.generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This will take a minute or two to provision. When it's done, you'll have a public AWS
PacketCOR Hosted interface. You will want to grab the value of ``r.json()['pc_id']``
from the response. This is your PacketCOR ID, and it is needed if you want to
check the :ref:`status of the provisioning <example-orderbundle-packetcorstatus>` process
(or perform other actions against this PacketCOR product).


.. _example-orderbundle-awshostedprivate:

AWS PacketCOR Hosted - Private
------------------------------

We want to find where we can connect. This will be
similar to :ref:`finding your pop_id <functions-popid>`, but we want to search
by cloud provider instead of by market. If you know your market, you can follow
those steps and get the ``pop_id``. For this example, we're going to see what
is available though.

::

    endpoint = 'locations'
    params = {'cloud_provider': 'aws', 'cloud_port_type': 'hosted'}
    query_string = generate_query_string(params)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This is going to return a list of all sites that have AWS Dedicated PacketCOR
functionality. Select the ``pop_id`` you wish to use. You will also need to get
the value of ``['sites']['aws_region']`` for the site you will use. AWS requires
this when building the connection.

Next you'll need to know which interface you want to use to connect to Amazon.
In this example, we'll be using ``ifd_id`` 4257. We received this when we
:ref:`created a port <example-orderport-orderport>`, but you could also find it
by iterating of your `available interfaces <https://docs.packetfabric.com/#api-Interface-GetInterfacesPhysical>`__

After this, you'll need to gather your ``asn``, ``aws_account_id`` and need to know
your router's IP address and the Amazon IP address. This is a private connection,
so we won't be supplying the advertised routes.

Last, you'll need a ``bgp_key`` for this connection.

::

    pc_hosted_aws = {
        "ifd_id":4257,
        "description":"AWS Hosted Private",
        "asn":YOURASN,
        "aws_account_id":"YOURACCOUNTID",
        "aws_region":"us-east-1",
        "aws_vif_type":"private",
        "billing_account":"70907",
        "bgp_key":"YOURBGPKEY",
        "speed":"3Gbps",
        "vlan_id":95,
        "aws_router_peer_ip":"10.100.5.198/30",
        "cust_router_peer_ip":"10.100.5.197/30"
    }

This payload will create a 3Gbps connection to Amazon's us-east-1 region and your
PacketFabric interface with an ``ifd_id`` of 4257.

::

    endpoint = "packet-cor/aws/hosted"
    params = pc_hosted_aws
    r = requests.post(gbl.generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This will take a minute or two to provision. When it's done, you'll have a private AWS
PacketCOR Hosted interface. You will want to grab the value of ``r.json()['pc_id']``
from the response. This is your PacketCOR ID, and it is needed if you want to
check the :ref:`status of the provisioning <example-orderbundle-packetcorstatus>` process
(or perform other actions against this PacketCOR product).


.. _example-orderbundle-googlehosted:

Google PacketCOR Hosted
-----------------------

Setting up a PacketCOR hosted with Google, requires that you have a pairing key
from Google. You can find this in your Google Account console.

Next you'll need to know which interface you want to use to connect to Google.
In this example, we'll be using ``ifd_id`` 4257. We received this when we
:ref:`created a port <example-orderport-orderport>`, but you could also find it
by iterating of your `available interfaces <https://docs.packetfabric.com/#api-Interface-GetInterfacesPhysical>`__

We want to find where we can connect. This will be
similar to :ref:`finding your pop_id <functions-popid>`, but we want to search
by cloud provider instead of by market. If you know your market, you don't need
to perform this search. You'll just need the ``market_code``.

::

    endpoint = 'locations'
    params = {'cloud_provider': 'google', 'cloud_port_type': 'hosted'}
    query_string = generate_query_string(params)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

We now have everything that is required to order a Google PacketCOR hosted instance.

::

    pc_hosted_google = {
        "billing_account": 70907,
        "description": "Google PacketCOR Hosted",
        "google_pairing_key": "google-pairing-key/region/zone",
        "ifd_id_src": 4257,
        "market_code_dest": "DA1",
        "speed": "1Gbps",
        "vlan_id": 12
    }

This payload will created a 1Gbps connection to the ``DA1`` market using our provided
pairing key and our PacketFabric interface with ``ifd_id`` 4257.

::

    endpoint = "packet-cor/google/hosted"
    params = pc_hosted_google
    r = requests.post(gbl.generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This will take a minute or two to provision. When it's done, you'll have a Google
PacketCOR Hosted interface. You will want to grab the value of ``r.json()['pc_id']``
from the response. This is your PacketCOR ID, and it is needed if you want to
check the :ref:`status of the provisioning <example-orderbundle-packetcorstatus>` process
(or perform other actions against this PacketCOR product).


.. _example-orderbundle-packethosted:

Packet PacketCOR Hosted
-----------------------

You'll need to know which interface you want to use to connect to Packet.
In this example, we'll be using ``ifd_id`` 4257. We received this when we
:ref:`created a port <example-orderport-orderport>`, but you could also find it
by iterating of your `available interfaces <https://docs.packetfabric.com/#api-Interface-GetInterfacesPhysical>`__

We want to find where we can connect. This will be
similar to :ref:`finding your pop_id <functions-popid>`, but we want to search
by cloud provider instead of by market. If you know your market, you don't need
to perform this search. You'll just need the ``market_code``.

::

    endpoint = 'locations'
    params = {'cloud_provider': 'packet', 'cloud_port_type': 'hosted'}
    query_string = generate_query_string(params)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

After this, you'll need to gather your ``asn``, ``aws_account_id`` and need to know
your router's IP address, the Amazon IP address and route prefixes you want to advertise.

Last, you'll need a ``bgp_key`` for this connection.

::

    pc_hosted_packet = {
        "ifd_id_src": 4257,
        "description": "Packet PacketCOR Hosted",
        "asn": YOURASN,
        "bpg_key": "YOURBGPKEY",
        "billing_account": "70907",
        "market_code_dest": "DA1",
        "route_filter_prefixes_packet": ["10.100.5.196/30"],
        "router_ip_packet": "10.100.5.198/30",
        "router_ip_cust": "10.100.5.197/30",
        "speed": "5Gbps",
        "vlan_id": 7
    }

This payload will create a 5Gbps connection to Packet in the ``DA1`` market and your
PacketFabric interface with an ``ifd_id`` of 4257.

This will take 24-72 hours to fully provision. When it is complete, you'll have a
Packet PacketCOR Hosted interface. When the call above is completed, you'll want
to grab the value of ``r.json()['pc_id']`` from the response. This is your
PacketCOR ID, and it is needed if you want to check the
:ref:`status of the provisioning <example-orderbundle-packetcorstatus>` process
(or perform other actions against this PacketCOR product). Since this product takes
so long to completely provision, it's a good idea to keep this ID handy so that you
can check the status later.


.. _example-orderbundle-azurehosted:

Azure PacketCOR Hosted
----------------------

Setting up a PacketCOR hosted with Azure, requires that you have a service key
from Microsoft. You can validate this service key by passing it to PacketFabric's
`validation check <https://docs.packetfabric.com/#api-PacketCOR_Azure-GetPacketCORAzureServiceKeyValidation>`__
If it says the key is not valid, you will need to get another one from Microsoft.

::

    service_key = "YOURSERVICEKEY"
    endpoint = 'packet-cor/azure/service-key/{}/validation'.format(service_key)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets))

In ``r.json()`` you should find that ``is_valid`` is ``True``.

Once this key has been validated we want to find where we can connect. This will be
similar to :ref:`finding your pop_id <functions-popid>`, but we want to search
by cloud provider instead of by market. If you know your market, you don't need
to perform this search. You'll just need the ``market_code``.

You'll need to know which interface you want to use to connect to Packet.
In this example, we'll be using ``ifd_id`` 4257. We received this when we
:ref:`created a port <example-orderport-orderport>`, but you could also find it
by iterating of your `available interfaces <https://docs.packetfabric.com/#api-Interface-GetInterfacesPhysical>`__

Finally, you'll need to gather either the private peering VLAN ID, Microsoft peering
VLAN ID or both (you need one or both IDs).

::

    pc_hosted_azure = {
        "ifd_id_src": 4257,
        "description": "Azure PacketCOR Hosted",
        "billing_account": "70907",
        "azure_service_key": "YOURSERVICEKEY",
        "market_code_dest": "DA1",
        "speed": "1Gbps",
        "vlan_id_private": 7,
        "vlan_id_microsoft": 8
    }

This payload will create a Hosted PacketCOR with a speed of 1Gbps. It will create
use both private peering and Microsoft peering (because both VLAN IDs are provided).

This will take 24-72 hours to fully provision. When it is complete, you'll have an
Azure PacketCOR Hosted interface. When the call above is completed, you'll want
to grab the value of ``r.json()['pc_id']`` from the response. This is your
PacketCOR ID, and it is needed if you want to check the
:ref:`status of the provisioning <example-orderbundle-packetcorstatus>` process
(or perform other actions against this PacketCOR product). Since this product takes
so long to completely provision, it's a good idea to keep this ID handy so that you
can check the status later.
