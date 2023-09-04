from telebot.types import Message
from loader import bot

from utils.database.get_user import get_or_create_user


@bot.message_handler(state='*', commands=["start"])
def bot_start(message: Message) -> None:
    """
    Прием команды /start. Создает пользователя в базе данных, если ранее не был создан.

    :param message: Данные message
    :return: None
    """
    # Прием имени и id телеграмма пользователя.
    user_name = message.from_user.full_name
    user_telegram_id = message.from_user.id

    # Регистрация пользователя, если ранее аккаунт не был создан.
    register = get_or_create_user(user_name, user_telegram_id)

    if register:
        # Приветствие бота при первой регистрации пользователя.
        bot.reply_to(
            message,
            f"Добро пожаловать в менеджер курса валют, {user_name}!\n"
            f"Я умею отслеживать актуальный курс и могу подсчитывать конвертацию "
            f"из рублей в любые выбранные валюты.\n"
            f"Для подробного описания моих возможностей напишите /help"
        )
    else:
        # Приветствие уже зарегистрированного пользователя.
        bot.reply_to(message, f"Рад вас снова видеть, {user_name}!")
