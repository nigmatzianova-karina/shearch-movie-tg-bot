from telebot.handler_backends import State, StatesGroup


class UserInputInfo(StatesGroup):
    """
    Класс состояний пользователя для FSM (Finite State Machine).
    Определяет возможные состояния бота при взаимодействии с пользователем.

    States:
        input_name: Состояние ввода названия фильма для поиска
        input_rating: Состояние ввода рейтинга для фильтрации
        input_budget: Состояние ввода бюджета для фильтрации

    Usage:
        Устанавливается через bot.set_state() и обрабатывается соответствующими хендлерами
    """
    input_name = State()
    input_rating = State()
    input_budget = State()
