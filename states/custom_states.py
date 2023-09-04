from telebot.handler_backends import State, StatesGroup


class ChangeUserCurrencies(StatesGroup):
	"""
	Состояния для изменения списка валют пользователя.
	"""
	today = State()
	add = State()
	delete = State()
	clear = State()
	back_main = State()


class GetCurseNow(StatesGroup):
	"""
	Состояния для вывода текущего курса.
	"""
	now = State()


class CalculationWallet(StatesGroup):
	"""
	Состояния для расчёта суммы по курсу валют пользователя.
	"""
	calculate = State()


class PeriodCurrency(StatesGroup):
	"""
	Состояния для курса валюты за период.
	"""
	start_date = State()
	set_date = State()
	end_date = State()
	currency = State()
	result = State()
