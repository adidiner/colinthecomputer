from furl import furl
import colinthecomputer.mq_drivers as drivers


def produce_consumer(mq_url):
	"""[summary]
	
	[description]
	:param mq_url: [description]
	:type mq_url: [type]
	:returns: [description]
	:rtype: {[type]}
	"""
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]

    def consume(parser, field):
        def on_message(topic, message):
            driver.topic_publish(parser(message), host, port, topic=field, segment='results') 
        driver.fanout_consume(on_message, host, port, topic=field, segment='raw_data')

    return consume