from typing import List

from database.common.models import User, History


def get_user_history(user_telegram_id, count) -> List:
	"""
	Вывод истории определенного кол-ва запросов пользователя.

	:param user_telegram_id: Идентификатор телеграмма пользователя
	:param count: Кол-во последних запросов
	:return:
	"""

	user = User.get(User.telegram_id == user_telegram_id)
	all_history = History.select().where(History.user == user).order_by(-History.created, -History.id).limit(10)
	result = list()

	for history in all_history:
		date_history = history.created.strftime('%d.%m.%Y %H:%M')
		result.append(f'[{date_history}] {history.text}')

	return result
