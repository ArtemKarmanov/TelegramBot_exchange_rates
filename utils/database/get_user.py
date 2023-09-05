from xmlrpc.client import Boolean


from database.common.models import User, Currency


def get_or_create_user(name: str, telegram_id: int) -> Boolean:
	"""
	Добавление нового пользователя в БД.

	:param name: Имя пользователя
	:param telegram_id: id телеграмма пользователя
	:return: user
	"""
	user, created = User.get_or_create(name=name, telegram_id=telegram_id)

	# Если пользователя только что был создан, то добавляются связанные валюты по умолчанию
	if created:
		Currency.create(owner=user, name='USD')
		Currency.create(owner=user, name='EUR')

		# Флаг для приветствия нового пользователя.
		return True
	# Либо приветствие уже зарегистрированного ранее.
	return False
