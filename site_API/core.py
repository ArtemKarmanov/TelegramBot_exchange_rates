import json

import requests
from requests import Response

from config_data import config


BASE_URL = 'https://currency-conversion-and-exchange-rates.p.rapidapi.com'

headers = {
	"X-RapidAPI-Key": config.RAPID_API_KEY,
	"X-RapidAPI-Host": config.RAPID_API_HOST
}


def get_latest_datetime_currencies() -> Response:
	"""
	Запрос текущего курса валют.

	:return: response
	"""
	url = f'{BASE_URL}/latest'
	querystring = dict()
	response = requests.get(url, headers=headers, params=querystring)

	return response


def get_period_date_currencies(start_date: str, end_date: str) -> json:
	"""
	Запрос курса валют за период.

	:param start_date: Начальная дата
	:param end_date: Конечная дата
	:return: response.json()
	"""
	url = f'{BASE_URL}/timeseries'
	querystring = {"start_date":start_date,"end_date":end_date}
	response = requests.get(url, headers=headers, params=querystring)

	return response.json()


latest_response = get_latest_datetime_currencies()
get_latest_api = latest_response.json()
