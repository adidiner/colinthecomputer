import pika


def fanout_publish(message, host, port, *, segment):
    """Fanout publish message to queue, on a given segment.
    
    The message is published to all subscribers on the segment.
    :param message: message to be published
    :type message: json
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param segment: segment to be published to
    :type segment: str
    """
    # Set up rabbitmq connectin
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  port=port))
    channel = connection.channel()

    # Message is published to all queues binded to exchange
    _exchange_declare(channel, exchange=segment, exchange_type='fanout')

    print(f"PUBLISHING TO {segment}")
    channel.basic_publish(exchange=segment,
                          routing_key='',
                          body=message)
    connection.close()


def topic_publish(message, host, port, *, topic, segment):
    """Topic publish message to queue, on a given segment.
    
    The message will be routed by the given topic, 
    meaning only subscribers subscribed to the given topic 
    will receive the message.
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
    """
    # Set up rabbitmq connectin
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  port=port))
    channel = connection.channel()

    # Message is published to all queues binded to exchange
    _exchange_declare(channel, exchange=segment, exchange_type='direct')

    print(f"PUBLISHING TO {segment}")
    channel.basic_publish(exchange=segment,
                          routing_key=topic,
                          body=message)

    connection.close()


def fanout_consume(on_message, host, port, topic, segment):
    """Consume fanout-published messages, perform on_message when receiving.

    Topic is used to specify the type of the consumer - 
    if several comsumers are active with the same topic,
    the messages will be distributed between them.
    :param on_message: an action to perform when receiving message,
    arguments are the topic and the message body
    :type on_message: function
    :param host: mq host address
    :type host: str
    :param port: mq port
    :type port: int
    :param topic: the consumers topic, determining the work queue it will wait on
    :type topic: str
    :param segment: segment to be consumed from
    :type segment: str
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  port=port))
    channel = connection.channel()
    _exchange_declare(channel, exchange=segment, exchange_type='fanout')

    # Wait in queue based on topic
    result = channel.queue_declare(queue=topic, exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=segment,
                       queue=queue_name,
                       routing_key=topic)
    print(f"queue binded, exchange={segment}, topic={topic}")

    # Perform on_message when message received, ack the handeling
    def callback(ch, method, properties, body):
        topic = method.routing_key
        on_message(topic, body)
        ch.basic_ack(delivery_tag = method.delivery_tag) # TODO: huh?

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()
    connection.close()


def topic_consume(on_message, host, port, topics, segment):
    """Consume topic-published messages, perform on_message when receiving.
    
    Consumes all messages published with the specified topics.
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
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  port=port))
    channel = connection.channel()
    _exchange_declare(channel, exchange=segment, exchange_type='direct')

    for topic in topics:
        # Wait in queue based on topic
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=segment,
                           queue=queue_name,
                           routing_key=topic)
        print(f"queue binded, exchange={segment}, topic={topic}")

        # Perform on_message when message received, ack the handeling
        def callback(ch, method, properties, body):
            topic = method.routing_key
            on_message(topic, body)
            ch.basic_ack(delivery_tag = method.delivery_tag) # TODO: huh?

        channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()
    connection.close()


def _exchange_declare(channel, exchange, exchange_type):
    """Declare exchange through channel,
    handle conflicting declaration and raise exception to user.
    
    TODO
    :param channel: channel to be declared from
    :type channel: [type]
    :param exchange: [description]
    :type exchange: [type]
    :param exchange_type: [description]
    :type exchange_type: [type]
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
        raise RuntimeError("Cannot publish to segment which is already in use " \
                           "by a different publishing method") 
