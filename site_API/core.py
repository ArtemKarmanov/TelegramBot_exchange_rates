import requests

from config_data import config


url = 'https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest'

querystring = {"from": "RUB", "to": "EUR,GBP"}

headers = {
	"X-RapidAPI-Key": config.RAPID_API_KEY,
	"X-RapidAPI-Host": config.RAPID_API_HOST
}

response = requests.get(url, headers=headers, params=querystring)
site_data = response.json()
