import pytest


from constants import USER, SNAPSHOTS, USER_JSON, SNAPSHOTS_JSON
import mock_mq_driver as mq
from colinthecomputer.parsers import parsers
import json


@pytest.fixture
def worker(tmpdir):
    w = Worker(mq_url='rabbitmq://127.0.0.1:6789/')
    w.driver = mq
    return w


def test_parse_pose():
    

def test_worker(worker):
    mq.message_box = {'raw_data': ['1', '2', '3']}
    worker.work(mock_parser, 'mock')
    assert set(mq.message_box['results']) == {('mock', '1'), ('mock', '2'), ('mock', '3')}