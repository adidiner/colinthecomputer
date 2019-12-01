import datetime as dt
import multiprocessing
import pathlib
import subprocess
import os
import socket
import struct
import time

import pytest

from colin import upload_thought


_SERVER_ADDRESS = '127.0.0.1', 5000
_SERVER_BACKLOG = 1000
#_CLIENT_PATH = pathlib.Path(__file__).absolute().parent.parent / 'client.py'

_HEADER_FORMAT = 'LLI'
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)

_USER_1 = 1
_USER_2 = 2
_THOUGHT_1 = "I'm hungry"
_THOUGHT_2 = "I'm sleepy"


@pytest.fixture
def get_message():
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server, args=(child,))
    process.start()
    parent.recv()
    try:
        def get_message():
            if not parent.poll(1):
                raise TimeoutError()
            return parent.recv()
        yield get_message
    finally:
        process.terminate()
        process.join()


def test_connection(get_message):
    upload_thought(_SERVER_ADDRESS, _USER_1, _THOUGHT_1)
    message = get_message()
    assert message


def test_user_id(get_message):
    upload_thought(_SERVER_ADDRESS, _USER_1, _THOUGHT_1)
    user_id, timestamp, thought = get_message()
    assert user_id == _USER_1
    upload_thought(_SERVER_ADDRESS, _USER_2, _THOUGHT_1)
    user_id, timestamp, thought = get_message()
    assert user_id == _USER_2


def test_thought(get_message):
    upload_thought(_SERVER_ADDRESS, _USER_1, _THOUGHT_1)
    user_id, timestamp, thought = get_message()
    assert thought == _THOUGHT_1
    upload_thought(_SERVER_ADDRESS, _USER_1, _THOUGHT_2)
    user_id, timestamp, thought = get_message()
    assert thought == _THOUGHT_2


def test_timestamp(get_message):
    upload_thought(_SERVER_ADDRESS, _USER_1, _THOUGHT_1)
    user_id, timestamp, thought = get_message()
    _assert_now(timestamp)
    upload_thought(_SERVER_ADDRESS, _USER_2, _THOUGHT_2)
    user_id, timestamp, thought = get_message()
    _assert_now(timestamp)


"""def test_cli(get_message):
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', _CLIENT_PATH, f'{host}:{port}', str(_USER_1), _THOUGHT_1],
        stdout = subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert b'done' in stdout.lower()
    user_id, timestamp, thought = get_message()
    assert user_id == _USER_1
    _assert_now(timestamp)
    assert thought == _THOUGHT_1"""


"""def test_cli_error():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', _CLIENT_PATH, f'{host}:{port}', str(_USER_1), _THOUGHT_1],
        stdout = subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert b'error' in stdout.lower()"""


def _run_server(pipe):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(_SERVER_ADDRESS)
    server.listen(_SERVER_BACKLOG)
    pipe.send('ready')
    with server:
        while True:
            connection, address = server.accept()
            _handle_connection(connection, pipe)


def _handle_connection(connection, pipe):
    with connection:
        header_data = _receive_all(connection, _HEADER_SIZE)
        user_id, timestamp, size = struct.unpack(_HEADER_FORMAT, header_data)
        data = _receive_all(connection, size)
        thought = data.decode()
        pipe.send([user_id, timestamp, thought])


def _receive_all(connection, size):
    chunks = []
    while size > 0:
        chunk = connection.recv(size)
        if not chunk:
            raise RuntimeError('incomplete data')
        chunks.append(chunk)
        size -= len(chunk)
    return b''.join(chunks)


def _assert_now(timestamp):
    now = int(time.time())
    assert abs(now - timestamp) < 5
