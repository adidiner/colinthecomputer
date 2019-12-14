import sys
import pathlib
import importlib
import inspect

modules = []
parsers = {} # TODO: parsers support multiple feilds
root = pathlib.Path.cwd() / 'colin/parsers/'

def load_modules(root):
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if path.name.startswith('_') or not path.suffix == '.py':
            continue
        modules.append(importlib.import_module(f'{root.name}.{path.stem}', package=root.name))

def load_parsers(module):
    for key, value in module.__dict__.items():
        if key.startswith('parse_') and callable(value):
            parsers[value.field] = value
        if key.endswith('Parser') and inspect.isclass(value):
            parsers[value.field] = value().__dict__['parse']

load_modules(root)
for module in modules:
    load_parsers(module)