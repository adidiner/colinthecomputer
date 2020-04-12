from furl import furl
import colinthecomputer.mq_drivers as drivers


def produce_consumer(mq_url):
    """Produce a consume function for the parsers,
    handling the communication with the given message queue/
    
    :param mq_url: a url describing the mq, in the form 'mq://host:port'
    :type mq_url: str
    :returns: a consume function
    :rtype: function
    """
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]

    def consume(parser, field):
        """Consumes messages from the message queue, feeding them to the parser.
        Publish the parser's results back to the queue.
        
        :param parser: a parsing function / class(TODO)
        :type parser: function, class(TODO)
        :param field: the field the parser handles
        :type field: str
        """
        def on_message(topic, message):
            driver.topic_publish(parser(message), host, port, topic=field, segment='results') 
        driver.fanout_consume(on_message, host, port, topic=field, segment='raw_data')

    return consume