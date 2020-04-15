import pytest
from click.testing import CliRunner
import threading
import time

from constants import USER, SNAPSHOTS, USER_JSON, SNAPSHOTS_JSON
import mock_mq_driver as mq
from colinthecomputer.server.publisher import Publisher
import json


@pytest.fixture
def publisher(tmpdir):
    p = Publisher(mq_url='rabbitmq://127.0.0.1:6789/', directory=tmpdir)
    p.driver = mq
    return p


def test_publisher(publisher):
    mq.message_box = {}
    for snapshot in SNAPSHOTS:
        publisher.publish((USER, snapshot))
    expected_snapshots = [snapshot.replace('tmpdir', str(publisher.directory)) for snapshot in SNAPSHOTS_JSON]
    assert set(mq.message_box['results']) == {('user', USER_JSON), ('user', USER_JSON)}
    assert set(mq.message_box['raw_data']) == set(expected_snapshots)