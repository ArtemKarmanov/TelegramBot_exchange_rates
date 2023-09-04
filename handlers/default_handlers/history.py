from loader import bot
from telebot.types import Message


@bot.message_handler(state='*', commands=['history'])
def get_history_user(message: Message):
	"""
	Вывод истории запросов пользователя

	:param message:
	:return:
	"""
