import struct
from datetime import datetime


class Thought:
    header_size = 20

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id!r}, ' \
               f'timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        ftimestamp = self.timestamp.strftime('[%Y-%m-%d %X]')
        return f'{ftimestamp} user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        return self.user_id == other.user_id and \
            self.timestamp == other.timestamp and \
            self.thought == other.thought

    def serialize(self):
        bthought = bytes(self.thought, 'utf-8')
        time = int(self.timestamp.timestamp())
        return struct.pack('QQI', self.user_id, time, len(bthought)) + bthought

    def deserialize(data):
        user_id, time, thought_size = \
         struct.unpack('QQI', data[:Thought.header_size])
        timestamp = datetime.fromtimestamp(time)
        thought = data[Thought.header_size:].decode('utf-8')
        return Thought(user_id, timestamp, thought)
