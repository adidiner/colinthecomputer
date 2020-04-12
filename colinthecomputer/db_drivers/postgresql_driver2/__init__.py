from .tables import db, User, Snapshot, Translation, Rotation, Pose, ColorImage, DepthImage, Feelings
from . import savers
from . import getters

def init_db(name, host, port, username, password):
    db.init(name, host=host, port=port,
            user=username, password=password)
    db.connect()
    db.create_tables([User, Snapshot, Translation, Rotation,
                  Pose, ColorImage, DepthImage, Feelings])

def _load_utils(util, module):
    utils = {}
    for key, value in module.__dict__.items():
        if key.startswith(f'{util}_') and callable(value):
            utils[key[len(f'{util}_'):]] = value
    return utils

savers = _load_utils('save', savers)
getters = _load_utils('get', getters)
print(savers)
print(getters)