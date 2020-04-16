import pytest
from click.testing import CliRunner

from constants import USER, SNAPSHOTS
from colinthecomputer.client import upload_sample
from colinthecomputer.client.__main__ import cli_upload_sample
import colinthecomputer.protocol as ptc
import colinthecomputer.client.reader as rd

class MockConnection:
    received_messages = []

    def __init__(self, socket):
        return

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        return

    @classmethod
    def connect(cls, host, port):
        return MockConnection(None)

    def send_message(self, message):
        MockConnection.received_messages.append(message)

    def receive_message(self):
        return

    def close(self):
        return


class MockReader:
    def __init__(self, path, file_format):
        self.path = path
        self.user = USER
        self.snapshots = SNAPSHOTS

    def __iter__(self):
        for snapshot in self.snapshots:
            yield snapshot


@pytest.fixture
def mock_connection(monkeypatch):
    monkeypatch.setattr(ptc, 'Connection', MockConnection)


@pytest.fixture
def mock_reader(monkeypatch):
    monkeypatch.setattr(rd, 'Reader', MockReader)


def test_upload_sample(mock_connection, mock_reader):
    MockConnection.received_messages = []
    upload_sample('path')
    user_message = USER.SerializeToString()
    snpashot_messages = [snapshot.SerializeToString() for snapshot in SNAPSHOTS]
    assert MockConnection.received_messages == [user_message, 
                                                snpashot_messages[0], 
                                                user_message, 
                                                snpashot_messages[1]]

def test_cli_upload_sample(mock_connection, mock_reader):
    MockConnection.received_messages = []
    runner = CliRunner()
    result = runner.invoke(cli_upload_sample, 'path')
    user_message = USER.SerializeToString()
    snpashot_messages = [snapshot.SerializeToString() for snapshot in SNAPSHOTS]
    assert result.exit_code == 0
    assert MockConnection.received_messages == [user_message, 
                                                snpashot_messages[0], 
                                                user_message, 
                                                snpashot_messages[1]]
