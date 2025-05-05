from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot, search_history
from states.user_states import UserInputInfo
from utils.utils_search_movie_by_rating import search_by_rating
from utils.utils_search_movie_by_title import search_by_title
from keyboards.inline.rating_buttons import button_rating


@bot.message_handler(commands=['movie_by_rating'])
def start_movie_by_rating(message: Message) -> None:
    """
    Инициирует поиск фильмов по рейтингу.

    Устанавливает состояние UserInputInfo.input_rating и запрашивает у пользователя
    минимальный рейтинг для поиска.

    Args:
        message (Message): Входящее сообщение с командой

    Actions:
        - Устанавливает состояние input_rating
        - Отправляет инструкцию по формату ввода

    Example:
        Пользователь вводит: /movie_by_rating
        Бот отвечает: "Какой рейтинг? Число от 0.0 до 10.0 (7.0, 8.3)"
    """
    bot.set_state(
        user_id=message.from_user.id,
        state=UserInputInfo.input_rating,
        chat_id=message.chat.id,
    )
    bot.send_message(
        chat_id=message.from_user.id,
        text='Какой рейтинг?\nЧисло от 0.0 до 10.0 (пример: 7, 10, 7.2-10)',
        parse_mode="HTML",
    )


@bot.message_handler(state=UserInputInfo.input_rating)
def first_result(message: Message) -> None:
    """
    Обрабатывает введенный рейтинг и выводит первый результат поиска.

    Args:
        message (Message): Сообщение с рейтингом от пользователя

    Actions:
        - Ищет фильмы с указанным рейтингом
        - Сохраняет результаты в состоянии пользователя
        - Отправляет первый найденный фильм
        - Добавляет запись в историю поиска

    Raises:
        ValueError: Если введен некорректный рейтинг
    """
    try:
        rating = message.text

        for i in map(float, rating.split("-")):
            if not 0.0 <= i <= 10.0:
                raise ValueError("Некорректное число")

        count = 0
        total_list = search_by_rating(rating)

        if not total_list:
            bot.send_message(
                chat_id=message.chat.id,
                text="🔍 Фильмов с таким рейтингом не найдено."
            )
            return

        result = total_list[count]['name']

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data.update({
                'input_name': result,
                'total_list': total_list,
                'count': count,
                'current_rating': rating,
            })

        search_result = search_by_title(result)
        result_text = (
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
            query=f"Рейтинг от {rating}",
            result=f"🎥 {search_result["name"].upper()}",
        )

        bot.send_photo(
            chat_id=message.chat.id,
            photo=search_result['poster_url'],
            caption=result_text,
            parse_mode='HTML',
            reply_markup=button_rating()
        )

    except ValueError as e:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"⚠️ Ошибка: {str(e)}\n"
                 "Пожалуйста, введите число от 0.0 до 10.0"
        )
    except Exception as e:
        print(f"[Ошибка поиска по рейтингу] {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Произошла ошибка при поиске. Попробуйте позже."
        )


@bot.callback_query_handler(func=lambda callback: callback.data == 'r-back')
def back(call) -> None:
    """
    Обработчик кнопки "Назад" для навигации по результатам поиска.

    Args:
        call (CallbackQuery): Объект callback-запроса

    Actions:
        - Получает текущий индекс и список фильмов из состояния
        - Уменьшает индекс на 1 (если возможно)
        - Отображает предыдущий фильм из списка
        - Обновляет состояние
        - Сохраняет в историю просмотров

    Raises:
        KeyError: Если отсутствуют необходимые данные в состоянии
    """
    try:
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        except Exception as delete_error:
            print(f"[Ошибка удаления сообщения] {delete_error}")

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            total_list = data['total_list']
            count = data['count']
            current_rating = data.get('current_rating', 'N/A')

        if len(total_list) == 1:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text="В списке только один фильм",
                show_alert=False,
            )
            return

        if count <= 0:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text="Это первый фильм в списке",
                show_alert=False,
            )
            return

        count -= 1
        result = total_list[count]['name']

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data.update({
                'input_name': result,
                'count': count,
            })

        search_result = search_by_title(result)
        caption = (
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
            user_id=call.from_user.id,
            query=f"Рейтинг от {current_rating}",
            result=f"🎥 {search_result["name"].upper()}",
        )

        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=search_result['poster_url'],
            caption=caption,
            parse_mode='HTML',
            reply_markup=button_rating(),
        )

    except Exception as e:
        print(f"[Ошибка навигации назад] {e}")
        bot.answer_callback_query(
            callback_query_id=call.id,
            text="⚠️ Ошибка при загрузке фильма",
            show_alert=False
        )


@bot.callback_query_handler(func=lambda callback: callback.data == 'r-next')
def next(call) -> None:
    """
    Обработчик кнопки "Вперед" для навигации по результатам поиска.

    Args:
        call (CallbackQuery): Объект callback-запроса

    Actions:
        - Получает текущий индекс и список фильмов из состояния
        - Увеличивает индекс на 1 (если возможно)
        - Отображает следующий фильм из списка
        - Обновляет состояние
        - Сохраняет в историю просмотров

    Raises:
        KeyError: Если отсутствуют необходимые данные в состоянии
    """
    try:
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        except Exception as delete_error:
            print(f"[Ошибка удаления сообщения] {delete_error}")

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            total_list = data['total_list']
            count = data['count']
            current_rating = data.get('current_rating', 'N/A')

        if len(total_list) == 1:
            bot.answer_callback_query(
                call.id,
                text="В списке только один фильм",
                show_alert=False,
            )
            return

        if count >= len(total_list) - 1:
            bot.answer_callback_query(
                callback_query_id=call.id,
                text="Это последний фильм в списке",
                show_alert=False,
            )
            return

        count += 1
        result = total_list[count]['name']

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data.update({
                'input_name': result,
                'count': count,
            })

        search_result = search_by_title(result)
        caption = (
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
            user_id=call.from_user.id,
            query=f"Рейтинг от {current_rating}",
            result=f"🎥 {search_result['name'].upper()}",
        )

        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=search_result['poster_url'],
            caption=caption,
            parse_mode='HTML',
            reply_markup=button_rating(),
        )

    except Exception as e:
        print(f"[Ошибка навигации вперед] {e}")
        bot.answer_callback_query(
            callback_query_id=call.id,
            text="⚠️ Ошибка при загрузке фильма",
            show_alert=False,
        )


@bot.callback_query_handler(func=lambda callback: callback.data == "back_to_menu")
def back_to_menu(call) -> None:
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
    bot.delete_state(
        user_id=call.from_user.id,
        chat_id=chat_id,
    )

    commands_text = '\n'.join(f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS)
    bot.send_message(
        chat_id=chat_id,
        text=f"Основные команды:\n{commands_text}",
    )