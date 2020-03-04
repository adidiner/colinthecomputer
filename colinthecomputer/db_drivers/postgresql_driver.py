from peewee import *
import sqlite3

db = SqliteDatabase('colin.db')

def init_db(host, port):
    db.init('colin')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = IntegerField()
    username = CharField()
    birthday = DateTimeField()
    gender = FixedCharField() # TODO: Enum?


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
    user = ForeignKeyField(User, backref='snapshots')
    datetime = DateTimeField()
    pose = ForeignKeyField(Pose, null=True, backref='snapshot')
    color_image = ForeignKeyField(ColorImage, null=True, backref='snapshot')
    depth_image = ForeignKeyField(DepthImage, null=True, backref='snapshot')
    feelings = ForeignKeyField(Feelings, null=True, backref='snapshot')


init_db('127.0.0.1', 5432)
db.connect()
db.create_tables([User, Snapshot])

def snapshot_query(user_id, datetime):
    snapshot_query = (Snapshot.select().where())

def save_pose(user_id, datetime, translation, rotation):
    translation = Translation(**translation)
    rotation = Rotation(**rotation)
    pose = Pose(translation=translation,
                rotation=rotation)
