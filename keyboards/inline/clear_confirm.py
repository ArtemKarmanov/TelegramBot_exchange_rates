from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def clear_currency_confirm_buttons() -> InlineKeyboardMarkup:
	"""
	Подтверждение очистки списка сохраненных валют пользователя.

	:return: markup
	"""
	# Инициализация клавиатуры, максимальное кол-во кнопок в строку — 2
	markup = InlineKeyboardMarkup(row_width=2)

	# Инициализация кнопок подтверждения либо отмены
	clear_yes = InlineKeyboardButton('Да', callback_data='yes')
	clear_no = InlineKeyboardButton('Нет', callback_data='no')

	# Добавление кнопок в клавиатуру
	markup.add(clear_yes, clear_no)

	return markup
