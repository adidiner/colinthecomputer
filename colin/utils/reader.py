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
        self._offset = 0
        with open(path, 'rb') as f:
            # Unpack user_id, username
            self.user_id, username_len = struct.unpack('QI',
                                                       f.read(UINT64+UINT32))
            self.username = f.read(username_len).decode('utf-8')
            # Unpack birthdate , gender
            birth_timestamp, gender = struct.unpack('Ic',
                                                    f.read(UINT32+CHAR))
            self.birth_date = dt.datetime.fromtimestamp(birth_timestamp)
            self.gender = gender.decode('utf-8')
            # Reader read offset bytes from file
            self._offset += UINT64 + UINT32 + username_len + UINT32 + CHAR

    def __repr__(self):
        return f'Reader(path={self.path})'

    def __str__(self):
        fbirth_date = self.birth_date.strftime('%B %d, %Y')
        if self.gender == 'f':
            fgender = 'female'
        elif self.gender == 'm':
            fgender = 'male'
        else:
            fgender = 'other'
        return f'user {self.user_id}: {self.username}, ' \
               f'born {fbirth_date} ({fgender})'

    def __iter__(self):
        with open(self.path, 'rb') as f:
            f.seek(self._offset)
            while len(f.read(4)) == 4:
                f.seek(-4, 1)
                yield read_snapshot(f)


def read_snapshot(stream):
    timestamp, = struct.unpack('Q', stream.read(UINT64))
    translation = struct.unpack('ddd', stream.read(DOUBLE*3))
    rotation = struct.unpack('dddd', stream.read(DOUBLE*4))
    color_image = read_color_image(stream)
    depth_image = read_depth_image(stream)
    feelings = struct.unpack('ffff', stream.read(FLOAT*4))
    return Snapshot(timestamp, translation, rotation,
                    color_image, depth_image, feelings)


def read_color_image(stream):
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*3)
    # Save as RGB
    data = PImage.frombytes(
        'RGB', (width, height), data, "raw", 'BGR').tobytes()
    return Image(im_type='color', width=width, height=height, data=data)


def read_depth_image(stream):
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*FLOAT)
    return Image(im_type='depth', width=width, height=height, data=data)


def iterated_read(stream, size):
    read, data = 0, b''
    while read + CHUNK < size:
        data += stream.read(CHUNK)
        read += CHUNK
    data += stream.read(size-read)
    return data


def read(path):
    reader = Reader(path)
    print(reader)
    for snapshot in reader:
        print(snapshot)
