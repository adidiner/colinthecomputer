from furl import furl
import colinthecomputer.mq_drivers as drivers


def produce_consumer(mq_url):
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]

    def consume(saver):
    	def on_message(topic, message):
    		saver.save(topic, message)
    	driver.topic_consume(on_message, host, port,
    				   topics=['user', 'pose', 'color_image', 'depth_image', 'feelings'],
    				   segment='results')

    return consume