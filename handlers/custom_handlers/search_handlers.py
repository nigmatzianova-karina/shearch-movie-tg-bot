from telebot.types import Message
from loader import bot
from states.user_states import UserInputInfo
from utils.utils_search_movie_by_title import search_by_title
from keyboards.inline.back_buttons import button_back
from config_data.config import DEFAULT_COMMANDS
from loader import search_history


@bot.message_handler(commands=['movie_search'])
def movie_search(message: Message) -> None:
    """
    Обработчик команды /movie_search. Инициирует поиск по названию.

    Args:
        message (Message): Объект сообщения от пользователя

    Sets:
        Устанавливает состояние UserInputInfo.input_name
    """
    bot.set_state(message.from_user.id, UserInputInfo.input_name, message.chat.id)
    bot.send_message(
        chat_id=message.from_user.id,
        text='Начинаем <u>поиск</u> по названию!\n'
             'Напишите название фильма или сериала.',
        parse_mode='HTML',
        reply_markup=button_back(),
    )


@bot.message_handler(state=UserInputInfo.input_name)
def find_movie(message: Message) -> None:
    """
    Обработчик поиска фильма по названию.

    Args:
        message (Message): Сообщение с названием фильма

    Returns:
        Отправляет пользователю информацию о найденном фильме
    """
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['input_name'] = message.text
            search_result = search_by_title(data["input_name"])

        result = str(
            f'🎥 <b>{search_result["name"].upper()}</b>\n\n'
            f'⭐ Рейтинг Кинопоиск: <b>{search_result["KP"]}</b>\n'
            f'⭐ Рейтинг IMDb: <b>{search_result["IMDb"]}</b>\n\n'
            f'📅 Год: <b>{search_result["year"]}</b>\n'
            f'🎭 Жанры: <b>{", ".join(search_result["genres"])}</b>\n'
            f'🌍 Страна: <b>{", ".join(search_result["countries"])}</b>\n'
            f'🔞 Возраст: <b>{search_result["ageRating"]}+</b>\n\n'
            f'📝 <b>Описание:</b>\n{search_result["description"]}'
        )

        search_history.add_record(
            user_id=message.from_user.id,
            query=data['input_name'],
            result=f"🎥 {search_result["name"].upper()}",
        )

        bot.send_photo(
            message.chat.id,
            search_result['poster_url'],
            caption=result,
            parse_mode='HTML',
            reply_markup=button_back(),
        )

    except Exception as e:
        print(f"[Ошибка поиска по названию] {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Произошла ошибка при поиске. Попробуйте позже."
        )


@bot.callback_query_handler(func=lambda callback: callback.data == "back_to_menu")
def back_to_menu(call):
    """
    Обработчик кнопки возврата в главное меню.

    Функция:
    1. Сбрасывает текущее состояние пользователя
    2. Отображает список доступных команд бота

    Args:
        call (CallbackQuery): Объект callback-запроса от кнопки

    Actions:
        - Удаляет состояние пользователя (delete_state)
        - Отправляет список команд из DEFAULT_COMMANDS
    """
    chat_id = call.message.chat.id
    bot.delete_state(chat_id)

    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(
        chat_id=chat_id,
        text=f"Основные команды:\n{"\n".join(text)}"
    )
