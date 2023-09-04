from datetime import datetime
from xmlrpc.client import Boolean

from site_API.core import get_latest_api


def get_datetime_now_api() -> str:
	"""
	Получение текущей даты и времени по данным от API.

	:return: result
	"""
	time_cur = get_latest_api['timestamp']
	result = transform_seconds_format(time_cur)

	return result


def transform_date_format(value: str, system_format: Boolean = False) -> str:
	"""
	Преобразование даты в читабельный формат.

	:param system_format: Вид формата
	:param value: Принимаемая дата
	:return: result
	"""
	# Если принимается системный формат, то вывод в виде «дд.мм.гггг», иначе наоборот
	if system_format:
		value_datetime = datetime.strptime(value, '%Y-%m-%d')
		result = value_datetime.strftime('%d.%m.%Y')
	else:
		value_datetime = datetime.strptime(value, '%d.%m.%Y')
		result = value_datetime.strftime('%Y-%m-%d')

	return result


def transform_seconds_format(value: int) -> str:
	"""
	Преобразование секунд в читабельный формат даты и времени.

	:param value: Принимаемые секунды
	:return: datetime_format
	"""
	value_timestamp = datetime.fromtimestamp(value)
	result = value_timestamp.strftime('%d.%m.%Y %H:%M')

	return result
