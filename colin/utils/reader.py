import gzip
import os


from . import read_drivers


drivers = {'binary': read_drivers.binary_reader,
           'protobuf': read_drivers.protobuf_reader}


class Reader:
    def __init__(self, path, file_format):
        self.path = path
        self.driver = drivers[file_format]
        self._offset = 0
        self.open = gzip.open if path.endswith('.gz') else open
        with self.open(path, 'rb') as f:
           self.user, offset = self.driver.read_user(f)
           self._offset += offset

    def __repr__(self):
        return f'Reader(path={self.path})'

    def __str__(self):
        return f'{self.user}'

    def __iter__(self):
        file_size = os.path.getsize(self.path)
        with self.open(self.path, 'rb') as f:
            f.seek(self._offset)
            while file_size - self._offset > 8:
                snapshot, offset = self.driver.read_snapshot(f)
                self._offset += offset
                yield snapshot


def read(path, file_format):
    reader = Reader(path, file_format)
    print(reader)
    for snapshot in reader:
        print(snapshot)
