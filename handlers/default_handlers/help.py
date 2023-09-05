from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS
from loader import bot

from utils.database.add_history import add_user_history


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    """
    Вывод справки по всем командам по команде /help.

    :param message: Сообщение
    :return: None
    """
    add_user_history(message.from_user.id, f'Запрос справки (/help).')

    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    text.extend([f"/{command} - {desk}" for command, desk in CUSTOM_COMMANDS])
    bot.reply_to(message, "\n".join(text))
