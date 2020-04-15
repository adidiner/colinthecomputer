import pika
from multiprocessing import Process
import time

import colinthecomputer.mq_drivers as drivers
driver = drivers['rabbitmq']
# TODO: dont hard code host and port
_HOST = '127.0.0.1'
_PORT = 6789

def worker(path, number):
	def write_result(topic, body):
		with open(path, 'at') as f:
			f.write(f'{str(body)}\n')

	driver.task_consume(write_result, _HOST, _PORT, number, "task_testing")

def test_task_queue(tmp_path):
	consumed = tmp_path / 'consumed.txt'
	driver.task_publish('1', _HOST, _PORT, segment="task_testing")
	print("a")
	p = Process(target=worker, args=(consumed, '1'))
	p.start()
	time.sleep(2)
	p.terminate()
	driver.task_publish('2', _HOST, _PORT, segment="task_testing")
	driver.task_publish('3', _HOST, _PORT, segment="task_testing")
	p1 = Process(target=worker, args=(consumed, '2'))
	p2 = Process(target=worker, args=(consumed, '2'))
	p1.start()
	p2.start()
	time.sleep(2)
	p1.terminate()
	p2.terminate()
	with open(consumed, 'rt') as f:
		results = f.readlines()
	assert set(results) == {'1\n', '2\n', '3\n'}
