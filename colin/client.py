import struct
import socket
import datetime as dt
from .utils import Connection
from . import Thought


def upload_thought(address, user_id, thought):
	thought = Thought(user_id, dt.datetime.now(), thought)
	with Connection.connect(*address) as conn:
		conn.send(thought.serialize())

