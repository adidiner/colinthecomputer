import sys
import pathlib
import importlib
import inspect

from colinthecomputer.utils import load_modules

modules = []
parsers = {} # TODO: parsers support multiple fields? do I even need this?
root = pathlib.Path.cwd() / 'colinthecomputer/parsers/'

def load_parsers(module):
    for key, value in module.__dict__.items():
        if key.startswith('parse_') and callable(value):
            parsers[value.field] = value
        if key.endswith('Parser') and inspect.isclass(value):
            parsers[value.field] = value().__dict__['parse']

load_modules(root)
for module in modules:
    load_parsers(module)

def run_parser(field, data):
    parsers[field](data)