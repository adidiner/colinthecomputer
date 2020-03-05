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
    channel.exchange_declare(exchange=segment, 
                             exchange_type=exchange_type)

    channel.basic_publish(exchange=segment,
                          routing_key=routing_key,
                          body=message)

    connection.close()


def consume(on_message, host, port, segment='', topics=None):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  port=port))
    channel = connection.channel()
    if not topics:
        topics = ['']

    for topic in topics:
        # Wait in queue based on topic
        channel.queue_declare(queue=topic)
        channel.queue_bind(exchange=segment,
                           queue=topic)
        print(f"queue binded, exchange={segment}, queue={topic}")

        # Perform on_message when message received, ack the handeling
        def callback(ch, method, properties, body):
            topic = method.routing_key
            on_message(topic, body)
            ch.basic_ack(delivery_tag = method.delivery_tag) # TODO: huh?

        channel.basic_consume(queue=topic, on_message_callback=callback)

    channel.start_consuming()
    connection.close()