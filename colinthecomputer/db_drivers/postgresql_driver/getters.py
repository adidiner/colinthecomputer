from peewee import *
from playhouse.shortcuts import model_to_dict
import psycopg2

from .tables import User, Snapshot, Translation, Rotation, Pose, ColorImage, DepthImage, Feelings

def get_users():
    """Gets all available users' id and name.
    """
    users = []
    for user in User.select():
        user = model_to_dict(user, 
                             only=[User.user_id, User.username])
        users.append(user)
    return users


def get_user_info(user_id):
    """Gets full user's information.
    """
    query = User.select().where(User.user_id==user_id)
    if not query.exists():
        return None
    user = query.get()
    return model_to_dict(user)


def get_snapshots(user_id):
    """Gets basic snapshot information for all the user's snapshots.
    """
    query = Snapshot.select().where(Snapshot.user_id==user_id)
    snapshots = []
    for snapshot in query:
        snapshot = model_to_dict(snapshot, 
                                 only=[Snapshot.snapshot_id, Snapshot.datetime])
        snapshots.append(snapshot)
    return snapshots

def get_snapshot_info(snapshot_id):
    """Gets verbose snapshot information, listing available results.
    """
    query = Snapshot.select().where(Snapshot.snapshot_id==snapshot_id)
    if not query.exists():
        return None
    snapshot = query.get()
    metadata = model_to_dict(snapshot,
                             only=[Snapshot.snapshot_id, Snapshot.datetime])
    data = model_to_dict(snapshot,
                            exclude=[Snapshot.snapshot_id, Snapshot.datetime, Snapshot.user_id])
    results = [field for field in data if data[field]]
    return {**metadata, 'results': results}


def get_result(snapshot_id, result_name):
    """Gets snapshot's result data.
    """
    query = Snapshot.select().where(Snapshot.snapshot_id==snapshot_id)
    if not query.exists():
        return None
    snapshot = query.get()
    snapshot = model_to_dict(snapshot, exclude=[Pose.id, Pose.translation.id, Pose.rotation.id,
                                                ColorImage.id, DepthImage.id, Feelings.id])
    if result_name not in snapshot:
        return None
    result = snapshot[result_name]
    return result
