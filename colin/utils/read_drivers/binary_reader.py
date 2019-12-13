import datetime as dt
import struct
from PIL import Image as PImage

from ..snapshot import Snapshot
from ..snapshot import Image
from ..user import User
from ..util_methods import iterated_read


UINT64 = 8
UINT32 = 4
CHAR = 1
DOUBLE = 8
FLOAT = 4


def read_user(stream):
    user_id, username_len = struct.unpack('QI',
                                          stream.read(UINT64+UINT32))
    username = stream.read(username_len).decode('utf-8')
    birth_timestamp, gender = struct.unpack('Ic',
                                            stream.read(UINT32+CHAR))
    gender = gender.decode('utf-8')
    user = User(user_id, username, birth_timestamp, gender)
    return user, len(user)


def read_snapshot(stream):
    timestamp, = struct.unpack('Q', stream.read(UINT64))
    translation = struct.unpack('ddd', stream.read(DOUBLE*3))
    rotation = struct.unpack('dddd', stream.read(DOUBLE*4))
    color_image = _read_color_image(stream)
    depth_image = _read_depth_image(stream)
    feelings = struct.unpack('ffff', stream.read(FLOAT*4))
    snapshot = Snapshot(timestamp, translation, rotation,
                    color_image, depth_image, feelings)
    return snapshot, len(snapshot)


def _read_color_image(stream):
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*3)
    # Save as RGB
    data = PImage.frombytes(
        'RGB', (width, height), data, "raw", 'BGR').tobytes()
    return Image(im_type='color', width=width, height=height, data=data)


def _read_depth_image(stream):
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*FLOAT)
    return Image(im_type='depth', width=width, height=height, data=data)
