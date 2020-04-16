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


### Patch User ###

def user_str(self):
    birth_date = dt.datetime.fromtimestamp(self.birthday)
    fbirthday = birth_date.strftime('%B %d, %Y')
    if self.gender == self.Gender.FEMALE:
        fgender = 'female'
    elif self.gender == self.Gender.MALE:
        fgender = 'male'
    else:
        fgender = 'other'
    return f'user {self.user_id}: {self.username}, ' \
           f'born {fbirthday} ({fgender})'

@classmethod
def gender_char_to_enum(cls, gender):
    if gender == 'm':
        return cls.Gender.MALE
    if gender == 'f':
        return cls.Gender.FEMALE
    return cls.Gender.OTHER

def gender_char(self):
    if self.gender == self.Gender.FEMALE:
        return 'f'
    elif self.gender == self.Gender.MALE:
        return 'm'
    else:
        return 'o'

"""User.__str__ = user_str
User.gender_char_to_enum = gender_char_to_enum"""
User.get_gender_char = gender_char


### Patch Snapshot ###

def snapshot_str(self):
    datetime = self.datetime_object()
    fdate = datetime.strftime('%B %d, %Y')
    ftime = datetime.strftime('%X.%f')
    return f'Snapshot from {fdate} at {ftime} on ' \
           f'{self.pose} ' \
           f'{self.color_image} and {self.depth_image}, ' \
           f'feelings: {self.feelings}' 

def snapshot_getitem(self, key):
    return self.__getattribute__(key)

def snapshot_datetime(self):
    return dt.datetime.fromtimestamp(self.datetime*(10**(-3)))

Snapshot.__str__ = snapshot_str
Snapshot.__getitem__ = snapshot_getitem
Snapshot.datetime_object = snapshot_datetime


### Patch Pose ###

def _to_tuple(message):
    return tuple([value for _, value in message.ListFields()])

def translation_str(self):
    return f'{_to_tuple(self)}'

@classmethod
def translation_from_tuple(cls, translation):
    x, y, z = translation
    return cls(x=x, y=y, z=z)

def rotation_str(self):
    return f'{_to_tuple(self)}'

@classmethod
def rotation_from_tuple(cls, rotation):
    x, y, z, w = rotation
    return cls(x=x, y=y, z=z, w=w)

def pose_str(self):
    return f'{self.translation} / {self.rotation}'

Pose.Translation.__str__ = translation_str
Pose.Translation.from_tuple = translation_from_tuple
Pose.Rotation.__str__ = rotation_str
Pose.Rotation.from_tuple = rotation_from_tuple
Pose.__str__ = pose_str


### Patch ColorImage ###

def color_image_str(self):
    return f'{self.width}x{self.height} color image'

ColorImage.__str__ = color_image_str


### Patch DepthImage ###

def depth_image_str(self):
    return f'{self.width}x{self.height} depth image'

DepthImage.__str__ = depth_image_str


### Patch Feelings ###

def feelings_str(self):
    return f'(hunger={self.hunger}, thirst={self.thirst}, ' \
           f'exhaustion={self.exhaustion}, happiness={self.happiness})'

@classmethod
def feelings_from_tuple(cls, feelings):
    hunger, thirst, exhaustion, happiness = feelings
    return cls(hunger=hunger, thirst=thirst,
               exhaustion=exhaustion, happiness=happiness)

Feelings.__str__ = feelings_str
Feelings.from_tuple = feelings_from_tuple


### Patch Config ###

def config_str(self):
    ffields = ', '.join(self.fields)
    return f'Supported fields: {ffields}'

def config_iter(self):
    for field in self.fields:
        yield field

def config_contains(self, field):
    return field in self.fields

Config.__str__ = config_str
Config.__iter__ = config_iter
Config.__contains__ = config_contains