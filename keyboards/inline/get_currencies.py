from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_currencies_buttons(currencies: list) -> InlineKeyboardMarkup:
	"""
	Вывод валюты в виде inline кнопок.

	:param currencies: Список валюты
	:return: markup
	"""
	# Инициализация клавиатуры, максимальное кол-во в строку — 3
	markup = InlineKeyboardMarkup(row_width=3)
	buttons_data = list()

	# Добавления каждой кнопки в список
	for i_name in currencies:
		buttons_data.append(InlineKeyboardButton(i_name, callback_data="currency_" + i_name))

	# Добавление кнопок в клавиатуру
	markup.add(*buttons_data)

	return markup
