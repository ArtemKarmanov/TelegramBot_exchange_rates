from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def add_back_main_button() -> ReplyKeyboardMarkup:
	"""
	Кнопка для возврата на родительскую страницу.

	:return: markup
	"""
	# Инициализация клавиатуры и добавление кнопки «Вернуться»
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	back_main_page = KeyboardButton(text='Вернуться')
	markup.add(back_main_page)

	return markup


def edit_currencies_button() -> ReplyKeyboardMarkup:
	"""
	Кнопка для перехода к редактированию списка

	:return: markup
	"""
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	edit_currencies = KeyboardButton(text='Изменить список валют')
	markup.add(edit_currencies)

	return markup


def add_back_main_custom_button() -> ReplyKeyboardMarkup:
	"""
	Возврат на домашнюю страницу в команде custom.

	:return: markup
	"""
	markup = edit_currencies_button()
	back_main = KeyboardButton(text='Вернуться к выбору периода')
	markup.add(back_main)

	return markup


def remove_back_main_button() -> ReplyKeyboardRemove:
	"""
	Удаление кнопки, если пользователь находится на родительской странице.

	:return: ReplyKeyboardRemove()
	"""

	return ReplyKeyboardRemove()
