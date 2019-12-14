import time

from .utils import Connection
from .utils import Reader
from .utils.messages import User, Config, Snapshot


def upload_sample(address, sample):
    reader = Reader(sample, 'protobuf')
    for snapshot in reader:
        with Connection.connect(*address) as connection:
            send_hello(connection, reader.user)
            config = receive_config(connection)
            send_snapshot(connection, config, snapshot)
        #time.sleep(0.2)  # TODO: figure out threading problem


def send_hello(connection, hello):
    message = hello.SerializeToString()
    connection.send_message(message)


def receive_config(connection):
    message = connection.receive_message()
    config = Config()
    config.ParseFromString(message)
    return config


def send_snapshot(connection, config, snapshot):
    fields = {field: snapshot[field] for field in config}
    snapshot = Snapshot(datetime=snapshot.datetime, **fields)
    message = snapshot.SerializeToString()
    connection.send_message(message)
