from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def clear_currency() -> InlineKeyboardMarkup:
	markup = InlineKeyboardMarkup(row_width=2)
	yes = InlineKeyboardButton('Да', callback_data='clear_currency_yes')
	no = InlineKeyboardButton('Нет', callback_data='clear_currency_no')
	markup.add(yes, no)

	return markup
