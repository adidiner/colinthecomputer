import socket
import time

import pytest

from colin.utils import Listener


_PORT = 1234
_HOST = '127.0.0.1'
_BACKLOG = 5000
_REUSEADDR = True


@pytest.fixture
def listener():
    return Listener(_PORT, host=_HOST, backlog=_BACKLOG, reuseaddr=_REUSEADDR)


def test_context_manager(listener):
    assert socket.socket().connect_ex((_HOST, _PORT)) != 0
    with listener:
        time.sleep(0.1)
        assert socket.socket().connect_ex((_HOST, _PORT)) == 0
    assert socket.socket().connect_ex((_HOST, _PORT)) != 0
