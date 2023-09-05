import datetime
import os

from loader import bot
from telebot.types import Message, CallbackQuery
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData

import matplotlib as mpl
import matplotlib.pyplot as plt

from utils.database.get_currencies import get_user_currencies
from utils.database.add_history import add_user_history
from utils.site_API.get_currencies_API import get_period_currencies_api, get_value_currency_api
from utils.site_API.get_date import transform_date_format
from keyboards.inline.get_currencies import get_currencies_buttons
from keyboards.reply.back_main import edit_currencies_button, add_back_main_custom_button, remove_back_main_button
from states.custom_states import PeriodCurrency

# Добавление календаря
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_callback = CallbackData('calendar', 'action', 'year', 'month', 'day')


@bot.message_handler(state='*', commands=['custom'])
def set_start_date(message: Message) -> None:
	"""
	Составление графика с периодом дат определенной валюты. Ввод начальной даты.

	:param message: Сообщение пользователя
	:return: None
	"""
	bot.set_state(message.from_user.id, PeriodCurrency.start_date, message.chat.id)
	add_user_history(message.from_user.id, 'Составления графика курса валюты с периодом (/custom).')

	# Проверка, что есть сохраненный список валют
	user_currencies = get_user_currencies(message.from_user.id)
	if not user_currencies:
		bot.send_message(
			message.chat.id,
			'С пустым списком ничего не смогу посчитать 🤔.\n'
			'Добавьте в ваш список какую-либо валюту нажав на кнопку «Изменить список валюты».',
			reply_markup=edit_currencies_button()
		)

	else:
		now = datetime.datetime.now()

		bot.send_message(
			message.chat.id,
			'Я могу вывести значение курса валюты за выбранный период в виде графика.\n'
			'Максимальный допустимый период 365 дней.\n'
			'Для этого нужно ввести дату начала, дату конца и выбрать валюту из сохраненного списка.\n\n',
			reply_markup=remove_back_main_button()
		)

		# Вызов markup календаря
		bot.send_message(
			message.chat.id,
			'Введите начальную дату, чтобы продолжить.',
			reply_markup=calendar.create_calendar(
				name=calendar_callback.prefix,
				year=now.year,
				month=now.month
			)
		)


@bot.message_handler(state='*', func=lambda message: message.text == 'Вернуться к выбору периода')
def back_main_page(message: Message) -> None:
	"""
	Возврат на стартовую страницу при нажатии на кнопку «Вернуться к выбору периода».
	"""

	bot.delete_state(message.from_user.id, message.chat.id)
	add_user_history(message.from_user.id, 'Возвращение к выбору периода при составлении графика.')

	set_start_date(message)


@bot.callback_query_handler(state='*', func=lambda call: call.data.startswith(calendar_callback.prefix))
def set_date_callback(call: CallbackQuery) -> None:
	"""
	Календарь с выбором начальной и конечной дат.

	:param call: Нажатие на кнопку даты в календаре.
	:return: None
	"""
	name, action, year, month, day = call.data.split(calendar_callback.sep)
	date = calendar.calendar_query_handler(
		bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
	)

	# При нажатии на кнопку дня в календаре
	if action == "DAY":
		user_state = bot.get_state(call.from_user.id, call.message.chat.id)
		# Введенная дата
		set_date = date.strftime('%d.%m.%Y')

		# Если состояние пользователя на начальной дате
		if user_state == str(PeriodCurrency.start_date):
			bot.send_message(
				chat_id=call.from_user.id,
				text=f'Вы указали начальную дату {set_date}.',
				reply_markup=remove_back_main_button(),
			)

			add_user_history(
				call.from_user.id,
				f'Указана начальная дата {set_date} для графика курса валюты.'
			)

			with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
				now_date = datetime.datetime.now()
				start_date = datetime.datetime.strptime(set_date, '%d.%m.%Y')

				# Начальная дата не может быть позже текущей
				if start_date >= now_date:
					bot.send_message(
						call.message.chat.id,
						f'Начальная дата не может быть позже текущей либо равна ей!\n'
						f'Вы указали {set_date}. Попробуйте снова.'
					)

				else:
					# Сохранение начальной даты у пользователя
					data['start_date'] = set_date

					set_end_date(call)
		# Если состояние пользователя на конечной дате
		elif user_state == str(PeriodCurrency.end_date):

			with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
				# Перевод дат в формат datetime, чтобы сравнивать
				now_date = datetime.datetime.now()
				start_date = datetime.datetime.strptime(data['start_date'], '%d.%m.%Y')
				end_date = datetime.datetime.strptime(set_date, '%d.%m.%Y')
				max_days = datetime.timedelta(days=365)

				# Конечная дата не может быть раньше начальной
				if start_date >= end_date:
					bot.send_message(
						chat_id=call.message.chat.id,
						text=
						f'Конечная дата должна быть позже начальной и не равна ей! '
						f'Вы указали {set_date}. Попробуйте снова.'
					)

					set_end_date(call)
				# Максимальное количество дней между датами 365 дней
				elif abs(end_date - start_date) > max_days:
					bot.send_message(
						chat_id=call.message.chat.id,
						text=f'Между датами не может быть больше 365 дней! Вы указали {set_date}. Попробуйте снова.'
					)

					set_end_date(call)
				# Конечная дата не может быть больше либо равен текущей дате
				elif end_date >= now_date:
					bot.send_message(
						chat_id=call.message.chat.id,
						text=
						f'Конечная дата не может быть позже текущей или равна ей! '
						f'Вы указали {set_date}. Попробуйте снова.'

					)

					set_end_date(call)
				else:
					add_user_history(
						call.from_user.id,
						f'Указана конечная дата {set_date} для графика курса валюты.'
					)

					bot.send_message(
						chat_id=call.from_user.id,
						text=f'Вы указали конечную дату {set_date}.',
						reply_markup=remove_back_main_button(),
					)
					# Сохранение конечной даты у пользователя
					data['end_date'] = set_date

					choose_currency(call)


