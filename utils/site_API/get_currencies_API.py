from typing import Any

from telebot.types import List

from site_API.core import get_latest_api, get_period_date_currencies


def get_value_currency_api(user_currency: Any) -> Any:
	"""
	Курс валют по данным от API.

	:param user_currency: Валюта либо список валют
	:return: result
	"""
	# Список валют из API
	data = get_latest_api['rates']

	# Если список валют, то вывод результата в виде словаря
	if isinstance(user_currency, list):
		result = dict()

		# Добавление в словарь со значением, если валюта есть в API
		for currency in user_currency:
			if currency in data.keys():
				result[currency] = data[currency]

		return result

	# Вывод курса одной валюты
	return data[user_currency]


def get_currencies_api() -> List:
	"""
	Список всех валют по данным API.

	:return: result
	"""
	# Список валют из API
	data = get_latest_api['rates']

	# Сортировка и вывод в виде списка
	result = list(sorted(data.keys()))

	return result


def get_period_currencies_api(start_date, end_date):
	"""
	Список дат с курсом валют за период.

	:param start_date: Начальная дата
	:param end_date: Конечная дата
	:return: period_data
	"""
	# Берем данные с API с указанным периодом
	data = get_period_date_currencies(start_date, end_date)

	# Сортируем данные и выводим в виде словаря
	period_data = dict(sorted(data['rates'].items()))

	return period_data
