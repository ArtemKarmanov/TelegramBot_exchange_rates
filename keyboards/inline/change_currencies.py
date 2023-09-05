from xmlrpc.client import Boolean
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_change_currencies_buttons(get_all_buttons: Boolean = True) -> InlineKeyboardMarkup:
	"""
	Кнопки изменения списка валют пользователя.

	:param get_all_buttons: Вывод всех кнопок
	:return: markup
	"""
	# Инициализируем клавиатуры
	markup = InlineKeyboardMarkup(row_width=3)
	# Инициализация кнопок действия над списком валют (добавление, удаление, очистка)
	add_currency = InlineKeyboardButton('➕ Добавить', callback_data='add')
	delete_currency = InlineKeyboardButton('➖ Удалить', callback_data='delete')
	clear_currencies = InlineKeyboardButton('❌ Очистить', callback_data='clear')

	# Если нужны не все кнопки, то выводим только добавление
	if not get_all_buttons:
		markup = markup.add(add_currency)
	else:
		# Иначе добавляем все кнопки
		markup = markup.add(add_currency, delete_currency, clear_currencies)

	return markup
