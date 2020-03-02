import pika

def broadcast_publish(message, host, port, segment=''):
        ''' Publish message to queue on host:port,
         in the specified segment (to all topics)'''
        # Set up rabbitmq connectin
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host,
                                                                    port=port))
        channel = connection.channel()

        # Message is published to all queues binded to exchange
        channel.exchange_declare(exchange=segment, 
                                                         exchange_type='fanout')

        channel.basic_publish(exchange=segment,
                                                    routing_key='',
                                                    body=message)

        connection.close()


def consume(on_message, host, port, segment='', topic=''):
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host,
                                                                    port=port))
        channel = connection.channel()

        # Wait in queue based on topic
        channel.queue_declare(queue=topic)
        channel.queue_bind(exchange=segment,
                                             queue=topic)

        # Perform on_message when message received, ack the handeling
        def callback(ch, method, properties, body):
                on_message(body)
                ch.basic_ack(delivery_tag = method.delivery_tag) # TODO: huh?

        channel.basic_consume(queue=topic, on_message_callback=callback)
        channel.start_consuming()
        connection.close()


def topic_publish(message, host, port, segment='', topic=''):
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host,
                                                                    port=port))
        channel = connection.channel()

        # Message is published to all queues binded to exchange
        channel.exchange_declare(exchange=segment, 
                                                         exchange_type='direct')

        channel.basic_publish(exchange=segment,
                                                    routing_key=topic,
                                                    body=message)

        connection.close()

# TODO: topic publish and broadcast publish are the same?