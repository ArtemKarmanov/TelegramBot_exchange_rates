from loader import bot
from telebot.types import Message

from keyboards.reply.back_main import edit_currencies_button
from utils.site_API.get_currencies_API import get_value_currency_api
from utils.site_API.get_date import get_datetime_now_api
from utils.database.get_currencies import get_user_currencies
from utils.database.add_history import add_user_history
from states.custom_states import GetCurseNow


@bot.message_handler(state='*', commands=['low'])
def output_course_now(message: Message) -> None:
	"""
	Вывод курса валют на текущий момент.
	"""
	bot.set_state(message.from_user.id, GetCurseNow.now, message.chat.id)
	add_user_history(message.from_user.id, f'Вывод курса валют на текущий момент (/low).')

	bot_message = f'💰 Текущий курс валют на {get_datetime_now_api()}\n\n'

	# Проверяем наличие списка валют пользователя
	user_currencies = get_user_currencies(message.from_user.id)

	# Если список есть, то выводим текущий курс
	if user_currencies:
		# Берем валюту со значениями от API
		currencies_api_data = get_value_currency_api(user_currencies)
		value_rub = get_value_currency_api('RUB')

		for currency, value in currencies_api_data.items():
			# Расчёт курса валюты в зависимости от рубля
			result = round(float(value_rub) / float(value), 2)
			# Добавление валюты в сообщение
			bot_message += f'➡️ 1 {currency} — {str(result)} р.\n'

	else:
		# Предлагаем добавить валюту, если список пуст
		bot_message = (
			'У вас пустой список с валютами, я ничего не смогу посчитать 😢\n'
		)

	# Добавление кнопки на редактирование списка валют пользователя
	markup = edit_currencies_button()

	bot_end_msg = (
		'\nЧтобы обновить свой список валюты, нажмите на кнопку «Изменить список валюты».\n'
		'Там можно будет добавить и удалить валюту из списка либо очистить весь список.')

	bot.send_message(message.chat.id, bot_message + bot_end_msg, parse_mode='html', reply_markup=markup)
