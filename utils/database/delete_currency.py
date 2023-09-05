from xmlrpc.client import Boolean

from database.common.models import User, Currency


def delete_user_currency(user_telegram_id: int, name_currency: str = None, clear: Boolean = False) -> None:
	"""
	Удаление валюты из списка пользователя.

	:param user_telegram_id: Идентификатор телеграмма пользователя
	:param name_currency: Имя валюты
	:param clear: Полная очистка списка
	:return: None
	"""
	user = User.get(User.telegram_id == user_telegram_id)

	# Если clear = True, то полная очистка списка, иначе удаление выбранной валюты
	if clear:
		delete_currency = Currency.delete().where(Currency.owner == user)
	else:
		delete_currency = Currency.delete().where(Currency.owner == user, Currency.name == name_currency)

	delete_currency.execute()
