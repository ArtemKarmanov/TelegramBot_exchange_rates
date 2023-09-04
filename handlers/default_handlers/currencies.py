from keyboards.inline.clear_confirm import clear_currency_confirm_buttons
from keyboards.inline.get_currencies import get_currencies_buttons
from keyboards.reply.back_main import add_back_main_button, remove_back_main_button
from loader import bot
from telebot.types import Message, CallbackQuery

from states.custom_states import ChangeUserCurrencies
from utils.database.get_currencies import get_user_currencies
from keyboards.inline.change_currencies import get_change_currencies_buttons
from utils.database.add_currency import add_currency_user
from utils.database.delete_currency import delete_user_currency
from utils.site_API.get_currencies_API import get_currencies_api


@bot.message_handler(state='*', commands=['currencies'])
def get_currencies(message: Message) -> None:
	"""
	Вывод всех валют пользователя с курсом.

	:param message: Сообщение
	:return: None
	"""
	bot_message = '📋 Ваш список валют:\n\n'
	bot_end_msg = (
		'\n💬 Выберите действие, чтобы редактировать список.\n\n'
		'Кнопка <b>«Добавить»</b> позволяет добавить новую валюту в свой список.\n'
		'Кнопка <b>«Удалить»</b> позволяет удалить определенную валюту из вашего списка.\n'
		'Кнопка <b>«Очистить»</b> полностью очистит ваш список.'
	)

	# Проверяем наличие списка валют пользователя
	user_currencies = get_user_currencies(message.from_user.id)

	# Если список есть, то выводим текущий курс
	if user_currencies:
		# Добавляем все кнопки (добавление, удаление, список)
		markup = get_change_currencies_buttons(get_all_buttons=True)
		for index, currency in enumerate(user_currencies):
			bot_message += f'{index + 1}. {currency}\n'
	else:
		# Предлагаем добавить валюту, если список пуст
		bot_message += '<b>Список сохраненных валют пуст.</b>'
		bot_end_msg = '\nНажмите на кнопку «Добавить», чтобы пополнить список.'
		# Вывод кнопки «Добавить»
		markup = get_change_currencies_buttons(get_all_buttons=False)

	bot.send_message(message.chat.id, bot_message, reply_markup=remove_back_main_button(), parse_mode='html')
	bot.send_message(message.chat.id, bot_end_msg, reply_markup=markup, parse_mode='html')


@bot.message_handler(state='*', func=lambda message: message.text in ['Вернуться', 'Изменить список валют'])
def back_main_page(message: Message) -> None:
	"""
	Возврат на стартовую страницу при нажатии на кнопку «Вернуться».

	:param message: Сообщение
	:return: None
	"""
	bot.delete_state(message.from_user.id, message.chat.id)

	get_currencies(message)


@bot.callback_query_handler(func=lambda call: call.data == 'delete')
def delete_callback(call: CallbackQuery) -> None:
	"""
	Выбор удаляемой валюты.

	:param call: Сообщение
	:return: None
	"""
	bot.set_state(call.from_user.id, ChangeUserCurrencies.delete, call.message.chat.id)

	markup_back = add_back_main_button()
	bot.send_message(call.message.chat.id, '➡️ Вы в разделе «Удалить».\n\n', reply_markup=markup_back)

	# Если у пользователя есть список валют, то добавляем кнопки
	user_currencies = get_user_currencies(call.from_user.id)
	if user_currencies:
		bot_message = 'Нажмите на валюту чтобы удалить из своего списка.\n\n'
		# Добавление валют пользователя в виде кнопок
		markup_currencies = get_currencies_buttons(user_currencies)
	else:
		bot_message = '<b>Ваш список валют пуст.</b>\n\n'
		markup_currencies = None

	bot.send_message(
		call.message.chat.id,
		bot_message +
		'Чтобы вернуться к вашему списку валют, нажмите кнопку «Вернуться».',
		parse_mode='html',
		reply_markup=markup_currencies
	)


@bot.callback_query_handler(state=ChangeUserCurrencies.delete, func=lambda call: call.data.startswith('currency_'))
def delete_name_callback(call: CallbackQuery) -> None:
	"""
	Удаление выбранной валюты.

	:param call: Сообщение
	:return: None
	"""
	# Срез до названия валюты
	name_currency = call.data[9:]

	# Список валюты у пользователя
	user_currencies = get_user_currencies(call.from_user.id)

	# Если валюта есть в списке пользователя, то удаление
	if name_currency in user_currencies:
		# Удаление валюты пользователя из БД и из списка валют пользователя
		delete_user_currency(name_currency=name_currency, user_telegram_id=call.from_user.id)
		user_currencies.remove(name_currency)
		bot_message = f'✅ «{name_currency}» удалена из списка валют. \n\n'
	else:
		bot_message = f'❌ «{name_currency}» уже нет в вашем списке валют. \n\n'

	if user_currencies:
		# Добавление валют пользователя в виде кнопок
		markup_currencies = get_currencies_buttons(user_currencies)

		bot_message += (
			'Вы можете продолжить удалять валюты.\n\n'
			'Чтобы вернуться к вашему списку валют, нажмите кнопку «Вернуться».'
		)
	else:
		markup_currencies = None
		bot_message += (
			'<b>Ваш список валют пустой.</b>\n\n'
			'Чтобы вернуться к вашему списку валют, нажмите кнопку «Вернуться».'
		)

	bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=bot_message,
		parse_mode='html',
		reply_markup=markup_currencies
	)


