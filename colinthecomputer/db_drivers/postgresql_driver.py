from peewee import *
from playhouse.shortcuts import model_to_dict
import psycopg2

'''TODO: run in script: 
docker run --name postgres -d -e POSTGRES_PASSWORD=password -e
 POSTGRES_USER=colin(<-also db) -p  5432:5432 postgres
'''
db = PostgresqlDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = BigIntegerField(primary_key=True)
    username = CharField()
    birthday = IntegerField() #todo DateTimeField()
    gender = CharField(max_length=1) # TODO: Enum? THERE IS A PROBLEM HERE


class Translation(BaseModel):
    x = DoubleField()
    y = DoubleField()
    z = DoubleField()


class Rotation(BaseModel):
    x = DoubleField()
    y = DoubleField()
    z = DoubleField()
    w = DoubleField()


class Pose(BaseModel):
    translation = ForeignKeyField(Translation)
    rotation = ForeignKeyField(Rotation)


class ColorImage(BaseModel):
    path = CharField()


class DepthImage(BaseModel):
    path = CharField()


class Feelings(BaseModel):
    hunger = FloatField()
    thirst = FloatField()
    exhaustion = FloatField()
    happiness = FloatField()


class Snapshot(BaseModel):
    snapshot_id = AutoField()
    user_id = IntegerField()
    datetime = BigIntegerField() # TODO DateTimeField()
    pose = ForeignKeyField(Pose, null=True, backref='snapshot')
    color_image = ForeignKeyField(ColorImage, null=True, backref='snapshot')
    depth_image = ForeignKeyField(DepthImage, null=True, backref='snapshot')
    feelings = ForeignKeyField(Feelings, null=True, backref='snapshot')


def init_db(name, host, port, username, password):
    db.init(name, host=host, port=port,
            user=username, password=password)
    db.connect()
    db.create_tables([User, Snapshot, Translation, Rotation,
                  Pose, ColorImage, DepthImage, Feelings])

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
    feelings = Feelings(**feelings)
    feelings.save()
    snapshot, _ = Snapshot.get_or_create(user_id=user_id, datetime=datetime)
    snapshot.feelings = feelings
    snapshot.save()

savers = {'pose': save_pose, 'color_image': save_color_image, 'depth_image': save_depth_image,
          'feelings': save_feelings, 'user': save_user} # TODO: automatic collection


def get_users():
    users = []
    for user in User.select():
        user = model_to_dict(user, 
                             only=[User.user_id, User.username])
        users.append(user)
    return users

def get_user_info(user_id):
    query = User.select().where(User.user_id==user_id)
    if not query.exists():
        return None
    user = query.get()
    return model_to_dict(user)

def get_snapshots(user_id):
    query = Snapshot.select().where(Snapshot.user_id==user_id)
    snapshots = []
    for snapshot in query:
        snapshot = model_to_dict(snapshot, 
                                 only=[Snapshot.snapshot_id, Snapshot.datetime])
        snapshots.append(snapshot)
    return snapshots

def get_snapshot_info(snapshot_id):
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

getters = {'users': get_users, 'user_info': get_user_info, 'snapshots': get_snapshots,
          'snapshot_info': get_snapshot_info, 'result': get_result} # TODO: automatic collection