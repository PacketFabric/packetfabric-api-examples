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
