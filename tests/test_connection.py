import socket
import time

import pytest

from colin.utils import Connection


_PORT = 1234


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
    with  Connection.connect('127.0.0.1', _PORT) as connection:
        server.accept()
