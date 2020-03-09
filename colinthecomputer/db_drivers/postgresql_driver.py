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

    def dict(self):
        result = model_to_dict(self)
        del result['id']
        return result


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

    def dict(self):
        result = {}
        result['translation'] = self.translation.dict()
        result['rotation'] = self.rotation.dict()
        return result


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
    # print("saved")
    snapshot.save()
    #print('USERS', get_users())
    #print('USER_INF0', get_user_info(42))
    #print(get_snapshots(42))
    #print('SNAPSHOT', get_snapshot(3))
    #print('RESULT', get_result(3, 'pose'))

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
    fields = ['user_id', 'username']
    users = []
    for user in User.select():
        user = model_to_dict(user)
        result = {key: user[key] for key in fields}
        users.append(result)
    return users

def get_user_info(user_id):
    query = User.select().where(User.user_id==user_id)
    if not query.exists():
        return None # TODO: what should I return?
    user = query.get()
    return model_to_dict(user)

def get_snapshots(user_id):
    fields = ['snapshot_id', 'datetime']
    query = Snapshot.select().where(Snapshot.user_id==user_id)
    snapshots = []
    for snapshot in query:
        snapshot = model_to_dict(snapshot)
        result = {key: snapshot[key] for key in fields}
        snapshots.append(result)
    return snapshots

def get_snapshot_info(snapshot_id):
    metadata = ['snapshot_id', 'datetime']
    query = Snapshot.select().where(Snapshot.snapshot_id==snapshot_id)
    if not query.exists():
        return None # TODO: what should I return?
    snapshot = query.get()
    snapshot = model_to_dict(snapshot)
    result = {key: snapshot[key] for key in metadata}
    result['results'] = []
    # Append available results (not None)
    for field, value in snapshot.items():
        if value and field not in metadata + ['user_id']:
            result['results'].append(field)
    return result

def get_result(snapshot_id, result_name):
    blobs = ['color_image', 'depth_image']
    query = Snapshot.select().where(Snapshot.snapshot_id==snapshot_id)
    if not query.exists():
        return None # TODO: what should I return?
    snapshot = query.get()
    #snapshot = model_to_dict(snapshot)
    #result = snapshot[result_name]
    if result_name not in blobs:
        result = snapshot.pose.dict()
        return result
    else:
        pass # TODO

getters = {'users': get_users, 'user_info': get_user_info, 'snapshots': get_snapshots,
          'snapshot_info': get_snapshot_info, 'result': get_result} # TODO: automatic collection