from telebot.types import List

from site_API.core import site_data


def find_in_site(currency: str, data=site_data) -> int:
	"""
	Поиск валюты по данным от сайта.

	:param currency: Название валюты
	:param data: Данные, выгруженные с сайта
	:return: result
	"""
	if currency in data.keys():

		return round(data[currency], 2)

	for i_value in data.values():
		if isinstance(i_value, dict):
			result = find_in_site(currency, i_value)

			return result


def all_currency_in_site() -> List:
	"""
	Список всех валют по данным от сайта.

	:return: result
	"""
	result = [i_currency for i_currency in site_data['rates'].keys()]
	result.sort()

	return result
