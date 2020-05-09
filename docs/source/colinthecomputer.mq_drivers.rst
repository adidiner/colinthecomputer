colinthecomputer.mq\_drivers package
====================================

Auto imported mq drivers.
When importing the package, it will expose the available mq drivers as a dictionary.
i.e:

.. code-block:: python

    import mq_drivers
    driver = mq_drivers['rabbitmq']


Adding a file named ``"yellowguy_driver"`` to the pacakge 
will automaticaly expose the driver via ``mq_drivers[yellowguy']``.

A meesage queue driver must supply ``task_publish``, ``task_cosume`` and ``share_publish``, ``share_consume``.


.. method:: task_publish(message, host, port, *, segment)

    Publish task message to queue, on a given segment.
    
    The message is published to all subscribered workers on the segment.
    The task will be consumed by a single worker of each kind (see task_consume).

    :param message: message to be published
    :type message: json
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param segment: segment to be published to
    :type segment: str

.. method:: share_publish(message, host, port, *, topic, segment)


    Share message to queue, on a given segment.
    
    The message will be routed by the given topic, 
    meaning only subscribers subscribed to the given topic 
    will receive the message.
    All subscribers of a topic will receive the message.

    :param message: message to be published
    :type message: json
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param topic: message topic
    :type topic: str
    :param segment: segment to be published to
    :type segment: str

.. method:: task_consume(on_message, host, port, *, topic, segment)

    Consume tasks, perform on_message when receiving.

    Topic is used to specify the type of the worker - 
    if several workers are active with the same topic,
    the tasks will be distributed between them.

    :param on_message: an action to perform when receiving message, arguments are the topic and the message body
    :type on_message: function
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param topic: the consumers topic, determining the work queue it will wait on
    :type topic: str
    :param segment: segment to be consumed from
    :type segment: str

.. method:: share_consume(on_message, host, port, *, topics, segment)

    Consume shared messages, perform on_message when receiving.
    
    Consumes all messages published with the specified topics.
    All consumers of a given topic will view the shared message.

    :param on_message: an action to perform when receiving message, arguments are the topic and the message body
    :type on_message: function
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param topic: the topics to consume from
    :type topic: str
    :param segment: segment to be consumed from
    :type segment: str


Submodules
----------

colinthecomputer.mq\_drivers.rabbitmq\_driver module
----------------------------------------------------

Supports the above methods.

Uses rabbitmq for the implementation.

