from loader import bot, custom_filters
import handlers  # noqa
from utils.set_bot_commands import set_default_commands

"""
Главный модуль бота. Запускает polling и регистрирует обработчики.
Точка входа — `if __name__ == "__main__"`.
"""

if __name__ == "__main__":
    set_default_commands(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
