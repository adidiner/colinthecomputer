"""
Auto imported db drivers.
When importing the package,
it will expose the available database drivers as a dictionary.
i.e:
    import db_drivers
    driver = db_drivers['postgresql']
Adding a file named "duckguy_driver" to the pacakge
will automaticaly expose the driver via db_drivers['duckguy'].
A db_driver has savers, getters attributes,
which enable saving and acessing data.
i.e:
    # in this example, driver.savers['character'] saves character information
    driver.savers['character'](name='roy', color='yellow', age='?')
    # saves data
    # in this example, driver.getters['character']
    # gets the existing characters in the db
    driver.getters['characters']()
    > ['roy']
The savers and getters are automatically collected,
and must be written in savers.py and getters.py modules
and be named save_field and get_field respectively.

To support the working project,
a driver must support the following savers
(but can expose more savers):
save_user(user_id, username, birthday, gender)
save_pose(user_id, datetime, data)
save_color_image(user_id, datetime, data)
save_depth_image(user_id, datetime, data)
save_feelings(user_id, datetime, data)

And the following getters:
get_users()
get_user_info(user_id)
get_snapshots(user_id)
get_snapshot_info(snapshot_id)
get_result(snapshot_id, result_name)
"""


import sys
import os
import pathlib
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
