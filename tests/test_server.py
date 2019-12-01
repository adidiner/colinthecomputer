import datetime as dt
import io
import multiprocessing
import pathlib
import signal
import socket
import struct
import subprocess
import sys
import threading
import time

import pytest

from colin import run_server


_SERVER_ADDRESS = '127.0.0.1', 5000
#_SERVER_PATH = pathlib.Path(__file__).absolute().parent.parent / 'server.py'

_HEADER_FORMAT = 'LLI'

_USER_1 = 1
_USER_2 = 2
_TIMESTAMP_1 = int(dt.datetime(2019, 10, 25, 15, 12, 5, 228000).timestamp())
_TIMESTAMP_2 = int(dt.datetime(2019, 10, 25, 15, 15, 2, 304000).timestamp())
_THOUGHT_1 = "I'm hungry"
_THOUGHT_2 = "I'm sleepy"


@pytest.fixture
def data_dir(tmp_path):
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server, args=(child, tmp_path))
    process.start()
    parent.recv()
    try:
        yield tmp_path
    finally:
        process.terminate()
        process.join()


def test_user_id(data_dir):
    _upload_thought(_USER_1, _TIMESTAMP_1, _THOUGHT_1)
    user_dir = data_dir / str(_USER_1)
    assert user_dir.exists()
    assert user_dir.is_dir()
    _upload_thought(_USER_2, _TIMESTAMP_1, _THOUGHT_1)
    user_dir = data_dir / str(_USER_2)
    assert user_dir.exists()
    assert user_dir.is_dir()


def test_timestamp(data_dir):
    thought_path = _get_path(data_dir, _USER_1, _TIMESTAMP_1)
    assert not thought_path.exists()
    _upload_thought(_USER_1, _TIMESTAMP_1, _THOUGHT_1)
    assert thought_path.exists()
    thought_path = _get_path(data_dir, _USER_1, _TIMESTAMP_2)
    assert not thought_path.exists()
    _upload_thought(_USER_1, _TIMESTAMP_2, _THOUGHT_1)
    assert thought_path.exists()


def test_thought(data_dir):
    _upload_thought(_USER_1, _TIMESTAMP_1, _THOUGHT_1)
    thought_path = _get_path(data_dir, _USER_1, _TIMESTAMP_1)
    assert thought_path.read_text() == _THOUGHT_1
    _upload_thought(_USER_2, _TIMESTAMP_2, _THOUGHT_2)
    thought_path = _get_path(data_dir, _USER_2, _TIMESTAMP_2)
    assert thought_path.read_text() == _THOUGHT_2


def test_partial_data(data_dir):
    message = _serialize_thought(_USER_1, _TIMESTAMP_1, _THOUGHT_1)
    with socket.socket() as connection:
        time.sleep(0.1) # Wait for server to start listening.
        connection.connect(_SERVER_ADDRESS)
        for c in message:
            connection.sendall(bytes([c]))
            time.sleep(0.01)
    thought_path = _get_path(data_dir, _USER_1, _TIMESTAMP_1)
    assert thought_path.read_text() == _THOUGHT_1


def test_race_condition(data_dir):
    timestamp = _TIMESTAMP_1
    for _ in range(10):
        timestamp += 1
        _upload_thought(_USER_1, timestamp, _THOUGHT_1)
        _upload_thought(_USER_1, timestamp, _THOUGHT_2)
        thought_path = _get_path(data_dir, _USER_1, timestamp)
        thoughts = set(thought_path.read_text().splitlines())
        assert thoughts == {_THOUGHT_1, _THOUGHT_2}


"""def test_cli(tmp_path):
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', _SERVER_PATH, f'{host}:{port}', str(tmp_path)],
        stdout = subprocess.PIPE,
    )
    def run_server():
        process.communicate()
    thread = threading.Thread(target=run_server)
    thread.start()
    time.sleep(0.1)
    _upload_thought(_USER_1, _TIMESTAMP_1, _THOUGHT_1)
    _upload_thought(_USER_2, _TIMESTAMP_2, _THOUGHT_2)
    process.send_signal(signal.SIGINT)
    thread.join()
    thought_path_1 = _get_path(tmp_path, _USER_1, _TIMESTAMP_1)
    thought_path_2 = _get_path(tmp_path, _USER_2, _TIMESTAMP_2)
    assert thought_path_1.read_text() == _THOUGHT_1
    assert thought_path_2.read_text() == _THOUGHT_2"""


def _run_server(pipe, data_dir):
    pipe.send('read')
    run_server(_SERVER_ADDRESS, data_dir)


def _upload_thought(user_id, timestamp, thought):
    message = _serialize_thought(user_id, timestamp, thought)
    with socket.socket() as connection:
        time.sleep(0.1) # Wait for server to start listening.
        connection.settimeout(2)
        time.sleep(0.2)
        connection.connect(_SERVER_ADDRESS)
        connection.sendall(message)
    time.sleep(0.2) # Wait for server to write thought.


def _serialize_thought(user_id, timestamp, thought):
    header = struct.pack(_HEADER_FORMAT, user_id, timestamp, len(thought))
    return header + thought.encode()


def _get_path(data_dir, user_id, timestamp):
    datetime = dt.datetime.fromtimestamp(timestamp)
    return data_dir / f'{user_id}/{datetime:%Y-%m-%d_%H-%M-%S}.txt'
