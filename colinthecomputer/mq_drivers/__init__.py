"""Auto imported mq drivers.
When importing the package, it will expose the available read drivers as a dictionary.
i.e:
    import mq_drivers
    driver = read_drivers['rabbitmq']
Adding a file named "redguy_driver" to the pacakge 
will automaticaly expose the driver via read_drivers['redguy'].
A meesage queue driver must supply the read_user and read_snapshot methods.

read_user:
    Read user information from stream.
    
    :param stream: data stream, beginning with the user information
    :type stream: bytes-like object
    :returns: size of read data
    :rtype: int

read_snapshot:
    Read snapshot from stream.
    
    :param stream: data stream, beginning with the snapshot
    :type stream: bytes-like object
    :returns: size of read data
    :rtype: int
"""

import sys
import os
import pathlib
import importlib
import inspect

from colinthecomputer.utils import load_modules, load_drivers


root = pathlib.Path(os.path.dirname(__file__))
modules = load_modules(root)
drivers = load_drivers(modules)
sys.modules[__name__] = drivers