@bot.callback_query_handler(func=lambda call: call.data == 'clear')
def clear_callback(call: CallbackQuery) -> None:
	"""
	Перед очисткой сохраненного списка валюты подтверждение пользователя.
	"""
	bot.set_state(call.from_user.id, ChangeUserCurrencies.clear, call.message.chat.id)

	markup_back = add_back_main_button()
	bot.send_message(call.message.chat.id, '➡️ Вы в разделе «Очистить».\n\n', reply_markup=markup_back)

	message_start = (
		'При очистке будет удален весь список валют, позднее их можно будет добавить снова.\n'
		'По кнопке «Вернуться» можно перейти обратно к своему списку валют.\n\n'
	)

	markup = clear_currency_confirm_buttons()
	bot.send_message(
		call.message.chat.id,
		message_start + '❗️ Вы уверены что хотите полностью очистить свой список валют?',
		reply_markup=markup
	)


@bot.callback_query_handler(state=ChangeUserCurrencies.clear, func=lambda call: call.data in ['yes', 'no'])
def clear_confirm_callback(call: CallbackQuery) -> None:
	"""
	Очистка либо отмена очистки сохраненного списка валюты.

	:param call: Сообщение
	:return: None
	"""

	# Выбор сделанный пользователем
	confirm = call.data

	if confirm == 'yes':
		# Если пользователь подтвердил, то полная очистка его списка
		delete_user_currency(user_telegram_id=call.from_user.id, clear=True)
		message = '✅ Список полностью очищен.'
	else:
		message = 'Список не был очищен.'

	message_end = '\n\nПо кнопке «Вернуться» можно перейти обратно к своему списку валют.'

	bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=message + message_end
	)


@bot.callback_query_handler(func=lambda call: call.data == 'add')
def choice_add_callback(call: CallbackQuery) -> None:
	"""
	Вывод списка валют от API с исключением уже добавленных пользователем.

	:param call: Сообщение
	:return: None
	"""
	bot.set_state(call.from_user.id, ChangeUserCurrencies.add, call.message.chat.id)

	# Список валюты пользователя
	user_currencies = get_user_currencies(call.from_user.id)

	# Список валюты от API
	currencies_api_data = get_currencies_api()

	markup_back = add_back_main_button()
	bot.send_message(call.message.chat.id, '➡️ Вы в разделе «Добавить».\n\n', reply_markup=markup_back)

	if len(user_currencies) >= 5:
		bot.send_message(
			call.message.chat.id,
			'❌ Больше 5-ти валют в списке хранить нельзя. '
			'Удалите ненужную из текущего списка, чтобы добавить новую.\n\n'
			'Нажмите кнопку «Вернуться», чтобы перейти обратно к списку.'
		)

		return

	message = 'Список доступных валют для добавления:\n'
	start_sym = ''

	# Вывод всего списка валюты от API
	for name_currency in currencies_api_data:

		# Вывод валюты если его нет в списке пользователя и это не рубли
		if name_currency not in user_currencies and name_currency != 'RUB':

			# Добавление новой строки с первой буквы названия валюты
			if start_sym != name_currency[0]:
				start_sym = name_currency[0]
				message += f'\n<b>{start_sym}</b>: {name_currency}'
			else:
				# Либо просто добавление валюты через запятую
				message += f', {name_currency}'

	message_end = (
		'\n\nНапишите, какую валюту необходимо добавить?\n\n'
		'По кнопке «Вернуться» можно перейти обратно к списку валют.'
	)

	bot.send_message(call.message.chat.id, message + message_end, parse_mode='html')


@bot.message_handler(state=ChangeUserCurrencies.add)
def add(message: Message) -> None:
	"""
	Добавление валюты с API в список валют пользователя.

	:param message: Сообщение
	:return: None
	"""
	name_currency = message.text.upper()
	currencies_api_data = get_currencies_api()
	user_currencies = get_user_currencies(message.from_user.id)

	# Возращение на стартовую страницу по кнопке «Вернуться»
	if name_currency == 'Вернуться'.upper():
		bot.delete_state(message.from_user.id, message.chat.id)
		return back_main_page(message)
	# Проверка добавлена ли уже валюта в список валют пользователя
	elif name_currency in user_currencies:
		bot_message = f'❌ «{name_currency}» уже есть в вашем списке валют!'
	# Хранение не более 5-ти валют в списке
	elif len(user_currencies) >= 5:
		bot_message = f'❌ Больше 5-ти валют нет возможности сохранить.'
	# Проверка, что не введены рубли
	elif name_currency == 'RUB':
		bot_message = f'❌ «{name_currency}» невозможно добавить, так как расчёт ведется в рублях.'
	# Добавление валюты в список пользователя, если эта валюта есть в API
	elif name_currency in currencies_api_data:
		add_currency_user(message.from_user.id, name_currency)
		bot_message = f'✅ «{name_currency}» успешно добавлена в список валют.'
	else:
		bot_message = f'❌ Валюты {name_currency} нет в списке. Попробуйте снова!'

	bot_message_end = (
		'\n\nНапишите какую еще валюту необходимо добавить, '
		'либо вернитесь обратно, нажав кнопку «Вернуться».'
	)
	bot.reply_to(message, bot_message + bot_message_end)
