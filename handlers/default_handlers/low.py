from telebot.types import Message
from loader import bot

import site_API.core as site
from utils.site_API.data import all_currency_in_site, find_in_site
from utils.site_API.date import datetime_now

from utils.database.CRUD import my_currency, add_currency_data, clear_my_currency, delete_currency

from keyboards.reply.back import request_back, remove_keyboard
from keyboards.inline.change import change_buttons
from keyboards.inline.currency import buttons_currency
from keyboards.inline.clear import clear_currency


@bot.message_handler(commands=['low'])
def bot_low(message: Message) -> None:

	bot.send_message(message.chat.id,
					 f'Текущий курс валют на {datetime_now()}',
					 reply_markup=remove_keyboard())

	bot_message = ''
	my_currency_list = my_currency(message.from_user.id)

	if my_currency_list:
		markup = change_buttons()
		value_rub = find_in_site('RUB', site.site_data)

		for i_name in my_currency_list:
			value = round(float(value_rub) / float(find_in_site(i_name, site.site_data)), 2)
			bot_message += i_name + ' — ' + str(value) + ' р.\n'
	else:
		bot_message = 'Список пуст. Добавить?'
		markup = change_buttons('add')

	bot.send_message(message.chat.id, bot_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call) -> None:

	my_currency_list = my_currency(call.from_user.id)

	if call.data == 'add_currency':
		bot_message = ''
		start_sym = ''

		for i_name in all_currency_in_site():
			if i_name not in my_currency_list and i_name != 'RUB':
				if start_sym != i_name[0]:
					start_sym = i_name[0]
					bot_message += '\n<b>' + start_sym + '</b>: ' + i_name
				else:
					bot_message += ', ' + i_name

		bot.send_message(call.message.chat.id, bot_message, parse_mode='html')
		bot.send_message(call.message.chat.id, 'Напишите, какую валюту необходимо добавить?', reply_markup=request_back())

		bot.register_next_step_handler(call.message, add_currency)

	elif call.data == 'del_currency':
		markup = buttons_currency(my_currency_list)
		bot.send_message(call.message.chat.id, 'Какую валюту удалить?', reply_markup=markup)

	elif call.data.startswith('del_name_'):
		name_currency = call.data[9:]
		bot.send_message(call.message.chat.id,
						 f'\U00002705 <b>{name_currency}</b> удалена из списка валют',
						 reply_markup=request_back(),
						 parse_mode="html")
		delete_currency(name_currency, call.from_user.id)

	elif call.data == 'clear_currency':
		markup = clear_currency()
		bot.send_message(call.message.chat.id,
						 '\U00002757 Вы уверены что хотите <b>полностью очистить</b> свой список валют?',
						 parse_mode="html",
						 reply_markup=markup)
	elif call.data == 'clear_currency_yes':
		clear_my_currency(call.from_user.id)
		bot.send_message(call.message.chat.id,
						 '\U00002705 Список полностью очищен.',
						 reply_markup=request_back())
	elif call.data == 'clear_currency_no':
		bot.send_message(call.message.chat.id,
						 'Список не был очищен.',
						 reply_markup=request_back())
	elif call.data == 'Вернуться':
		bot_low(call.message)


@bot.message_handler(content_types=['text'])
def add_currency(message: Message) -> None:
	text_end = ' Напишите какую еще валюту необходимо добавить, либо вернитесь обратно, нажав кнопку «Вернуться».'
	name = message.text.upper()

	if name in my_currency(message.from_user.id):
		bot.reply_to(message,
					 f'Ошибка. <b>{name}</b> уже есть в вашем списке валют!' + text_end,
					 parse_mode='html')
	elif name == 'RUB':
		bot.reply_to(message,
					 f'Ошибка. <b>{name}</b> невозможно добавить, так как расчёт ведется в рублях.' + text_end,
					 parse_mode='html')
	elif find_in_site(name, site.site_data):
		add_currency_data(name, message.from_user.id)
		bot.send_message(message.chat.id,
						 f'\U00002705 <b>{name}</b> добавлена в список валют.' + text_end,
						 parse_mode="html")
	elif message.text == 'Вернуться':
		bot_low(message)
	else:
		bot.send_message(message.chat.id, f'{message.text} нет в списке валют.' + text_end)
		bot.register_next_step_handler(message, add_currency)
