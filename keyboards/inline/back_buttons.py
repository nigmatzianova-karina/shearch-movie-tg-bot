from telebot import types


def button_back():
    """
    Создает inline-клавиатуру с одной кнопкой для возврата в главное меню.

    Returns:
        InlineKeyboardMarkup: Объект клавиатуры с кнопкой "Назад в меню"
    """
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Назад в меню', callback_data='back_to_menu')
    )
    return keyboard
