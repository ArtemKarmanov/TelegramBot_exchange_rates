from telebot.types import Message
from loader import bot

from utils.database.person import new_person


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Прием команды /start. Создает пользователя в базе данных, если его там нет.

    :param message: данные message
    :return: bot.reply_to(message, f"Привет, {user_name}!")
    """
    name = message.from_user.full_name
    telegram_id = message.from_user.id

    new_person(name, telegram_id)

    bot.reply_to(message, f"Привет, {name}!")
