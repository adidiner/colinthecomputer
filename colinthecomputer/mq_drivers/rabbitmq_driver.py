import pika


def task_publish(message, host, port, *, segment):
    """
    Publish task message to queue, on a given segment.

    The message is published to all subscribered workers on the segment.
    The task will be consumed by a single worker of each kind
    (see task_consume).
    """
    connection, channel = _setup(host, port)
    # Message is published to all queues binded to exchange
    _exchange_declare(channel, exchange=segment, exchange_type='fanout')

    channel.basic_publish(exchange=segment,
                          routing_key='',
                          body=message)
    connection.close()


def share_publish(message, host, port, *, topic, segment):
    """
    Share message to queue, on a given segment.

    The message will be routed by the given topic,
    meaning only subscribers subscribed to the given topic
    will receive the message.
    All subscribers of a topic will receive the message.
    """
    connection, channel = _setup(host, port)
    # Message is published to all queues binded to exchange
    _exchange_declare(channel, exchange=segment, exchange_type='direct')

    channel.basic_publish(exchange=segment,
                          routing_key=topic,
                          body=message)
    connection.close()


def task_consume(on_message, host, port, *, topic, segment):
    """
    Consume tasks, perform on_message when receiving.

    Topic is used to specify the type of the worker -
    if several workers are active with the same topic,
    the tasks will be distributed between them.
    """
    connection, channel = _setup(host, port)
    _exchange_declare(channel, exchange=segment, exchange_type='fanout')

    # Wait in queue based on topic
    result = channel.queue_declare(queue=topic)
    queue_name = result.method.queue
    channel.queue_bind(exchange=segment,
                       queue=queue_name,
                       routing_key=topic)

    # Perform on_message when message received
    def callback(ch, method, properties, body):
        topic = method.routing_key
        on_message(topic, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()
    connection.close()


def share_consume(on_message, host, port, *, topics, segment):
    """
    Consume shared messages, perform on_message when receiving.

    Consumes all messages published with the specified topics.
    All consumers of a given topic will view the shared message.
    """
    connection, channel = _setup(host, port)
    _exchange_declare(channel, exchange=segment, exchange_type='direct')

    for topic in topics:
        # Wait in queue based on topic
        result = channel.queue_declare(queue='')
        queue_name = result.method.queue
        channel.queue_bind(exchange=segment,
                           queue=queue_name,
                           routing_key=topic)

        # Perform on_message when message received
        def callback(ch, method, properties, body):
            topic = method.routing_key
            on_message(topic, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()
    connection.close()


def _setup(host, port):
    """
    Setup pika connection.

    :param host: connection host
    :type host: str
    :param port: connection port
    :type port: str
    :returns: connection and connection channel
    :rtype: (pika.BlockingConnection, pika.channel.Channel)
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  port=port))
    channel = connection.channel()
    return connection, channel


def _exchange_declare(channel, exchange, exchange_type):
    """
    Declare exchange through channel,
    handle conflicting declaration and raise exception to user.

    :param channel: channel to be declared from
    :type channel: pika.channel.Channel
    :param exchange: exchange name
    :type exchange: str
    :param exchange_type: fanout or direct
    :type exchange_type: str
    :raises: RuntimeError
    """
    try:
        channel.exchange_declare(exchange=exchange,
                                 exchange_type=exchange_type)
    # If exchange was declared with a different type, declaration will fail
    except pika.exceptions.ChannelClosedByBroker as e:
        reply_code, = e.args
        if reply_code != 406:
            raise
        raise RuntimeError("Cannot publish to segment which is already in use"
                           " by a different publishing method")
