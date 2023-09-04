from telebot.types import Message
from loader import bot

from utils.database.add_history import add_user_history


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    add_user_history(message.from_user.id, f'Вызов неизвестной команды «{message.text}».')

    bot.reply_to(
        message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}."
    )
