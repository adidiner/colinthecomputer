import pytest


from constants import USER, SNAPSHOTS, USER_JSON, SNAPSHOTS_JSON
import mock_mq_driver as mq
from colinthecomputer.saver.consumer import Consumer
import json


@pytest.fixture
def consumer(tmpdir):
    c = Consumer(mq_url='rabbitmq://127.0.0.1:6789/')
    c.driver = mq
    return c

class MockSaver:
    consumed = {}
    def __init__(self):
        return

    def save(self, topic, message):
        if topic not in self.consumed:
            self.consumed[topic] = set()
        print(topic, message)
        self.consumed[topic].add(message)


@pytest.fixture
def saver():
    return MockSaver()


def test_consumer(saver, consumer):
    mq.message_box = {'results': [('user', '1'), ('user', '2'),
                                  ('pose', '3'), ('feelings', '4')]}
    consumer.consume(saver.save)
    assert saver.consumed == {'user': {'1', '2'}, 'pose': {'3'}, 'feelings': {'4'}}