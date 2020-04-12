import io
import sys
import os
import pathlib
import importlib
import inspect


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
    modules = []
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if path.name.startswith('_') or not path.suffix == '.py':
            continue
        modules.append(importlib.import_module(f'{root.name}.{path.stem}', package=root.name))
    return modules

def load_drivers(modules):
    drivers = {}
    for module in modules:
        name = pathlib.Path(module.__file__).stem
        if name.endswith('_driver'):
            drivers[name[:-len('_driver')]] = module
    return drivers

def filtered_dict(d, filter_keys):
    return {key: value for key, value in d.items() if key in filter_keys}



