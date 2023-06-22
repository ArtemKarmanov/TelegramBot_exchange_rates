from peewee import *

db = SqliteDatabase('database/peewee_db.db')


class BaseModel(Model):
	class Meta:
		database = db


class Person(BaseModel):
	name = CharField()
	telegram_id = IntegerField()


class Currency(BaseModel):
	owner = ForeignKeyField(Person, backref='user')
	name = CharField()
