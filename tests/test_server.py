import pytest
import threading
import time

from constants import USER, SNAPSHOTS
from colinthecomputer.server import run_server
from colinthecomputer.client.__main__ import cli_upload_sample
import colinthecomputer.protocol as ptc
import colinthecomputer.client.reader as rd


class MockListener:
    class MockClient:
        def __init__(self, connection):
            self.connection = connection
            self.gets = 0

        def __enter__(self):
            return self

        def __exit__(self, exception, error, traceback):
            return

        def send_message(self, message):
            return

        def receive_message(self):
            if self.connection == 2:
                return b'kill'
            if self.gets == 0:
                self.gets += 1
                return USER.SerializeToString()
            if self.gets == 1:
                self.gets += 1
                return SNAPSHOTS[self.connection].SerializeToString()

        def close(self):
            return

    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.connections = 0

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        return

    def start(self):
        return

    def stop(self):
        return

    def accept(self):
        if self.connections < 3:
            client = MockListener.MockClient(self.connections)
            self.connections += 1
            return client
        while True:
            pass


@pytest.fixture
def mock_listener(monkeypatch):
    monkeypatch.setattr(ptc, 'Listener', MockListener)


def test_run_server(capsys, mock_listener):
    MockListener.received_messages = []
    run_server()
    stdout, stderr = capsys.readouterr()
    assert stdout == f"{(USER, SNAPSHOTS[0])!r}\n{(USER, SNAPSHOTS[1])!r}\n"
