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


# TODO: might be a patlib built in
def make_path(root, *dirs):
    path = root
    for directory in dirs:
        path /= directory
        if not path.exists():
            path.mkdir()
    return path


def load_modules(root):
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if path.name.startswith('_') or not path.suffix == '.py':
            continue
        modules.append(importlib.import_module(f'{root.name}.{path.stem}', package=root.name))