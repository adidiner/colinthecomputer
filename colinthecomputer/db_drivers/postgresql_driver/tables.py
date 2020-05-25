from peewee import *
import psycopg2


db = PostgresqlDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = BigIntegerField(primary_key=True)
    username = CharField()
    birthday = IntegerField()
    gender = CharField(max_length=1)


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
    datetime = BigIntegerField()
    pose = ForeignKeyField(Pose, null=True, backref='snapshot')
    color_image = ForeignKeyField(ColorImage, null=True, backref='snapshot')
    depth_image = ForeignKeyField(DepthImage, null=True, backref='snapshot')
    feelings = ForeignKeyField(Feelings, null=True, backref='snapshot')
