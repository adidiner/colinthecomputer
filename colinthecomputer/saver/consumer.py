from furl import furl
import colinthecomputer.mq_drivers as drivers


def produce_consumer(mq_url):
	"""Produce a consume function for the saver,
    handling the communication with the given message queue
    
    :param mq_url: a url describing the mq, in the form 'mq://host:port'
    :type mq_url: str
    :returns: a consume function
    :rtype: function
    """
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]

    def consume(saver, topics=None):
    	"""Consume messages from the message queue,
    	use the saver to save them to the database.
    	
    	:param saver: saver function which recieves topic and data
    	:type saver: function
    	:param topics: topics to be consumed and saved,
    	defaults to user, pose, color_image, depth_image and feelings
    	:type topics: list[str]
    	"""
    	if not topics:
    		topics = ['user', 'pose', 'color_image', 'depth_image', 'feelings']
    	def on_message(topic, message):
    		saver.save(topic, message)
    	driver.topic_consume(on_message, host, port,
    				   topics=topics,
    				   segment='results')

    return consume