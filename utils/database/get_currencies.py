from typing import List

from database.common.models import User


def get_user_currencies(user_telegram_id: int) -> List:
	"""
	Список всех валют пользователя.

	:param user_telegram_id: Идентификатор telegram пользователя
	:return: result
	"""
	user = User.get(User.telegram_id == user_telegram_id)
	result = list()

	# Добавление валюты в список
	for currency in user.currencies:
		result.append(currency.name)

	result = sorted(result)

	return result
