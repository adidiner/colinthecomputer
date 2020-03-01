import time

from ..protocol import Connection
from .reader import Reader
from ..protocol import User, Config, Snapshot


def upload_sample(path, host='127.0.0.1', port=8000):
    reader = Reader(path, 'protobuf') # TODO: make this configurable
    for snapshot in reader:
        with Connection.connect(host, port) as connection:
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
