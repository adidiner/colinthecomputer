from furl import furl
import colinthecomputer.mq_drivers as drivers


class Worker:
    """Worker which handles the consuming and publishing 
    between the parsers and the message queue.
    
    :param mq_url: a url describing the mq, in the form 'mq://host:port'
    :type mq_url: str
    """
    def __init__(self, mq_url):
        mq_url = furl(mq_url)
        mq, self.host, self.port, self.mq_url = mq_url.scheme, mq_url.host, mq_url.port, mq_url
        self.driver = drivers[mq]

    def __repr__(self):
        return f'Worker(mq_url={mq_url})'

    def work(self, parser, field):
        """Consumes messages from the message queue, feeding them to the parser.
        Publish the parser's results back to the queue.
        
        :param parser: a parsing function / class(TODO)
        :type parser: function, class(TODO)
        :param field: the field the parser handles
        :type field: str
        """
        def on_message(topic, message):
            self.driver.topic_publish(parser(message), self.host, self.port, topic=field, segment='results') 
        self.driver.fanout_consume(on_message, self.host, self.port, topic=field, segment='raw_data')
