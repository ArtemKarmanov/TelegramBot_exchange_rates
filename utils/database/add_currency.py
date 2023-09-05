from database.common.models import Currency, User


def add_currency_user(user_telegram_id: int, name_currency: str):
	"""
	Добавление валюты в список пользователя.

	:param user_telegram_id: Идентификатор телеграмма пользователя
	:param name_currency: Название валюты
	:return:
	"""
	user = User.get(User.telegram_id == user_telegram_id)
	Currency.create(owner=user, name=name_currency)
