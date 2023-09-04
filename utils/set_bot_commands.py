from telebot import TeleBot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    """
    Все базовые команды бота.

    :param bot: Бот
    :return: None
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


def set_custom_commands(bot: TeleBot) -> None:
    """
    Добавление кастомных команд для бота.

    :param bot: Бот
    :return: None
    """
    bot.set_my_commands = (
        [BotCommand(*i) for i in CUSTOM_COMMANDS])
