import io


CHUNK = 1000000


def to_stream(data):
    if type(data) is io.BytesIO:
        return data
    return io.BytesIO(data)


def iterated_read(stream, size):
    read = 0
    chunks = []
    while read + CHUNK < size:
        chunks.append(stream.read(CHUNK))
        read += CHUNK
    chunks.append(stream.read(size-read))
    data = b''.join(chunks)
    return data


def parse_address(address):
    address = address.split(':')
    return (address[0], int(address[1]))