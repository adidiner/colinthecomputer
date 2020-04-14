from .tables import db, User, Snapshot, Translation, Rotation, Pose, ColorImage, DepthImage, Feelings
from . import savers
from . import getters

def init_db(name, host, port, username, password):
    db.init(name, host=host, port=port,
            user=username, password=password)
    db.connect()
    db.create_tables([User, Snapshot, Translation, Rotation,
                  Pose, ColorImage, DepthImage, Feelings])
