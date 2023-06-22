from loader import bot

import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from database.common.models import db, Person, Currency

if __name__ == "__main__":
    db.create_tables([Person, Currency])
    set_default_commands(bot)
    bot.infinity_polling()
