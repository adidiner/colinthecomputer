colinthecomputer.client.read\_drivers package
=============================================

Auto imported read drivers.
When importing the package, it will expose the available read drivers as a dictionary.
i.e:

.. code-block:: python

    import read_drivers
    driver = read_drivers['binary']

Adding a file named ``"redguy_driver"`` to the pacakge 
will automaticaly expose the driver via ``read_drivers['redguy']``.

A read driver must supply the ``read_user`` and ``read_snapshot`` methods.

.. method:: read_user(stream)

    Read user information from stream.
    
    :param stream: data stream, beginning with the user information
    :type stream: bytes-like object
    :returns: size of read data
    :rtype: ``int``

.. method:: read_snapshot(stream)

    Read snapshot from stream.
    
    :param stream: data stream, beginning with the snapshot
    :type stream: bytes-like object
    :returns: size of read data
    :rtype: ``int``


Submodules
----------

colinthecomputer.client.read\_drivers.binary\_driver module
-----------------------------------------------------------

Supports the above methods.

Reads binary format sample (but exposes protobuf snapshots).

colinthecomputer.client.read\_drivers.protobuf\_driver module
-------------------------------------------------------------

Supports the above methods.

Reads protobuf format snapshots.
