from database.common.models import Person, Currency


def new_person(name: str, telegram_id: int) -> Person:
	"""
	Добавление нового пользователя в БД.

	:param name: имя пользователя
	:param telegram_id: id телеграмма пользователя
	:return: user
	"""
	user, user_is = Person.get_or_create(name=name, telegram_id=telegram_id)

	if user_is:
		Currency.get_or_create(owner=user, name='USD')
		Currency.get_or_create(owner=user, name='EUR')

	return user
