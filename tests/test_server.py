import pytest
import time

from constants import USER, SNAPSHOTS, USER_JSON, SNAPSHOTS_JSON
import colinthecomputer.server as server
import colinthecomputer.protocol as ptc


@pytest.fixture
def blob_dir(tmp_path):
    server.server.DIRECTORY = str(tmp_path)
    return str(tmp_path)


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


def test_run_server(capsys, blob_dir, mock_listener):
    MockListener.received_messages = []
    server.run_server()
    time.sleep(1)
    stdout, stderr = capsys.readouterr()
    expected_snapshots = \
        [snapshot.replace('tmpdir', blob_dir) for snapshot in SNAPSHOTS_JSON]
    assert stdout == \
        f"{(USER_JSON, expected_snapshots[0])!r}\n" \
        f"{(USER_JSON, expected_snapshots[1])!r}\n" \
        or stdout == \
        f"{(USER_JSON, expected_snapshots[1])!r}\n" \
        f"{(USER_JSON, expected_snapshots[0])!r}\n"
