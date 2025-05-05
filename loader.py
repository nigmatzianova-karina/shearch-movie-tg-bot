"""
Модуль инициализации бота и зависимостей.

Инициализирует:
- Бота с хранилищем состояний (StateMemoryStorage)
- Историю поиска (SearchHistory) с подключением к SQLite
- Кастомные фильтры для FSM
"""
import os
from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from config_data import config
from database.search_history import SearchHistory


search_history = SearchHistory(
    db_path=os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'search_history.db'
    )
)

storage = StateMemoryStorage()
bot = TeleBot(
    token=config.BOT_TOKEN,
    state_storage=storage
)

bot.add_custom_filter(custom_filters.StateFilter(bot))
