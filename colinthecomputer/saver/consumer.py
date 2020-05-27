from furl import furl

import colinthecomputer.mq_drivers as drivers


class Consumer:
    """
    Consumer which handles consuming from the message queue,
    feeding the results to a saver.

    :param mq_url: a url describing the mq, in the form 'mq://host:port'
    :type mq_url: str
    """
    def __init__(self, mq_url):
        mq_url = furl(mq_url)
        mq, self.host, self.port, self.mq_url =\
            mq_url.scheme, mq_url.host, mq_url.port, mq_url
        self.driver = drivers[mq]

    def __repr__(self):
        return f'Consumer(mq_url={self.mq_url})'

    def consume(self, on_message, topics=None):
        """
        Consume messages from the message queue,
        performe on_message for every consumed message.

        :param on_message: function to perform, recieves topic and data
        :type saver: function
        :param topics: topics to be consumed and saved,
                       defaults to user, pose,
                       color_image, depth_image and feelings
        :type topics: list[str]
        """
        if not topics:
            topics = ['user',
                      'pose',
                      'color_image',
                      'depth_image',
                      'feelings']
        self.driver.share_consume(on_message,
                                  self.host,
                                  self.port,
                                  topics=topics,
                                  segment='results')
