import struct


from ...protocol import Snapshot
from ...protocol import User
from ...utils import iterated_read


UINT32 = 4


def read_user(stream):
	size, = struct.unpack('I', stream.read(UINT32))
	user = User()
	user.ParseFromString(stream.read(size))
	return user, size + UINT32


def read_snapshot(stream):
	size, = struct.unpack('I', stream.read(UINT32))
	snapshot = Snapshot()
	snapshot.ParseFromString(iterated_read(stream, size))
	return snapshot, size + UINT32
