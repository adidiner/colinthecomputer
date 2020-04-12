import sys
import pathlib
import importlib
import inspect
import os

from colinthecomputer.utils import load_modules

modules = []
parsers = {} # TODO: parsers support multiple fields? do I even need this?
root = pathlib.Path(os.path.dirname(__file__))

def load_parsers(module):
    for key, value in module.__dict__.items():
        if key.startswith('parse_') and callable(value):
            parsers[value.field] = value
        if key.endswith('Parser') and inspect.isclass(value):
            parsers[value.field] = value().__dict__['parse']

modules = load_modules(root)
for module in modules:
    load_parsers(module)

def run_parser(field, data):
    """Run available parser for field, on the given data.
    
    :param field: snapshot field to parse
    :type field: str
    :param data: data as consumed from the message queue
    :type data: json
    """
    try:
        parsers[field](data)
    except Exception as error:
        print(f"ERROR: {error}")