from furl import furl
import json

import colinthecomputer.db_drivers as drivers
from colinthecomputer.utils import printerr


class Saver:
    """
    Saver which saves results to a given database.

    :param db_url: database url,
                   in the form db://username:password@host:port/db_name
    :type db_url: str
    """
    def __init__(self, db_url):
        self.db_url = db_url
        db_url = furl(self.db_url)
        db_name, *_ = db_url.path.segments
        driver = drivers[db_url.scheme]
        driver.init_db(name=db_name,
                       host=db_url.host,
                       port=db_url.port,
                       username=db_url.username,
                       password=db_url.password)
        self.savers = driver.savers

    def __repr__(self):
        return f'Saver(db_url={self.db_url})'

    @printerr
    def save(self, topic, data):
        """
        Saves data of a given topic to the database.

        :param topic: the topic of the data
                      (supported topics:
                      user, pose, color_image, depth_image, feelings)
        :type topic: str
        :param data: the given data,
                     as cosumed from the parsed result in the mq
        :type data: json
        """
        data = json.loads(data)
        self.savers[topic](**data)
