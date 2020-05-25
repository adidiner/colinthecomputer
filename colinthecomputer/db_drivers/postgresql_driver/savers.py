from peewee import *
import psycopg2

from .tables import (User,
                     Snapshot,
                     Translation,
                     Rotation,
                     Pose,
                     ColorImage,
                     DepthImage,
                     Feelings,
                     )


def save_user(user_id, username, birthday, gender):
    """Saves user information."""
    user, _ = User.get_or_create(**locals())
    user.save()


def save_pose(user_id, datetime, data):
    """Saves pose (translation, rotation) data."""
    translation = Translation(**data['translation'])
    rotation = Rotation(**data['rotation'])
    translation.save()
    rotation.save()
    pose = Pose(translation=translation,
                rotation=rotation)
    pose.save()
    _update_snapshot(user_id, datetime, 'pose', pose)


def save_color_image(user_id, datetime, data):
    """Saves color image data (i.e path)."""
    color_image = ColorImage(path=data['path'])
    color_image.save()
    _update_snapshot(user_id, datetime, 'color_image', color_image)


def save_depth_image(user_id, datetime, data):
    """Saves depth image data (i.e path)."""
    depth_image = DepthImage(path=data['path'])
    depth_image.save()
    _update_snapshot(user_id, datetime, 'depth_image', depth_image)


def save_feelings(user_id, datetime, data):
    """Saves feelings data."""
    feelings = Feelings(**data)
    feelings.save()
    _update_snapshot(user_id, datetime, 'feelings', feelings)


def _update_snapshot(user_id, datetime, field, value):
    if not Snapshot.get_or_none(user_id=user_id, datetime=datetime):
        Snapshot.create(user_id=user_id,
                        datetime=datetime)
    (Snapshot
     .update(**{field: value})
     .where((Snapshot.user_id == user_id) & 
            (Snapshot.datetime == datetime))
     .execute())
