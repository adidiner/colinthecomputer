import struct


from ...protocol import Snapshot
from ...protocol import User
from ...utils import iterated_read


UINT32 = 4


def read_user(stream):
    """Read user information from stream.
    
    :param stream: data stream, beginning with the user information
    :type stream: bytes-like object
    :returns: size of read data
    :rtype: int
    """
    size, = struct.unpack('I', stream.read(UINT32))
    user = User()
    user.ParseFromString(stream.read(size))
    return user, size + UINT32


def read_snapshot(stream):
    """Read snapshot from stream.
    
    :param stream: data stream, beginning with the snapshot
    :type stream: bytes-like object
    :returns: size of read data
    :rtype: int
    """
    size, = struct.unpack('I', stream.read(UINT32))
    snapshot = Snapshot()
    snapshot.ParseFromString(iterated_read(stream, size))
    return snapshot, size + UINT32
