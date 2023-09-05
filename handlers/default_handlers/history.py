from loader import bot
from telebot.types import Message

from utils.database.get_history import get_user_history
from keyboards.reply.back_main import remove_back_main_button


@bot.message_handler(state='*', commands=['history'])
def view_history_user(message: Message) -> None:
	"""
	Вывод истории запросов пользователя

	:param message: Сообщение пользователя
	:return: None
	"""
	bot.send_message(message.chat.id, 'История последних 10 ваших запросов.\n\n')
	user_history = get_user_history(message.from_user.id, 10)
	bot_message = ''

	if not user_history:
		bot_message = 'Ваша история запросов пуста.'

	for history in user_history:
		bot_message += f'{history}\n'

	markup = remove_back_main_button()
	bot.send_message(message.chat.id, bot_message, reply_markup=markup)
