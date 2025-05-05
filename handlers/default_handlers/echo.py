from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def echo(message: Message) -> None:
    """
    Эхо-обработчик для сообщений без состояния.

    Args:
        message (Message): Входящее сообщение от пользователя

    Description:
        - Перехватывает любые текстовые сообщения без состояния
        - Возвращает эхо-ответ с полученным текстом
        - Используется для обработки сообщений, не попавших в другие обработчики
    """
    bot.reply_to(
        message,
        "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}",
    )
