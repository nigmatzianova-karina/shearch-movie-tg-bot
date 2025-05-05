from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["start"])
def start(message: Message):
    """
    Обработчик команды /start. Приветствует пользователя и показывает список доступных команд.

    Args:
        message (Message): Объект сообщения от пользователя

    Description:
        - Приветствует пользователя
        - Формирует список команд из DEFAULT_COMMANDS
        - Отправляет пользователю форматированное сообщение
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Привет, {message.from_user.full_name}!\n"
             f"Я, SEARCH_MOVIE_BOT, помогу тебе в поиске фильма или сериала на вечер!\n\n"
             f"Основные команды:\n"
             f"{"\n".join(text)}",
    )
