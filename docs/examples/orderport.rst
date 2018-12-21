.. _example-orderport:

Ordering a Port
===============

Ordering a port is a series of API calls. These calls are to gather all the required
information needed to make the completed order, then finally placing the order.

.. _example-orderport-billingid

Find our billing_id
-------------------

A new port needs to be associated with your billing account. This can be accomplished
by :ref:`finding your billing_id <functions-billingid>`.

.. _example-orderport-popid

Getting pop_id
--------------

A new port needs to be located in a specific spot. You can find the associated ``pop_id``
of where you'd like a port by :ref:`finding your ``pop_id`` <functions-popid>`.

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

    endpoint = 'ports'

    params = {
        'billing_account': billing_id,
        'description': description,
        'media': media_type,
        'pop_id': pop_id,
        'speed': speed,
        'subscription_term': subscription_term,
        'zone': zone
    }
    query_string = generate_query_string(params)
    r = requests.post(generate_full_endpoint(api_url, endpoint, valid_secrets), json=params)

One important note, here, is that the final ``.post()`` is sent using the ``json`` parameter, not
the ``data`` parameter.

.. _example-orderport-conclusion

Finishing up
------------

Congratulations! You've now ordered and activated a single port. This entire process
should take about a minute, with the majority of that time spent waiting
for provisioning to complete. Billing for this new port will begin automatically
after 15 days.
