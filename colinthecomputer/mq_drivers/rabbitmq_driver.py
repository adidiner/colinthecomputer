import pika

def publish(message, host, port, *, segment='', topic=None):
    ''' Publish message to queue on host:port,
     in the specified segment.
    If topic is specified, direct publish to topic as routing key.
    Otherwise, fanout to all queues in segemnt (exchange). '''
    # TODO: once topic is None, it HAS to be fanout, if topic is something, it HAS to be direct
    if not topic:
        exchange_type = 'fanout'
        routing_key = ''
    else:
        exchange_type = 'direct'
        routing_key = topic
    # Set up rabbitmq connectin
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  port=port))
    channel = connection.channel()

    # Message is published to all queues binded to exchange
    try:
        channel.exchange_declare(exchange=segment, 
                                 exchange_type=exchange_type)
    # If exchange was declared with a different type, declaration will fail
    except pika.exceptions.ChannelClosedByBroker as e:
        reply_code, = e.args
        if reply_code != 406:
            raise
        raise RuntimeError("Cannot publish to segment which is already in use " \
                           "by a different publishing method") 

    print(f"PUBLISHING TO {segment}")
    channel.basic_publish(exchange=segment,
                          routing_key=routing_key,
                          body=message)

    connection.close()

def fanout_publish(message, host, port, *, segment=''):
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


def topic_publish(message, host, port, topic, *, segment=''):
    # TODO: once topic is None, it HAS to be fanout, if topic is something, it HAS to be direct
    exchange_type = 'direct'
    routing_key = topic
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


def _exchange_declare(channel, exchange, exchange_type):
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


def consume(on_message, host, port, segment='', queue='', topics=None):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  port=port))
    channel = connection.channel()
    if not topics:
        topics = ['']

    for topic in topics:
        # Wait in queue based on topic
        result = channel.queue_declare(queue=queue, exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=segment,
                           queue=queue_name,
                           routing_key=topic)
        print(f"queue binded, exchange={segment}, queue={queue}, topic={topic}")

        # Perform on_message when message received, ack the handeling
        def callback(ch, method, properties, body):
            topic = method.routing_key
            on_message(topic, body)
            ch.basic_ack(delivery_tag = method.delivery_tag) # TODO: huh?

        channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()
    connection.close()

def fanout_consume(on_message, host, port, segment='', topic=''):
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

def topic_consume(on_message, host, port, segment='', topics):
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