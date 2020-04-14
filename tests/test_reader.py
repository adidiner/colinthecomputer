import datetime as dt
import pytest

from colinthecomputer.client.reader import Reader
from constants import SAMPLE, USER, SNAPSHOTS


@pytest.fixture
def reader():
    reader = Reader(SAMPLE, 'binary')
    yield reader


def test_user_info(reader):
    assert reader.user == USER


def test_read_snapshots(reader):
    iterations = 0
    for snapshot in reader:
        assert snapshot == SNAPSHOTS[iterations]
        iterations += 1
    assert iterations == len(SNAPSHOTS)
