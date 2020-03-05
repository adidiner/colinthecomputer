from furl import furl
import json

from colinthecomputer.db_drivers import postgresql_driver

drivers = {'postgresql': postgresql_driver}

class Saver:
    def __init__(self, db_url):
        db_url = furl(db_url)
        db, host, port = db_url.scheme, db_url.host, db_url.port
        self.driver = drivers[db]
        self.savers = self.driver.savers

    def __repr__(self):
        return f'Saver(db_url={self.db_url})'

    def save(self, topic, data):
        data = json.loads(data)
        # Save user information
        if topic == 'user':
            self.savers[topic](**data)
            return
        # Save parser results
        unpack = lambda user_id, datetime, data: (user_id, datetime, data)
        user_id, datetime, data = unpack(**data)
        self.savers[topic](user_id, datetime, **data)
