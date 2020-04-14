import pytest
from click.testing import CliRunner
import threading
import time

from constants import USER, CONFIG, SNAPSHOTS
from colinthecomputer.server import run_server
from colinthecomputer.client.__main__ import cli_upload_sample
import colinthecomputer.protocol as ptc
import colinthecomputer.client.reader as rd




class MockListener:
    received_messages = []
    class MockClient:
        def __init__(self, snapshot):
            self.snapshot = snapshot
            self.gets = 0

        def __enter__(self):
            return self

        def __exit__(self, exception, error, traceback):
            return

        def send_message(self, message):
            MockListener.received_messages.append(message)

        def receive_message(self):
            if self.gets == 0:
                return USER.SerializeToString()
                self.gets += 1
            if self.gets == 1:
                return SNAPSHOTS[snapshot].SerializeToString()
                self.gets += 1

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
        if self.connections < 2:
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
    stdout, stderr = capsys.readouterr()
    thread = threading.Thread(target=run_server)
    thread.start()
    time.sleep(3)
    #thread.join()
    config_message = CONFIG.SerializeToString()
    assert MockListener.received_messages == [config_message, config_message]
    assert stdout == f"({USER}, {SNAPSHOTS[0]})\n({USER}, {SNAPSHOTS[1]})"
