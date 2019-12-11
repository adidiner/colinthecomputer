import datetime as dt
import time

from .utils import Connection
from .utils import Reader
from .protocol import Hello, Config, Snapshot


def upload_sample(address, sample):
    reader = Reader(sample)
    hello = Hello(reader.user_id, reader.username,
                  reader.birth_date, reader.gender)
    for snapshot in reader:
        with Connection.connect(*address) as connection:
            send_hello(connection, hello)
            config = receive_config(connection)
            send_snapshot(connection, config, snapshot)
        time.sleep(0.2) #TODO: figure out threading problem


def send_hello(connection, hello):
    message = hello.serialize()
    connection.send_message(message)


def receive_config(connection):
    message = connection.receive_message()
    return Config.deserialize(message)


def send_snapshot(connection, config, snapshot):
    fields = {field: snapshot[field] for field in config}
    message = Snapshot(snapshot.timestamp, **fields).serialize()
    connection.send_message(message)
