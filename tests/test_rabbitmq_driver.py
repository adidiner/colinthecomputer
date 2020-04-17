import pika
from multiprocessing import Process
import time

import colinthecomputer.mq_drivers as drivers
driver = drivers['rabbitmq']
# TODO: dont hard code host and port
_HOST = '127.0.0.1'
_PORT = 2222


def worker(path, number):
    def write_task(topic, body):
        with open(path, 'at') as f:
            f.write(f"{body.decode('utf-8')}\n")

    driver.task_consume(write_task, _HOST, _PORT, topic=number, segment="task_testing")


def consumer(path, topics):
    def write_shared(topic, body):
        print(f"{topic}:{body.decode('utf-8')}\n")
        with open(path, 'at') as f:
            f.write(f"{topic}:{body.decode('utf-8')}\n")
    print("calling shred consume")
    driver.share_consume(write_shared, _HOST, _PORT, topics=topics, segment="shared_testing")


def test_task_queue(tmp_path):
    consumed = tmp_path / 'tasks.txt'
    p = Process(target=worker, args=(consumed, '1'))
    p.start()
    time.sleep(1)
    driver.task_publish('1', _HOST, _PORT, segment="task_testing")
    time.sleep(1)
    p.terminate()
    p1 = Process(target=worker, args=(consumed, '2'))
    p2 = Process(target=worker, args=(consumed, '2'))
    p1.start()
    p2.start()
    time.sleep(1)
    driver.task_publish('2', _HOST, _PORT, segment="task_testing")
    driver.task_publish('3', _HOST, _PORT, segment="task_testing")
    time.sleep(1)
    p1.terminate()
    p2.terminate()
    with open(consumed, 'rt') as f:
        results = f.readlines()
    assert set(results) == {'1\n', '2\n', '3\n'}


def test_share_queue(tmp_path):
    consumed = tmp_path / 'shared.txt'
    p = Process(target=consumer, args=(consumed, ['1']))
    p.start()
    time.sleep(1)
    driver.share_publish('1', _HOST, _PORT, segment="shared_testing", topic='1')
    time.sleep(1)
    p.terminate()
    p1 = Process(target=consumer, args=(consumed, ['2']))
    p2 = Process(target=consumer, args=(consumed, ['1', '2']))
    p1.start()
    p2.start()
    time.sleep(1)
    driver.share_publish('2', _HOST, _PORT, segment="shared_testing", topic='2')
    driver.share_publish('3', _HOST, _PORT, segment="shared_testing", topic='2')
    time.sleep(1)
    p1.terminate()
    p2.terminate()
    with open(consumed, 'rt') as f:
        results = f.readlines()
    assert set(results) == {'1:1\n', '1:1\n',
                            '2:2\n', '2:2\n',
                            '2:3\n', '2:3\n'}