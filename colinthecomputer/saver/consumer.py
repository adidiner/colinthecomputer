from furl import furl
import colinthecomputer.mq_drivers as drivers

class Consumer:
    """Consumer which handles consuming from the message queue,
    feeding the results to a saver.
    
    :param mq_url: a url describing the mq, in the form 'mq://host:port'
    :type mq_url: str
    """
    def __init__(self, mq_url):
        mq_url = furl(mq_url)
        mq, self.host, self.port, self.mq_url = mq_url.scheme, mq_url.host, mq_url.port, mq_url
        self.driver = drivers[mq]

    def __repr__(self):
        return f'Consumer(mq_url={mq_url})'

    def consume(self, saver, topics=None):
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
        self.driver.share_consume(on_message, 
                                  self.host,
                                  self.port,
                                  topics=topics,
                                  segment='results')

