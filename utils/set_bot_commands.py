from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot) -> None:
    """
    Устанавливает стандартные команды для бота.

    Args:
        bot: Экземпляр телеграм-бота
        DEFAULT_COMMANDS (List[Tuple[str, str]]): Список команд в формате
            [("command", "description"), ...]

    Example:
        DEFAULT_COMMANDS = [
            ("start", "Запустить бота"),
            ("help", "Помощь по командам")
        ]
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
