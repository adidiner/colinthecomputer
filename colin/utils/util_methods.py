import io


CHUNK = 1000000


def to_stream(data):
    if type(data) is io.BytesIO:
        return data
    return io.BytesIO(data)


def iterated_read(stream, size):
    read, data = 0, b''
    while read + CHUNK < size:
        data += stream.read(CHUNK)
        read += CHUNK
    data += stream.read(size-read)
    return data