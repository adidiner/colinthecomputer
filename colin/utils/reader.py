import datetime as dt
import struct
from PIL import Image as PImage

from .snapshot import Snapshot
from .snapshot import Image


UINT64 = 8
UINT32 = 4
CHAR = 1
DOUBLE = 8
FLOAT = 4
CHUNK = 1000000


class Reader:
    def __init__(self, path):
        self.path = path
        self.offset = 0
        with open(path, 'rb') as f:
            # Unpack user_id and username
            self.user_id = struct.unpack('Q', f.read(UINT64))
            username_len = struct.unpack('I', f.read(UINT32))
            self.username = f.read(username_len).decode('utf-8')
            # Unpack birthdate
            birth_timestamp = struct.unpack('I', f.read(UINT32))
            self.birth_date = dt.datetime.fromtimestamp(birth_timestamp)
            # Unpack gender
            gender = struct.unpack('c', f.read(CHAR))
            self.gender = gender.decode('utf-8')
            # Read offset bytes from file
            self.offset += UINT64 + UINT32 + username_len + UINT32 + CHAR

    def __iter__(self):
        with open(self.path, 'rb') as f:
            f.seek(self.offset)
            while f.read(1) != '':
                f.seek(-1, 1)
                yield read_snapshot(f)


def read_snapshot(stream):
    timestamp, = struct.unpack('Q', stream.read(UINT64))
    timestamp *= 10**(-3)
    snapshot = Snapshot(dt.datetime.fromtimestamp(timestamp))
    snapshot.translation = struct.unpack('ddd', stream.read(DOUBLE*3))
    snapshot.rotation = struct.unpack('dddd', stream.read(DOUBLE*4))
    snapshot.color_image = read_color_image(stream)
    snapshot.depth_image = read_depth_image(stream)
    snapshot.feelings = struct.unpack('ffff', stream.read(FLOAT*4))
    return snapshot


def read_color_image(stream):
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*3)
    # Save as RGB
    data = PImage.frombytes(
        'RGB', (width, height), data, "raw", 'BGR').tobytes()
    return Image('color', width=width, height=height, data=data)


def read_depth_image(stream):
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*FLOAT)
    return Image('depth', width=width, height=height, data=data)


def iterated_read(stream, size):
    read, data = 0, b''
    while read + CHUNK < size:
        data += stream.read(CHUNK)
        read += CHUNK
    data += stream.read(size-read)
    return data
