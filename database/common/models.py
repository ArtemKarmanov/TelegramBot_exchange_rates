from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField

db = SqliteDatabase('database/peewee_db.db')


class BaseModel(Model):
	"""
	Базовая модель для всех таблиц.
	"""
	class Meta:
		"""
		Добавляется связь с БД.
		"""
		database = db


class User(BaseModel):
	"""
	Модель пользователя.
	"""
	name = CharField()
	telegram_id = IntegerField()


class Currency(BaseModel):
	"""
	Модель валют привязанных к пользователю.
	"""
	owner = ForeignKeyField(User, backref='currencies')
	name = CharField()
