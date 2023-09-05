import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
)
CUSTOM_COMMANDS = (
    ("currencies", "Изменить список валют"),
    ("low", "Посмотреть текущий курс"),
    ("high", "Рассчитать свои средства по курсу"),
    ("custom", "Вывести курс за период"),
    ("history", "История запросов"),
)
