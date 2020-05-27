import pytest

from constants import USER_JSON, SNAPSHOTS_JSON
import mock_mq_driver as mq
from colinthecomputer.server.publisher import Publisher


@pytest.fixture
def publisher():
    p = Publisher(mq_url='rabbitmq://127.0.0.1:6789/')
    p.driver = mq
    return p


def test_publisher(publisher):
    mq.message_box = {}
    for snapshot in SNAPSHOTS_JSON:
        publisher.publish((USER_JSON, snapshot))
    assert set(mq.message_box['results']) == \
        {('user', USER_JSON), ('user', USER_JSON)}
    assert set(mq.message_box['raw_data']) == set(SNAPSHOTS_JSON)
