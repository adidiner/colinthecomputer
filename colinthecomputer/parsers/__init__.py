"""Auto imported parsers.

You may add new parsers by writing a ``parse_somthing`` function,
or ``SomethingParser`` class,
and specifing it's field in a parser.field attribute.

After adding a parser with a curtain field,
it can be invoked with the ``run_parser`` function
and with the ``parse`` and ``run-parser`` cli,
using the specified field.
"""


import pathlib
import inspect
import os

from colinthecomputer.utils import load_modules

modules = []
parsers = {}
root = pathlib.Path(os.path.dirname(__file__))


def load_parsers(module):
    for key, value in module.__dict__.items():
        if key.startswith('parse_') and callable(value):
            parsers[value.field] = value
        if key.endswith('Parser') and inspect.isclass(value):
            parsers[value.field] = value().parse


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
        return parsers[field](data)
    except Exception as error:
        print(f"ERROR: {error}")
