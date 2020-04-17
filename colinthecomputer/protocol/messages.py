"""Module of patched protobuf classes, used for client-server communication.
(this file simply patches basic functions as str,
making testing and interaction more conveniente.
See protocol format in colin.proto"""

import datetime as dt


from .colin_pb2 import User
from .colin_pb2 import Snapshot
from .colin_pb2 import Pose
from .colin_pb2 import ColorImage
from .colin_pb2 import DepthImage
from .colin_pb2 import Feelings
from .colin_pb2 import Config


def gender_enum_to_char(gender):
    if gender == User.Gender.FEMALE:
        return 'f'
    elif gender == User.Gender.MALE:
        return 'm'
    else:
        return 'o'


def gender_char_to_enum(gender):
    if gender == 'm':
        return User.Gender.MALE
    if gender == 'f':
        return User.Gender.FEMALE
    return User.Gender.OTHER


def snapshot_str(snapshot):
    datetime = dt.datetime.fromtimestamp(snapshot.datetime*(10**(-3)))
    fdate = datetime.strftime('%B %d, %Y')
    ftime = datetime.strftime('%X.%f')
    return f'Snapshot from {fdate} at {ftime} on ' \
           f'{snapshot.pose} ' \
           f'{snapshot.color_image.width}x{snapshot.color_image.height} color image ' \
           f'and {snapshot.depth_image.width}x{snapshot.depth_image.height} depth image ' \
           f'feelings: {snapshot.feelings}' 


def user_str(user):
    birth_date = dt.datetime.fromtimestamp(user.birthday)
    fbirthday = birth_date.strftime('%B %d, %Y')
    if user.gender == user.Gender.FEMALE:
        fgender = 'female'
    elif user.gender == user.Gender.MALE:
        fgender = 'male'
    else:
        fgender = 'other'
    return f'user {user.user_id}: {user.username}, ' \
           f'born {fbirthday} ({fgender})'
