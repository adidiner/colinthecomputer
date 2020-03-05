from furl import furl
from colinthecomputer.mq_drivers import rabbitmq_driver
drivers = {'rabbitmq':rabbitmq_driver}


def produce_consumer(mq_url):
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]

    def consume(saver):
    	def on_message(topic, message):
    		print(topic, message)
    		saver.save(topic, message)
    	driver.consume(on_message, host, port, segment='results', 
    				   topics=['user', 'pose', 'color_image', 'depth_image', 'feelings'])

    return consume