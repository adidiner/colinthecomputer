import colinthecomputer.protocol as ptc
from colinthecomputer.utils import make_path
import colinthecomputer.mq_drivers as drivers

import pathlib
from furl import furl


class Publisher:
    """Publisher which publishes messages to a given message queue.
    
    :param mq_url: a url describing the mq, in the form 'mq://host:port'
    :type mq_url: str
    """
    def __init__(self, mq_url):
        mq_url = furl(mq_url)
        mq, self.host, self.port, self.mq_url = mq_url.scheme, mq_url.host, mq_url.port, mq_url
        self.driver = drivers[mq]

    def __repr__(self):
        return f'Publisher(mq_url={self.mq_url}, blob_dir={self.directory})'

    def publish(self, message):
        """Publish message to the message queue.
        
        :param message: message to be published, 
                        consisting of a result (parsed) message and a raw_data message.
        :type message: json, json
        """
        result, raw_data = message
        self.driver.share_publish(result,
                                  self.host,
                                  self.port,
                                  topic='user',
                                  segment='results')

        self.driver.task_publish(raw_data,
                                 self.host, 
                                 self.port, 
                                 segment='raw_data')

