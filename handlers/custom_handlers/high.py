from telebot.types import Message

from loader import bot

from keyboards.reply.back_main import edit_currencies_button
from utils.database.get_currencies import get_user_currencies
from utils.database.add_history import add_user_history
from utils.site_API.get_currencies_API import get_value_currency_api
from utils.site_API.get_date import get_datetime_now_api
from states.custom_states import CalculationWallet


@bot.message_handler(state='*', commands=['high'])
def set_wallet(message: Message) -> None:
	"""
	Ввод кол-ва средств, которые необходимо рассчитать по текущему курсу.

	:param message: Сообщение
	:return: None
	"""
	bot.set_state(message.from_user.id, CalculationWallet.calculate, message.chat.id)
	add_user_history(message.from_user.id, f'Ввод средств для расчёта по курсу (/high).')

	user_currencies = get_user_currencies(message.from_user.id)

	if user_currencies:
		bot.send_message(message.chat.id, 'Введите сумму в рублях, которую необходимо перевести в курс валют.')
	else:
		bot.send_message(
			message.chat.id,
			'У вас пустой список с валютами, я ничего не смогу посчитать 😢'
			'\n\nЧтобы обновить свой список валюты, нажмите на кнопку «Изменить список валюты».\n'
			'Там можно будет добавить и удалить валюту из списка либо очистить весь список.'
		)


@bot.message_handler(state=CalculationWallet.calculate, func=lambda message: Message)
def calculation(message: Message) -> None:
	"""
	Вывод результата расчёта.

	:param message: Сообщение
	:return: None
	"""

	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		# Цикличный запрос на ввод суммы, если введены не только цифры
		if not message.text.isdigit():
			add_user_history(message.from_user.id, f'Попытка расчёта «{message.text}».')
			bot.reply_to(
				message,
				'❌ В сумме присутствуют буквы либо символы. Необходимо ввести сумму только цифрами.\n'
				'Попробуйте ввести снова!'
			)
			return
		# Сохранение введённой суммы пользователем
		data['amount'] = message.text

	add_user_history(message.from_user.id, f'Расчёт суммы {message.text} руб.')

	bot.send_message(
		message.chat.id,
		f'💰 Расчёт по текущему курсу валют на {get_datetime_now_api()}'
	)
	bot_message = f'Вы ввели <u>{message.text} руб</u>. В других валютах это будет:\n\n'
	bot_end_msg = (
		f'\nВведите новую сумму, если необходимо сделать новый расчёт.\n\n'
		'Либо обновите список валюты нажав на кнопку «Изменить список валюты».\n'
		'Там можно будет добавить и удалить валюту из списка либо очистить весь список 😉'
	)

	# Проверяем наличие списка валют пользователя
	user_currencies = get_user_currencies(message.from_user.id)

	# Если список есть, то выводим текущий курс
	if user_currencies:
		# Берем валюту со значениями от API
		currencies_api_data = get_value_currency_api(user_currencies)
		value_rub = get_value_currency_api('RUB')

		for currency, value in currencies_api_data.items():
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				# Расчёт введенной суммы по курсу валюты
				result = round(float(data['amount']) / (float(value_rub) / (float(value))), 2)
			# Добавление результата в сообщение
			bot_message += f'➡️ <b>{currency}</b> — {str(result)}\n'
	else:
		# Предлагаем добавить валюту, если список пуст
		bot_message = 'Ваш список сохраненных валют пуст.'
		bot_end_msg = (
			'\nС пустым списком ничего не смогу посчитать 🤔.\n'
			'Добавьте в ваш список какую-либо валюту нажав на кнопку «Изменить список валюты».'
		)

	markup = edit_currencies_button()

	bot.send_message(message.chat.id, bot_message + bot_end_msg, reply_markup=markup, parse_mode='html')
