from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def buttons_currency(data: list) -> InlineKeyboardMarkup:
	"""
	Вывод валюты в виде inline кнопок.

	:param data: Список валюты
	:return: markup
	"""
	markup = InlineKeyboardMarkup(row_width=3)
	buttons_list = list()

	for i_name in data:
		buttons_list.append(InlineKeyboardButton(i_name, callback_data="del_name_" + i_name))

	markup.add(*buttons_list)

	return markup
