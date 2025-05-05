from telebot import types


def buttons_history():
    """
    Создает inline-клавиатуру с двумя кнопками действий:
        - Отчистка истории поиска
        - Закрытие действия (возврат в главное меню)

    Returns:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками действий.
    """
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Очистить историю', callback_data='clear_history'),
        types.InlineKeyboardButton(text='Закрыть', callback_data='close_history'),
    )
    return keyboard
