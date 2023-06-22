from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def change_buttons(which: str = 'all') -> InlineKeyboardMarkup:
	"""
	Кнопки изменения списка валют пользователя.

	:param which: Если all, то вывести все, иначе только кнопку "Добавить".
	:return: markup
	"""
	markup = InlineKeyboardMarkup(row_width=3)
	add_currency = InlineKeyboardButton("\U00002795 Добавить", callback_data="add_currency")
	del_currency = InlineKeyboardButton("\U00002796 Удалить", callback_data="del_currency")
	clear_currency = InlineKeyboardButton("\U0000274C Очистить", callback_data="clear_currency")

	if which == 'add':
		markup.add(add_currency)
	else:
		markup.add(add_currency, del_currency, clear_currency)

	return markup
