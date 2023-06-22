from telebot.types import List

from database.common.models import Person, Currency


def my_currency(user_tg_id: int) -> List:
	"""
	Список всех валют сохраненных у пользователя.

	:param user_tg_id: id телеграмма пользователя
	:return: result
	"""
	user = Person.get(telegram_id=user_tg_id)
	currency_data = Currency.select().where(Currency.owner == user)
	result = []

	for i_currency in currency_data:
		result.append(i_currency.name)

	return result


def add_currency_data(name: str, user_tg_id: int) -> bool:
	"""
	Добавление валюты в список пользователя в БД.

	:param name: Название валюты
	:param user_tg_id: id телеграмма пользователя
	:return: bool
	"""
	user = Person.get(telegram_id=user_tg_id)
	Currency.create(owner=user, name=name)

	return True


def clear_my_currency(user_tg_id: int) -> bool:
	"""
	Удаление всего списка валют пользователя в БД.

	:param user_tg_id: id телеграмма пользователя
	:return: bool
	"""
	user = Person.get(telegram_id=user_tg_id)
	currency_data = Currency.delete().where(Currency.owner == user)
	currency_data.execute()

	return True


def delete_currency(name: str, user_tg_id: int) -> bool:
	"""
	Удаление определенной валюты из списка пользователя в БД.

	:param name: Название валюты
	:param user_tg_id: id телеграмма пользователя
	:return: bool
	"""
	user = Person.get(telegram_id=user_tg_id)
	currency_data = Currency.delete().where(Currency.owner == user, Currency.name == name)
	currency_data.execute()

	return True
