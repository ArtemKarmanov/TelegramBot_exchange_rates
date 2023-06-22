from datetime import datetime, date, timedelta
from site_API.core import site_data
from utils.site_API.data import find_in_site



def datetime_now() -> str:
	"""
	Текущая дата и время по данным от сайта.

	:return: result
	"""
	time_cur = find_in_site('timestamp', site_data)
	result = seconds_format(time_cur)

	return result


def date_format(value: date) -> str:
	"""
	Преобразование даты в читабельный формат.

	:param value: Принимаемая дата
	:return: result
	"""
	result = value.strftime('%d.%m.%Y')

	return result


def seconds_format(value: int) -> str:
	"""
	Преобразование секунд в читабельный формат даты и времени.

	:param value: Принимаемые секунды
	:return: datetime_format
	"""
	format = datetime.fromtimestamp(value)
	datetime_format = format.strftime('%d.%m.%Y %H:%M')

	return datetime_format


date_start = date_format(date.today() - timedelta(days=1))
date_end = date_format(date.today())
