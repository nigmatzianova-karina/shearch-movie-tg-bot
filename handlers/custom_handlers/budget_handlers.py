from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from keyboards.inline.budget_buttons import button_budget
from loader import bot, search_history
from states.user_states import UserInputInfo
from utils.utils_search_movie_by_budget import search_by_budget
from utils.utils_search_movie_by_title import search_by_title


@bot.message_handler(commands=['movie_by_budget'])
def start_movie_by_budget(message: Message) -> None:
    """
    Инициирует поиск фильмов по бюджету.

    Устанавливает состояние UserInputInfo.input_budget и запрашивает у пользователя
    минимальный бюджет для поиска.

    Args:
        message (Message): Входящее сообщение с командой

    Actions:
        - Устанавливает состояние input_budget
        - Отправляет инструкцию по формату ввода

    Example:
        Пользователь вводит: /movie_by_budget
        Бот отвечает: "Начинаем поиск по бюджету фильма!\n Какой бюджет?\n(пример: 1000-6666666)"
    """
    bot.set_state(
        user_id=message.from_user.id,
        state=UserInputInfo.input_budget,
        chat_id=message.chat.id,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text='Начинаем поиск по бюджету фильма!\nКакой бюджет?\n(пример: 1000-6666666)',
        parse_mode='HTML',
    )


@bot.message_handler(state=UserInputInfo.input_budget)
def first_result(message: Message) -> None:
    """
    Обрабатывает введенный бюджет и выводит первый результат поиска.

    Args:
        message (Message): Сообщение с диапазоном бюджета в формате "min-max"

    Actions:
        - Ищет фильмы в указанном бюджете
        - Сохраняет результаты в состоянии пользователя
        - Отправляет первый найденный фильм
        - Добавляет запись в историю поиска

    Raises:
        ValueError: Если введен некорректный формат бюджета
    """
    try:
        count = 0
        budget_range = message.text.strip()

        if '-' not in budget_range:
            raise ValueError("Используйте формат 'min-max', например: '1000000-5000000'")

        total_list = search_by_budget(budget_range)

        if not total_list:
            bot.send_message(
                chat_id=message.chat.id,
                text="🔍 Фильмов с таким бюджетом не найдено."
            )
            return

        result = total_list[count]['name']

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data.update({
                'input_name': result,
                'total_list': total_list,
                'count': count,
                'budget_range': budget_range,
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
            user_id=message.from_user.id,
            query=f"Бюджет: {budget_range}",
            result=f"🎥 {search_result["name"].upper()}",
        )

        bot.send_photo(
            chat_id=message.chat.id,
            photo=search_result['poster_url'],
            caption=caption,
            parse_mode='HTML',
            reply_markup=button_budget(),
        )

    except ValueError as e:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"⚠️ Ошибка: {str(e)}\n"
                 "Пожалуйста, введите бюджет в формате 'min-max'"
        )
    except Exception as e:
        print(f"[Ошибка поиска по бюджету] {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Произошла ошибка при поиске. Попробуйте позже."
        )


@bot.callback_query_handler(func=lambda callback: callback.data == 'b-back')
def back(call) -> None:
    """
    Обработчик кнопки "Назад" для навигации по результатам поиска по бюджету.

    Args:
        call (CallbackQuery): Объект callback-запроса

    Actions:
        - Получает текущий индекс и список фильмов из состояния
        - Уменьшает индекс на 1 (если возможно)
        - Отображает предыдущий фильм из списка
        - Обновляет состояние
        - Сохраняет в историю просмотров
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
            budget_range = data.get('budget_range', 'N/A')

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
            query=f"Бюджет: {budget_range}",
            result=f"🎥 {search_result["name"].upper()}",
        )

        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=search_result['poster_url'],
            caption=caption,
            parse_mode='HTML',
            reply_markup=button_budget(),
        )

    except Exception as e:
        print(f"[Ошибка навигации назад] {e}")
        bot.answer_callback_query(
            call.id,
            text="⚠️ Ошибка при загрузке фильма",
            show_alert=False
        )


@bot.callback_query_handler(func=lambda callback: callback.data == 'b-next')
def next(call) -> None:
    """
    Обработчик кнопки "Вперед" для навигации по результатам поиска по бюджету.

    Args:
        call (CallbackQuery): Объект callback-запроса

    Actions:
        - Получает текущий индекс и список фильмов из состояния
        - Увеличивает индекс на 1 (если возможно)
        - Отображает следующий фильм из списка
        - Обновляет состояние
        - Сохраняет в историю просмотров
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
            budget_range = data.get('budget_range', 'N/A')

        if len(total_list) == 1:
            bot.answer_callback_query(
                callback_query_id=call.id,
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
            query=f"Бюджет: {budget_range}",
            result=f"🎥 {search_result["name"].upper()}",
        )

        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=search_result['poster_url'],
            caption=caption,
            parse_mode='HTML',
            reply_markup=button_budget(),
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
