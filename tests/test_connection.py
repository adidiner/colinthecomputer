import socket
import time

import pytest

from colinthecomputer.protocol import Connection


_PORT = 1234
_MESSAGE = b'\x05\x00\x00\x00hello'
_MESSAGE_LEN = 9


@pytest.fixture
def server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', _PORT))
    server.listen(1000)
    try:
        time.sleep(0.1)
        yield server
    finally:
        server.close()


def test_context_manager(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    with connection:
        assert not sock._closed
    assert sock._closed


def test_connect(server):
    with Connection.connect('127.0.0.1', _PORT) as connection:
        server.accept()


def test_send(server):
    with Connection.connect('127.0.0.1', _PORT) as connection:
        sock, _ = server.accept()
        connection.send_message(b'hello')
        assert sock.recv(_MESSAGE_LEN) == _MESSAGE


def test_receive(server):
     with Connection.connect('127.0.0.1', _PORT) as connection:
        sock, _ = server.accept()
        sock.sendall(_MESSAGE)
        assert connection.receive_message() == b'hello'