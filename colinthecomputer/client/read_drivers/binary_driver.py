import struct
from PIL import Image as PImage

from colinthecomputer.protocol import Snapshot
from colinthecomputer.protocol import ColorImage
from colinthecomputer.protocol import DepthImage
from colinthecomputer.protocol import Pose
from colinthecomputer.protocol import Feelings
from colinthecomputer.protocol import User
from colinthecomputer.protocol import gender_char_to_enum
from colinthecomputer.utils import iterated_read


UINT64 = 8
UINT32 = 4
CHAR = 1
DOUBLE = 8
FLOAT = 4


def read_user(stream):
    """Read user information from stream."""
    user_id, username_len = struct.unpack('QI',
                                          stream.read(UINT64+UINT32))
    username = stream.read(username_len).decode('utf-8')
    birth_timestamp, gender = struct.unpack('Ic',
                                            stream.read(UINT32+CHAR))
    gender = gender_char_to_enum(gender.decode('utf-8'))
    user = User(user_id=user_id,
                username=username,
                birthday=birth_timestamp,
                gender=gender)
    offset = UINT64 + UINT32*2 + CHAR + username_len
    return user, offset


def read_snapshot(stream):
    """Read snapshot from stream."""
    timestamp, = struct.unpack('Q', stream.read(UINT64))
    x, y, z = struct.unpack('ddd', stream.read(DOUBLE*3))
    translation = Pose.Translation(x=x, y=y, z=z)
    x, y, z, w = struct.unpack('dddd', stream.read(DOUBLE*4))
    rotation = Pose.Rotation(x=x, y=y, z=z, w=w)
    pose = Pose(translation=translation, rotation=rotation)
    color_image, ci_offset = _read_color_image(stream)
    depth_image, di_offset = _read_depth_image(stream)
    hunger, thirst, exhaustion, happiness =\
        struct.unpack('ffff', stream.read(FLOAT*4))
    feelings = Feelings(hunger=hunger, thirst=thirst,
                        exhaustion=exhaustion, happiness=happiness)
    snapshot = Snapshot(datetime=timestamp,
                        pose=pose,
                        color_image=color_image,
                        depth_image=depth_image,
                        feelings=feelings)
    offset = UINT64 + DOUBLE*3 + DOUBLE*4 + \
        FLOAT*4 + ci_offset + di_offset
    return snapshot, offset


def _read_color_image(stream):
    """
    Read color image from stream.

    :param stream: data stream, beginning with the color image
    :type stream: bytes-like object
    :returns: size of read data
    :rtype: int
    """
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = iterated_read(stream, height*width*3)
    # Save as RGB
    data = PImage.frombytes(
        'RGB', (width, height), data, "raw", 'BGR').tobytes()
    offset = UINT32*2 + len(data)
    return ColorImage(width=width, height=height, data=data), offset


def _read_depth_image(stream):
    """
    Read depth image from stream.

    :param stream: data stream, beginning with the depth image
    :type stream: bytes-like object
    :returns: size of read data
    :rtype: int
    """
    height, width = struct.unpack('II', stream.read(UINT32*2))
    data = []
    for _ in range(height*width):
        value, = struct.unpack('f', stream.read(FLOAT))
        data.append(value)
    offset = UINT32*2 + len(data)*FLOAT
    return DepthImage(width=width, height=height, data=data), offset
