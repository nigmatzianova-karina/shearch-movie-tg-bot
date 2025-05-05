from telebot import types


def button_rating():
    """
    Создает inline-клавиатуру с тремя кнопками действий:
        - Предыдущий результат
        - Следующий результат
        - Возврат в главное меню

    Returns:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками действий.
    """
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='<-', callback_data='r-back'),
        types.InlineKeyboardButton(text='->', callback_data='r-next'),
        types.InlineKeyboardButton(text='Back to menu', callback_data="back_to_menu"),
    )
    return keyboard
