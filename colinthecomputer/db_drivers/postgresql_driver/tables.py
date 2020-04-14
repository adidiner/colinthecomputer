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
