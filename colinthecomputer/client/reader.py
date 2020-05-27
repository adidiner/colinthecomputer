import gzip
import os

from . import read_drivers
import colinthecomputer.protocol as ptc
from colinthecomputer.utils import gzip_size


class Reader:
    """
    Reader of a sample file, exposing iteration over snapshots.

    :param path: path to the sample file
    :type path: str
    :param file_format: the sample file format
    :type file_format: str
    """
    def __init__(self, path, file_format):
        self.path = path
        self.driver = read_drivers[file_format]
        self.open = gzip.open if path.endswith('.gz') else open
        self.file_size = gzip_size(path) if path.endswith('.gz') \
                                         else os.path.getsize(path)
        self._offset = 0
        with self.open(path, 'rb') as f:
            self.user, offset = self.driver.read_user(f)
            self._offset += offset

    def __repr__(self):
        return f'Reader(path={self.path})'

    def __str__(self):
        return f'{self.user}'

    def __iter__(self):
        with self.open(self.path, 'rb') as f:
            f.seek(self._offset)
            # read snapshots with driver
            while self.file_size - self._offset > 8:
                snapshot, offset = self.driver.read_snapshot(f)
                self._offset += offset
                yield snapshot


def read(path, file_format):
    """
    Read and print all snapshots in sample file.

    :param path: path to the sample file
    :type path: str
    :param file_format: the sample file format
    :type file_format: str
    """
    reader = Reader(path, file_format)
    print(ptc.user_str(reader.user))
    count = 0
    for snapshot in reader:
        #print(ptc.snapshot_str(snapshot))
        count += 1
    print(count)
