import struct


from colinthecomputer.protocol import Snapshot
from colinthecomputer.protocol import User
from colinthecomputer.utils import iterated_read


UINT32 = 4


def read_user(stream):
    """Read user information from stream."""
    size, = struct.unpack('I', stream.read(UINT32))
    user = User()
    user.ParseFromString(stream.read(size))
    return user, size + UINT32


def read_snapshot(stream):
    """Read snapshot from stream."""
    size, = struct.unpack('I', stream.read(UINT32))
    snapshot = Snapshot()
    snapshot.ParseFromString(iterated_read(stream, size))
    return snapshot, size + UINT32
