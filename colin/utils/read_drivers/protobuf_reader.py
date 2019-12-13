import struct


from ..snapshot import Snapshot
from ..snapshot import Image
from ..user import User
from ..util_methods import iterated_read
from .colin_pb2 import User as ProtoUser
from .colin_pb2 import Snapshot as ProtoSnapshot


UINT32 = 4


def read_user(stream):
	size, = struct.unpack('I', stream.read(UINT32))
	puser = ProtoUser()
	puser.ParseFromString(stream.read(size))
	if puser.gender == ProtoUser.Gender.FEMALE:
		gender = 'f'
	elif puser.gender == ProtoUser.Gender.MALE:
		gender = 'm'
	else:
		gender = 'o'
	user = User(puser.user_id, puser.username, puser.birthday, gender)
	return user, size + UINT32


def read_snapshot(stream):
	size, = struct.unpack('I', stream.read(UINT32))
	psnapshot = ProtoSnapshot()
	psnapshot.ParseFromString(iterated_read(stream, size))
	timestamp = psnapshot.datetime
	translation = _to_tuple(psnapshot.pose.translation)
	rotation = _to_tuple(psnapshot.pose.rotation)
	color_image = Image(im_type='color',
						width=psnapshot.color_image.width,
						height=psnapshot.color_image.height,
						data=psnapshot.color_image.data)
	depth_image = Image(im_type='depth',
						width=psnapshot.color_image.width,
						height=psnapshot.color_image.height,
						data=psnapshot.color_image.data)
	feelings = _to_tuple(psnapshot.feelings)
	snapshot = Snapshot(timestamp, translation, rotation,
						color_image, depth_image,
						feelings)
	return snapshot, size + UINT32


def _to_tuple(message):
	return tuple([value for _, value in message.ListFields()])