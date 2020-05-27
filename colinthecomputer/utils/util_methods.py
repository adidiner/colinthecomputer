import io
import sys
import os
import pathlib
import importlib
import inspect
import functools
import traceback
import struct


CHUNK = 1000000


def gzip_size(path):
    """Get original size of gz compressed file"""
    with open(path, 'rb') as f:
        f.seek(-4, 2)
        return struct.unpack('I', f.read(4))[0]


def to_stream(data):
    """
    Converts data to byte-stream
    
    :param data: given data
    :type data: bytes-like object (can be string)
    :returns: bytestream
    :rtype: io.BytesIO
    """
    if type(data) is io.BytesIO:
        return data
    return io.BytesIO(data)


def iterated_read(stream, size):
    """
    Read size bytes from stream iterativly.
    
    :param stream: byte data stream
    :type stream: bytes-like stream
    :param size: amount to read
    :type size: int
    :returns: read data
    :rtype: bytestring
    """
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


def load_modules(root):
    """
    Loads all modules under root path, returns module dict.
    
    :param root: path to root directory where the requested modules are defined
    :type root: pathlib.Path (TODO)
    :returns: module dictionary, in the form {'mod_name': mod}
    :rtype: dict[str: module]
    """
    modules = []
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if path.name.startswith('_') or not path.suffix == '.py':
            continue
        modules.append(importlib.import_module(f'{root.name}.{path.stem}', package=root.name))
    return modules


def load_packages(root):
    """
    Loads all modules under root path, returns module dict.
    
    :param root: path to root directory where the requested modules are defined
    :type root: pathlib.Path (TODO)
    :returns: module dictionary, in the form {'mod_name': mod}
    :rtype: dict[str: module]
    """
    packages = []
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if path.name.startswith('_') or not path.is_dir():
            continue
        if (path / pathlib.Path('__init__.py')) not in [child for child in path.iterdir()]:
            continue
        packages.append(importlib.import_module(f'{root.name}.{path.stem}', package=root.name))
    return packages


def load_drivers(modules):
    """
    Load all modules marked as drivers in the given module.
    
    :param modules: module dictionary, in the form {'mod_name': mod}
    :type modules: dict[str: module]
    :returns: driver dictionary, in the form {'driver_name': driver}
    :rtype: dict[str: module]
    """
    drivers = {}
    for module in modules:
        name = module.__name__.split('.')[-1]
        if name.endswith('_driver'):
            drivers[name[:-len('_driver')]] = module
    return drivers


def filtered_dict(d, filter_keys):
    """
    Filter d to a dict with only the filter keys.
    
    Returns a new dict, containing the values of d only if key is in filter_keys.
    :param d: inirt dict
    :type d: dict
    :param filter_keys: keys to filter by
    :type filter_keys: list
    """
    return {key: value for key, value in d.items() if key in filter_keys}


def printerr(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as error:
            print(f"ERROR in {f.__module__}: {error}")
            traceback.print_tb(sys.exc_info()[2])
    return wrapper
