import sys
import os
import pathlib
import importlib
import inspect

from colinthecomputer.utils import load_packages, load_drivers


def _load_utils(util, module):
    utils = {}
    for key, value in module.__dict__.items():
        if key.startswith(f'{util}_') and callable(value):
            utils[key[len(f'{util}_'):]] = value
    return utils


root = pathlib.Path(os.path.dirname(__file__))
packages = load_packages(root)
drivers = load_drivers(packages)
for driver in drivers.values():
	# After loading for the first time, savers and getters are dicts
	# - make sure to load them only as modules
	if inspect.ismodule(driver.savers):
		driver.savers = _load_utils('save', driver.savers)
	if inspect.ismodule(driver.getters):
		driver.getters = _load_utils('get', driver.getters)
sys.modules[__name__] = drivers