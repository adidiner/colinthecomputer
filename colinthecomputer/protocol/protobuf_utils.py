"""
Module of patched protobuf classes, used for client-server communication.
(this file simply patches basic functions as str,
making testing and interaction more conveniente.
See protocol format in colin.proto
"""

import datetime as dt
import json
from google.protobuf.json_format import MessageToDict, MessageToJson

from .colin_pb2 import Snapshot, User


def gender_enum_to_char(gender):
    """Convert protobuf gender to char.

    :param gender: protobuf gender
    :type gender: User.Gender
    :returns: char representing the gender
    :rtype: str
    """
    if gender == User.Gender.FEMALE:
        return 'f'
    elif gender == User.Gender.MALE:
        return 'm'
    else:
        return 'o'


def gender_char_to_enum(gender):
    """Convert gender char to protobuf gender.

    :param gender: gender char
    :type gender: char
    :returns: protobuf gender enum
    :rtype: User.Gender
    """
    if gender == 'm':
        return User.Gender.MALE
    if gender == 'f':
        return User.Gender.FEMALE
    return User.Gender.OTHER


def snapshot_str(snapshot):
    """Create slim snapshot string"""
    datetime = dt.datetime.fromtimestamp(snapshot.datetime*(10**(-3)))
    fdate = datetime.strftime('%B %d, %Y')
    ftime = datetime.strftime('%X.%f')
    nl = '\n'
    return f'Snapshot from {fdate} at {ftime}:{nl}' \
           f'pose: {MessageToJson(snapshot.pose, including_default_value_fields=True)}{nl}' \
           f'color image: {snapshot.color_image.width}x{snapshot.color_image.height} image{nl}' \
           f'depth image: {snapshot.depth_image.width}x{snapshot.depth_image.height} image{nl}' \
           f'feelings: {MessageToJson(snapshot.feelings, including_default_value_fields=True)}'


def user_str(user):
    """Create slim user string"""
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


def json_user_message(user):
    """Convert protocol-user to json.

    :param user: user object
    :type user: User
    :returns: user information json
    :rtype: json
    """
    user_dict = MessageToDict(user,
                              preserving_proto_field_name=True)
    user_dict['gender'] = gender_enum_to_char(user.gender)
    return json.dumps(user_dict)


def json_snapshot_message(snapshot, user_id, color_image_path, depth_image_path):
    """Convert protocol-snapshot to json, replacing binary data with path to data.

    :param snapshot: snapshot object
    :type snapshot: Snapshot
    :param user_id: user id corresponding the snapshot
    :type user_id: int
    :param image_path: path to BLOBS
    :type image_path: str
    :returns: snapshot information json
    :rtype: json
    """
    snapshot_metadata = Snapshot()
    snapshot_metadata.CopyFrom(snapshot)
    snapshot_metadata.color_image.ClearField('data')
    snapshot_metadata.depth_image.ClearField('data')
    snapshot_dict = MessageToDict(snapshot_metadata,
                                  preserving_proto_field_name=True,
                                  including_default_value_fields=True)
    snapshot_dict['user_id'] = user_id
    snapshot_dict['color_image']['data'] = color_image_path
    snapshot_dict['depth_image']['data'] = depth_image_path
    return json.dumps(snapshot_dict)