@bot.callback_query_handler(state=PeriodCurrency.start_date, func=lambda call: call.data)
def set_end_date(call: CallbackQuery) -> None:
	"""
	Ввод конечной даты периода.

	:param call: Вызов после выбора начальной даты
	:return: None
	"""
	bot.set_state(call.from_user.id, PeriodCurrency.end_date, call.message.chat.id)

	add_user_history(call.from_user.id, 'Составления графика с периодом, ввод конечной даты.')
	now = datetime.datetime.now()

	# Вызов markup календаря
	bot.send_message(
		call.message.chat.id,
		'Введите дату окончания.',
		reply_markup=calendar.create_calendar(
			name=calendar_callback.prefix,
			year=now.year,
			month=now.month
		)
	)


@bot.callback_query_handler(state=PeriodCurrency.end_date, func=lambda call: call.data)
def choose_currency(call: CallbackQuery) -> None:
	"""
	Выбор валюты из сохраненного списка пользователя.

	:param call: Сообщение
	:return: None
	"""
	bot.set_state(call.from_user.id, PeriodCurrency.currency, call.message.chat.id)
	add_user_history(call.from_user.id, 'Составления графика с периодом, выбор валюты из списка.')

	# Список валюты пользователя
	user_currencies = get_user_currencies(call.from_user.id)

	# Добавляем кнопку на каждую валюту
	markup = get_currencies_buttons(user_currencies)

	bot.send_message(
		call.message.chat.id,
		'Выберите валюту из вашего сохраненного списка, чтобы продолжить.\n\n',
		reply_markup=markup
	)

	# Кнопка возврата к выбору периода и кнопка к изменению списка валют
	markup_edit_currencies = add_back_main_custom_button()
	bot.send_message(
		call.message.chat.id,
		'Чтобы сделать изменения в вашем списке валют, нажмите кнопку «Изменить список валют».\n'
		'Если хотите изменить период, нажмите кнопку «Вернуться к выбору периода».',
		reply_markup=markup_edit_currencies
	)


@bot.callback_query_handler(state=PeriodCurrency.currency, func=lambda call: call.data.startswith('currency_'))
def period_currency(call: CallbackQuery) -> None:
	"""
	Вывод курса выбранной валюты за указанный период.

	:param call: Сообщение
	:return: None
	"""
	# Берем название валюты
	name_currency = call.data[9:]

	bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f'Вы выбрали валюту «{name_currency}».'
	)

	# Инициализация графика
	fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')

	with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
		add_user_history(
			call.from_user.id,
			f'Составления графика валюты {name_currency} с {data["start_date"]} по {data["end_date"]}.'
		)
		# Установка заголовка графика
		ax.set_title(f'Курс «{name_currency}» с {data["start_date"]} по {data["end_date"]}')

		# Изменение формата в вид для API
		data['start_date'] = transform_date_format(value=data['start_date'])
		data['end_date'] = transform_date_format(value=data['end_date'])

		# Данные по датам от API
		period_data = get_period_currencies_api(start_date=data['start_date'], end_date=data['end_date'])

	# Список значений по x и y
	dates_x = []
	values_y = []
	# Берем значение рубля
	value_rub = get_value_currency_api('RUB')

	# Фильтрация по данным от API
	for date, currencies in period_data.items():
		# Добавление даты в список
		dates_x.append(mpl.dates.datestr2num(date))
		# Добавление курса валюты в список, если имя совпало
		for currency, value in currencies.items():
			if currency == name_currency:
				value = round(float(value_rub) / float(value), 2)
				values_y.append(value)
				break

	# Добавление сетки
	ax.grid(True)

	# Добавление данных для графика
	ax.plot(dates_x, values_y)

	cdf = mpl.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
	ax.xaxis.set_major_formatter(cdf)

	# Путь и название изображения для графика
	path = f'uploads/custom/user_{call.from_user.id}/'
	name_file = 'custom_result.png'

	# Если директория не существует, то создаем её
	if not os.path.isdir(path):
		os.mkdir(path)

	# Сохраняем фигуру в виде файла
	fig.savefig(f'{path}{name_file}', dpi=200)

	# Открываем файл для отправки пользователю
	photo = open(f'{path}{name_file}', 'rb')

	# Отправка графика пользователю
	bot.send_photo(call.message.chat.id, photo)

	bot.delete_state(call.from_user.id, call.message.chat.id)
