from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def help(message: Message) -> None:
    """
    Обработчик команды /help. Показывает список доступных команд.

    Args:
        message (Message): Объект сообщения от пользователя

    Description:
        - Формирует список команд из DEFAULT_COMMANDS
        - Отправляет пользователю форматированное сообщение
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Основные команды:\n{"\n".join(text)}",
    )
