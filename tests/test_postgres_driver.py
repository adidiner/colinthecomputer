import pika
from multiprocessing import Process
import time

import colinthecomputer.db_drivers as drivers
driver = drivers['postgresql']
# TODO: dont hard code host and port
_HOST = '127.0.0.1'
_PORT = 3333
_USERNAME = 'test'
_DB_NAME = 'test'
_PASSWORD = 'password'

# sudo docker run -d -e POSTGRES_PASSWORD=password -e POSTGRES_USER=test -p  3333:5432 postgres
# db://username:password@host:port/db_name
# postgresql://colin:password@127.0.0.1:3469/colin

@pytest.fixture
def init():
    init_db(name=_DB_NAME, host=_HOST, port=_PORT,
            user=_USERNAME, password=_PASSWORD)

