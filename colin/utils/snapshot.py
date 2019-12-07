import datetime as dt
import struct

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

    def serialize(self):
        data = b''
        data += struct.pack('I', self.width)
        data += struct.pack('I', self.height)
        data += self.data
        return data

    @classmethod
    def deserialize(cls, data, im_type):
        part, data = data[:UINT32*2], data[UINT32*2:]
        width, height = struct.unpack('II', part)
        if im_type == 'color':
            data = data[:width*height*3]
        if im_type == 'depth':
            data = data[:width*height*FLOAT]
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
        # Unpack timestamp
        part, data = data[:UINT64], data[UINT64:]
        timestamp, = struct.unpack('Q', part)
        # Unpack translation
        part, data = data[:DOUBLE*3], data[DOUBLE*3:]
        translation = struct.unpack('ddd', part)
        # Unpack rotation
        part, data = data[:DOUBLE*4], data[DOUBLE*4:]
        rotation = struct.unpack('dddd', part)
        # Unpack images
        color_image = Image.deserialize(data, 'color')
        data = data[UINT32*2+len(color_image.data):]
        depth_image = Image.deserialize(data, 'depth')
        data = data[UINT32*2+len(depth_image.data):]
        # Unnpack feelings
        part = data[:FLOAT*4]
        feelings = struct.unpack('ffff', part)
        # Create snapshot instance
        return Snapshot(timestamp, translation, rotation,
                        color_image, depth_image, feelings)
