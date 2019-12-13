import datetime as dt
import struct

from .util_methods import to_stream

UINT64 = 8
UINT32 = 4
CHAR = 1
DOUBLE = 8
FLOAT = 4


class Image:
    def __init__(self,  im_type, width, height, data):
        self.type = im_type
        self.width = width
        self.height = height
        self.data = data

    def __repr__(self):
        return f'<Image: {self.type} {self.width}x{self.height}>'

    def __str__(self):
        return f'{self.width}x{self.height} {self.type} image'

    def __eq__(self, other):
        if not isinstance(other, Image):
            return False
        return self.type == other.type and \
            self.width == other.width and \
            self.height == other.height and \
            self.data == other.data

    def serialize(self):
        data = b''
        data += struct.pack('I', self.width)
        data += struct.pack('I', self.height)
        if self.data:
            data += self.data
        return data

    @classmethod
    def deserialize(cls, data, im_type):
        stream = to_stream(data)
        width, height = struct.unpack('II', stream.read(UINT32*2))
        if im_type == 'color':
            data = stream.read(width*height*3)
        if im_type == 'depth':
            data = stream.read(width*height*FLOAT)
        return cls(im_type, width, height, data)


class Snapshot:
    def __init__(self, timestamp, translation=(0, 0, 0), rotation=(0, 0, 0, 0),
                 color_image=None, depth_image=None, feelings=(0, 0, 0, 0)):
        self.timestamp = timestamp
        self.datetime = dt.datetime.fromtimestamp(self.timestamp*(10**(-3)))
        self.translation = translation
        self.rotation = rotation
        if color_image:
            self.color_image = color_image
        else:
            self.color_image = Image('color', 0, 0, None)
        if depth_image:
            self.depth_image = depth_image
        else:
            self.depth_image = Image('depth', 0, 0, None)
        self.feelings = feelings

    def __repr__(self):
        return f'Snapshot(datetime={self.datetime}, ' \
               f'translation={self.translation}, ' \
               f'rotation={self.rotation}, ' \
               f'color_image={self.color_image!r}, ' \
               f'depth_image={self.depth_image!r}, ' \
               f'feelings={self.feelings}'

    def __str__(self):
        fdate = self.datetime.strftime('%B %d, %Y')
        ftime = self.datetime.strftime('%X.%f')
        return f'Snapshot from {fdate} at {ftime} on ' \
               f'{self.translation} / {self.rotation} ' \
               f'with a {self.color_image} and a {self.depth_image}, ' \
               f'feelings are {self.feelings}.'

    def __eq__(self, other):
        if not isinstance(other, Snapshot):
            return False
        return self.datetime == other.datetime and \
            self.translation == other.translation and \
            self.rotation == other.rotation and \
            self.color_image == other.color_image and \
            self.depth_image == other.depth_image and \
            self.feelings == other.feelings

    def __getitem__(self, key):
        return self.__dict__[key]

    def __iter__(self):
        for key in self.__dict__:
            yield key

    def serialize(self):
        data = b''
        data += struct.pack('Q', self.timestamp)
        data += struct.pack('ddd', *self.translation)
        data += struct.pack('dddd', *self.rotation)
        data += self.color_image.serialize()
        data += self.depth_image.serialize()
        data += struct.pack('ffff', *self.feelings)
        return data

    @classmethod
    def deserialize(cls, data):
        stream = to_stream(data)
        timestamp, = struct.unpack('Q', stream.read(UINT64))
        translation = struct.unpack('ddd', stream.read(DOUBLE*3))
        rotation = struct.unpack('dddd', stream.read(DOUBLE*4))
        color_image = Image.deserialize(stream, 'color')
        depth_image = Image.deserialize(stream, 'depth')
        feelings = struct.unpack('ffff', stream.read(FLOAT*4))
        # Create snapshot instance
        return Snapshot(timestamp, translation, rotation,
                        color_image, depth_image, feelings)
