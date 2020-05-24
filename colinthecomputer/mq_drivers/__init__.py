"""Auto imported mq drivers.
When importing the package,
it will expose the available mq drivers as a dictionary.
i.e:
    import mq_drivers
    driver = mq_drivers['rabbitmq']
Adding a file named "yellowguy_driver" to the pacakge
will automaticaly expose the driver via mq_drivers[yellowguy'].
A meesage queue driver must supply task_publish,
task_cosume and share_publish, share_consume.

task_publish:
    Publish task message to queue, on a given segment.

    The message is published to all subscribered workers on the segment.
    The task will be consumed by a single worker of each kind
    (see task_consume).
    :param message: message to be published
    :type message: json
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param segment: segment to be published to
    :type segment: str

share_publish:
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

task_consume:
    Consume tasks, perform on_message when receiving.

    Topic is used to specify the type of the worker -
    if several workers are active with the same topic,
    the tasks will be distributed between them.
    :param on_message: an action to perform when receiving message,
    arguments are the topic and the message body
    :type on_message: function
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param topic: the consumers topic,
                  determining the work queue it will wait on
    :type topic: str
    :param segment: segment to be consumed from
    :type segment: str

share_consume:
    Consume shared messages, perform on_message when receiving.

    Consumes all messages published with the specified topics.
    All consumers of a given topic will view the shared message.
    :param on_message: an action to perform when receiving message,
    arguments are the topic and the message body
    :type on_message: function
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param topic: the topics to consume from
    :type topic: str
    :param segment: segment to be consumed from
    :type segment: str
"""

import sys
import os
import pathlib

from colinthecomputer.utils import load_modules, load_drivers


root = pathlib.Path(os.path.dirname(__file__))
modules = load_modules(root)
drivers = load_drivers(modules)
sys.modules[__name__] = drivers
