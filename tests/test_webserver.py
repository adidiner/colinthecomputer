'''import datetime as dt
import multiprocessing
import pathlib
import shutil

import pytest
import requests

from colin import run_webserver


_WEBSERVER_ADDRESS = '127.0.0.1', 8000
_WEBSERVER_URL = 'http://localhost:8000'
_ROOT_DIR = pathlib.Path(__file__).absolute().parent.parent
#_WEBSERVER_PATH = _ROOT_DIR / 'web.py'
_DATA_DIR = _ROOT_DIR / 'data'


@pytest.fixture
def webserver():
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_webserver, args=(child,))
    process.start()
    parent.recv()
    try:
        yield
    finally:
        process.terminate()
        process.join()


def test_index(webserver):
    response = requests.get(_WEBSERVER_URL)
    for user_dir in _DATA_DIR.iterdir():
        assert f'user {user_dir.name}' in response.text
        assert f'users/{user_dir.name}' in response.text


def test_user(webserver):
    for user_dir in _DATA_DIR.iterdir():
        response = requests.get(f'{_WEBSERVER_URL}/users/{user_dir.name}')
        for thought_file in user_dir.iterdir():
            datetime = dt.datetime.strptime(thought_file.stem, '%Y-%m-%d_%H-%M-%S')
            assert f'User {user_dir.name}' in response.text
            assert f'{datetime:%Y-%m-%d %H:%M:%S}' in response.text
            thought_file.read_text() in response.text


def test_dynamic(webserver):
    user_id = 0
    user_dir = _DATA_DIR / str(user_id)
    user_dir.mkdir()
    try:
        datetime = dt.datetime(2000, 1, 1, 12, 0, 0)
        thought = 'Hello, world!'
        thought_file = user_dir / f'{datetime:%Y-%m-%d_%H-%M-%S}.txt'
        thought_file.write_text(thought)
        response = requests.get(_WEBSERVER_URL)
        assert f'user {user_dir.name}' in response.text
        assert f'users/{user_dir.name}' in response.text
        response = requests.get(f'{_WEBSERVER_URL}/users/{user_id}')
        assert f'User {user_dir.name}' in response.text
        assert f'{datetime:%Y-%m-%d %H:%M:%S}' in response.text
        assert thought_file.read_text() in response.text
    finally:
        shutil.rmtree(user_dir)


def _run_webserver(pipe):
    pipe.send('ready')
    run_webserver(_WEBSERVER_ADDRESS, _DATA_DIR)'''