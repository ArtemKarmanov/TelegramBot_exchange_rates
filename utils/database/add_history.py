from database.common.models import User, History


def add_user_history(user_telegram_id: int, text: str) -> None:
	"""
	Сохранение запроса пользователя в историю.

	:param user_telegram_id: Идентификатор телеграмма пользователя
	:param text: Запрос пользователя
	:return: None
	"""
	user = User.get(User.telegram_id == user_telegram_id)
	new_history = History.create(user=user, text=text)
