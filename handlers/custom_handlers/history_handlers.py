from loader import search_history, bot
from telebot.types import Message
from keyboards.inline.history_buttons import buttons_history
from config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=['history'])
def show_history(message: Message):
    """
    Показывает историю поисковых запросов пользователя.

    Получает историю поиска из базы данных и отображает её в формате:
    1. [Запрос] -> [Результат]
       ⏱ [Время поиска]

    Args:
        message (Message): Входящее сообщение с командой /history

    Actions:
        - Получает историю поиска для текущего пользователя
        - Форматирует результаты в читаемый вид
        - Отправляет список или сообщение об отсутствии истории
    """
    history = search_history.get_history(message.from_user.id)
    if not history:
        bot.send_message(message.chat.id, text="История поиска пустая.")
        return

    response = "История поиска: \n\n"
    for idx, (query, result, timestamp) in enumerate(history, 1):
        response += f"{idx}. Твой запрос: {query}\n -> {result}\n⏱ {timestamp}\n\n"

    bot.send_message(
        message.chat.id,
        response,
        reply_markup=buttons_history(),
    )


@bot.callback_query_handler(func=lambda callback: callback.data == "clear_history")
def clear_history(call):
    """
    Обработчик кнопки очистки истории.
    Очищает историю поиска пользователя.

    Args:
        call (CallbackQuery): Объект callback-запроса от кнопки

    Actions:
        - Очищает историю поиска
        - Отправляет уведомление о сделанном действии
    """
    search_history.clear_history(call.from_user.id)
    bot.answer_callback_query(
        call.id,
        "История очищена"
    )


@bot.callback_query_handler(func=lambda callback: callback.data == "close_history")
def close_history(call):
    """
    Обработчик кнопки возврата в главное меню.
    Отображает список доступных команд бота.

    Args:
        call (CallbackQuery): Объект callback-запроса от кнопки

    Actions:
        - Отправляет список команд из DEFAULT_COMMANDS
    """
    chat_id = call.message.chat.id
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(
        chat_id=chat_id,
        text=f"Основные команды:\n{"\n".join(text)}"
    )
