
from furl import furl
from colinthecomputer.mq_drivers import rabbitmq_driver
drivers = {'rabbitmq':rabbitmq_driver}


def produce_consumer(mq_url):
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]

    def consume(parser, field):
    	def on_message(message):
    		driver.publish(parser(message), host, port, segment='results', topic=field)	
    	driver.consume(on_message, host, port, segment='raw_data', topic=field)

    return consume