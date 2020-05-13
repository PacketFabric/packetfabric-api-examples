.. _example-orderbundle-packetcordedicated:

Dedicated PacketCOR Products
============================

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

.. _example-orderbundle-awsdedicated:

AWS PacketCOR Dedicated
-----------------------

We want to find where we can connect our dedicated connection. This will be
similar to :ref:`finding your pop_id <functions-popid>`, but we want to search
by cloud provider instead of by market. If you know your market, you can follow
those steps and get the ``pop_id``. For this example, we're going to see what
is available though.

::

    endpoint = 'locations'
    params = {'cloud_provider': 'aws', 'cloud_port_type': 'dedicated'}
    query_string = generate_query_string(params)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This is going to return a list of all sites that have AWS Dedicated PacketCOR
functionality. Select the ``pop_id`` you wish to use. You will also need to get
the value of ``['sites']['aws_region']`` for the site you will use. AWS requires
this when building the connection.

Once you have the ``pop_id`` and ``aws_region``, you are ready to create your
AWS PacketCOR Dedicated interface.

::

    pc_dedicated_aws = {
        "pop_id_dest": 2,
        "speed": "10Gbps",
        "subscription_term": "12",
        "zone_dest": "A",
        "description": "Dedicated AWS PC",
        "aws_region": "us-east-1",
        "billing_account":"70907",
        "service_class": "longhaul"
    }

This payload is going to create a 10Gbps port, in your PacketFabric Zone A for
a 12 month term. It will be associated with ``aws_region`` ``us-east-1`` and your
billing account of ``70907`` (which you found earlier when you
:ref:`found your billing_id <functions-billingid>`).

::

    endpoint = "packet-cor/aws/dedicated"
    params = pc_dedicated_aws
    r = requests.post(gbl.generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This will take about a minute to provision. When it's done, you'll have an AWS
PacketCOR Dedicated interface that you can connect virtual circuits to. You will
want to grab the value of ``r.json()['pc_id']`` from the response. This is your
PacketCOR ID, and it is needed if you want to check the :ref:`status of the provisioning <example-orderbundle-packetcorstatus>`
process (or perform other actions against this PacketCOR product).


.. _example-orderbundle-googlededicated:

Google PacketCOR Dedicated
--------------------------

We want to find where we can connect our dedicated connection. This will be
similar to :ref:`finding your pop_id <functions-popid>`, but we want to search
by cloud provider instead of by market. If you know your market, you can follow
those steps and get the ``pop_id``. For this example, we're going to see what
is available though.

::

    endpoint = 'locations'
    params = {'cloud_provider': 'google', 'cloud_port_type': 'dedicated'}
    query_string = generate_query_string(params)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This is going to return a list of all sites that have Google Dedicated PacketCOR
functionality. Select the ``pop_id`` you wish to use.

Once you have the ``pop_id``, you are ready to create your Google PacketCOR
Dedicated interface.

::

    pc_dedicated_google = {
        "billing_account": 70972,
        "description": "GPC Testing - dedicated",
        "pop_id_dest": 1,
        "service_class": "longhaul",
        "speed": "10Gbps",
        "subscription_term": 12,
        "zone_dest": "A"
    }

This payload is going to create a 10Gbps port, in your PacketFabric Zone A for
a 12 month term. It will be associated with your billing account of ``70907``
(which you found earlier when you :ref:`found your billing_id <functions-billingid>`).

::

    endpoint = "packet-cor/google/dedicated"
    params = pc_dedicated_google
    r = requests.post(gbl.generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

This will take about a minute to provision. When it's done, you'll have an Google
PacketCOR Dedicated interface that you can connect virtual circuits to. You will
want to grab the value of ``r.json()['pc_id']`` from the response. This is your
PacketCOR ID, and it is needed if you want to check the :ref:`status of the provisioning <example-orderbundle-packetcorstatus>`
process (or perform other actions against this PacketCOR product).


.. _example-orderbundle-packetcoraddvc:

Add a virtual circuit to your PacketCOR
---------------------------------------

Now that you've set up a Dedicated PacketCOR, you will want to use it to connect
to your cloud provider. You can do this by building a virtual circuit between
one of your PacketFabric ports (which you can do provision by
:ref:`creating a port <example-orderport-orderport>`) and the new PacketCOR
product we just provisioned. Documentation for this is available
`here <https://docs.packetfabric.com/api/#api-PacketCOR-PostPacketCORVirtualCircuit>`__

For this we will need a few bits of information. First, you'll need your ``ifd_id``
for the port you wish to connect to the PacketCOR instance. Next, you'll need your
``pc_id`` of the the PacketCOR instance we provisioned. Last, you'll need to
determine if you want to use this PacketCOR for metro connections only or if you'll
use longhaul connections as well. This will affect how you are billed and where you can
connect to the PacketCOR instance from.

::

    params = {
        "pc_id": 184,
        "ifd_id_src": 4257,
        "billing_account": 70972,
        "billing_product_type": "packetcor_dedicated_vc_longhaul",
        "vlan_id_src": 42,
        "vlan_id_dest": "12"
    }

This payload will create a virtual circuit between ``ifd_id`` 4257 and PacketCOR
instance 184. This will be a longhaul product and the appropriate VLAN IDs are
provided based on my existing infrastructure.

This will take about a minute to provision. You can monitor progress via the
same ``status`` endpoint you used to check when the
:ref:`PacketCOR instance was provisioning <example-orderbundle-packetcorstatus>`

You can add multiple virtual circuits from multiple locations to this PacketCOR
dedicated instance.


.. _example-orderbundle-packetcorstatus:

Check the status of your PacketCOR
----------------------------------

You can check the status of the provisions process by checking it's ``status``
endpoint

::

    pc_id = 184   # This value was found from the .post() response when creating the PacketCOR
    endpoint = "https://api.packetfabric.com/packet-cor/{}/status".format(pc_id)
    r = requests.get(generate_full_endpoint(api_url, endpoint, valid_secrets))

The important key in this response is ``state``. This will tell you the current
status of the PacketCOR. If it is ``Active``, it is ready for you to start attaching
virtual circuits.

The ``all_states`` key tells you how many states this product will need to go
through before it is active. The ``all_state_descriptions`` key provides an
explanation of all possible states a PacketCOR instance could be in.
