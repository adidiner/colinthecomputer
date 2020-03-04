from peewee import *
import sqlite3

db = SqliteDatabase('arazim.db')

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
    pass

class Snapshot(BaseModel):
    user = ForeignKeyField(User, backref='snapshots')
    datetime = DateTimeField()
    

init_db('127.0.0.1', 5432)
db.connect()
db.create_tables([Erez])

