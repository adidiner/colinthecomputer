import colinthecomputer.protocol as ptc
import colinthecomputer.client.reader as rd
from colinthecomputer.utils import printerr


@printerr
def upload_sample(path, host='127.0.0.1', port=8000, file_format='protobuf'):
    """
    Uploads sample from given path to the server.

    :param path: path to the sample file
    :type path: str
    :param host: server host address, defaults to 127.0.0.1
    :type host: str, optional
    :param port: server port address, defaults to 8000
    :type port: str, optional
    :param file_format: the sample file format,
                        supported formats are binary and protobuf.
                        defaults to protobuf
    :type file_format: str, optional
    """
    reader = rd.Reader(path, file_format)
    for snapshot in reader:
        with ptc.Connection.connect(host, port) as connection:
            send_hello(connection, reader.user)
            send_snapshot(connection, snapshot)


def send_hello(connection, hello):
    """Sends hello message to a server."""
    message = hello.SerializeToString()
    connection.send_message(message)


def send_snapshot(connection, snapshot):
    """Sends snapshot message to a server."""
    message = snapshot.SerializeToString()
    connection.send_message(message)
