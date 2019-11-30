import struct
import socket
import datetime as dt
from cli import CommandLineInterface
from .utils import Connection
from . import Thought

#cli = CommandLineInterface()

def upload_thought(address, user_id, thought):
	thought = Thought(user_id, dt.datetime.now(), thought)
	with Connection.connect(*address) as conn:
		conn.send(thought.serialize())

"""@cli.command
def upload(address, user, thought):
	try:
		address = address.split(':')
		address = (address[0], int(address[1]))
		upload_thought(address, int(user), thought)
		print('done')
	except Exception as error:
		print(f'ERROR: {error}')
		return 1


if __name__ == '__main__':
	cli.main()"""
