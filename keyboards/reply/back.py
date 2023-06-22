from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def request_back() -> ReplyKeyboardMarkup:
	"""
	Кнопка для возврата на родительскую страницу

	:return: markup
	"""
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(KeyboardButton('Вернуться'))

	return markup


def remove_keyboard() -> ReplyKeyboardRemove:
	"""
	Удаление кнопки, если пользователь находится на родительской странице
	:return:
	"""

	return ReplyKeyboardRemove()
