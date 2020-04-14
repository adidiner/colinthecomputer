from peewee import *
from playhouse.shortcuts import model_to_dict
import psycopg2

from .tables import User, Snapshot, Translation, Rotation, Pose, ColorImage, DepthImage, Feelings


def save_user(user_id, username, birthday, gender):
    user, _ = User.get_or_create(**locals())
    user.save()

def save_pose(user_id, datetime, translation, rotation):
    translation = Translation(**translation)
    rotation = Rotation(**rotation)
    translation.save()
    rotation.save()
    pose = Pose(translation=translation,
                rotation=rotation)
    pose.save()
    snapshot, _ = Snapshot.get_or_create(user_id=user_id, datetime=datetime)
    snapshot.pose = pose
    snapshot.save()

def save_color_image(user_id, datetime, path):
    color_image = ColorImage(path=path)
    color_image.save()
    snapshot, _ = Snapshot.get_or_create(user_id=user_id, datetime=datetime)
    snapshot.color_image = color_image
    snapshot.save()

def save_depth_image(user_id, datetime, path):
    depth_image = DepthImage(path=path)
    depth_image.save()
    snapshot, _ = Snapshot.get_or_create(user_id=user_id, datetime=datetime)
    snapshot.depth_image = depth_image
    snapshot.save()

def save_feelings(user_id, datetime, feelings):
    print(feelings)
    feelings = Feelings(**feelings)
    print(feelings)
    feelings.save()
    print(feelings)
    snapshot, _ = Snapshot.get_or_create(user_id=user_id, datetime=datetime)
    snapshot.feelings = feelings
    snapshot.save()
