from ..m import mq_drivers


drivers = {'rabbitmq': mq_drivers.rabbitmq_driver}
directory = pathlib.Path('/home/user/test/raw_data/') # TODO


def produce_consumer(mq_url):
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]

    def consumer(parser, field):
    	driver.consume(parser, host, port, segemnt='raw_data', topic=field)
    	

def parse_to_mq(parser):
	pass
