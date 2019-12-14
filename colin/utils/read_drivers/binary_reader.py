import datetime as dt
import struct
from PIL import Image as PImage

from ..messages import Snapshot
from ..messages import ColorImage
from ..messages import DepthImage
from ..messages import Pose
from ..messages import Feelings
from ..messages import User
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
    gender = User.gender_char_to_enum(gender.decode('utf-8'))
    user = User(user_id=user_id,
                username=username,
                birthday=birth_timestamp,
                gender=gender)
    offset = UINT64 + UINT32*2 + CHAR + username_len
    return user, offset


def read_snapshot(stream):
    timestamp, = struct.unpack('Q', stream.read(UINT64))
    translation = Pose.Translation.from_tuple(
        struct.unpack('ddd', stream.read(DOUBLE*3)))
    rotation = Pose.Rotation.from_tuple(
        struct.unpack('dddd', stream.read(DOUBLE*4)))
    pose = Pose(translation=translation, rotation=rotation)
    color_image, ci_offset = _read_color_image(stream)
    depth_image, di_offset = _read_depth_image(stream)
    feelings = Feelings.from_tuple(
        struct.unpack('ffff', stream.read(FLOAT*4)))
    snapshot = Snapshot(datetime=timestamp,
                        pose=pose,
                        color_image=color_image,
                        depth_image=depth_image,
                        feelings=feelings)
    offset = UINT64 + DOUBLE*3 + DOUBLE*4 + \
     FLOAT*4 + ci_offset + di_offset
    return snapshot, offset


def _read_color_image(stream):
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*3)
    # Save as RGB
    data = PImage.frombytes(
        'RGB', (width, height), data, "raw", 'BGR').tobytes()
    offset = UINT32*2 + len(data)
    return ColorImage(width=width, height=height, data=data), offset


def _read_depth_image(stream):
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*FLOAT) # TODO: this doesnt work
    offset = UINT32*2 + len(data)
    return DepthImage(width=width, height=height, data=data), offset
