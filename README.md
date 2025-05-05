## Описание проекта
Telegram-бот для поиска фильмов по различным критериям: названию, рейтингу и бюджету. 
Также сохраняет историю поиска пользователей.

### Как пользоваться
1. movie_search — поиск фильма/сериала по названию
2. movie_by_rating — поиск фильмов/сериалов по рейтингу
3. movie_by_budget — поиск фильмов/сериалов по бюджету
4. history — возможность просмотра истории запросов и поиска фильма/сериала


#### custom command:

**/movie_search** - поиск фильма/сериала по названию

![img_3.png](imgs for readme/img_3.png)

Запрос с параметрами:

CURL POST https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query=

Пример ответ запроса:

```console
{
  "docs": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "description": "string",
      "poster": {
        "url": "string",
      },
      "rating": {
        "kp": 6.2,
      },
      "genres": [
        {
          "name": "string"
        }
      ],
      "countries": [
        {
          "name": "string"
        }
      ],
      "ageRating": 0,
    }
  ],
  "total": 0,
  "limit": 0,
  "page": 0,
  "pages": 0
}
```

**/movie_by_rating** — поиск фильмов/сериалов по рейтингу

![img_4.png](imgs for readme/img_4.png)

Запрос с параметрами:

CURL POST 'https://api.kinopoisk.dev/v1.4/movie?page=1&limit=100&selectFields=name&notNullFields=name&notNullFields=description&notNullFields=year&notNullFields=rating.kp&notNullFields=rating.imdb&notNullFields=ageRating&notNullFields=genres.name&notNullFields=countries.name&notNullFields=poster.url&sortField=rating.kp&sortType=1&rating.kp='

Ответ запроса:
```
{
  "docs": [
    {
        "name": "Человек паук",
    }, 
    {
        "name": "Человек паук 2"
    },
  ],
  "total": 2,
  "limit": 2,
  "page": 1,
  "pages": 1
}
```

**/movie_by_budget** — поиск фильмов/сериалов по бюджету

![img.png](imgs for readme/img_5.png)

Запрос с параметрами:
CURL POST 'https://api.kinopoisk.dev/v1.4/movie?page=1&limit=100&selectFields=name&notNullFields=name&notNullFields=description&notNullFields=year&notNullFields=rating.kp&notNullFields=rating.imdb&notNullFields=ageRating&notNullFields=genres.name&notNullFields=countries.name&notNullFields=poster.url&sortField=budget.value&sortType=1&budget.value='

Ответ запроса:
```
{
  "docs": [
    {
        "name": "Человек паук",
    }, 
    {
        "name": "Человек паук 2"
    },
  ],
  "total": 2,
  "limit": 2,
  "page": 1,
  "pages": 1
}
```

**/history** — возможность просмотра истории запросов и поиска фильма/сериала

![img.png](imgs for readme/img_6.png)

Без запроса к API


#### default command:

**/start** - старт, приветствует пользователя, отправляет список доступных команд

![img_1.png](imgs for readme/img_1.png)

**/help** - помощь, отправляет сообщение со списком доступных команд

![img_2.png](imgs for readme/img_2.png)

### Как запустить
1. Клонирование репозитория
```commandline
git clone https://github.com/karina_nigmatzianova/movie-search-bot.git
cd movie_search_bot
```

2. Установка зависимостей
```commandline
pip install -r requirements.txt
```
Файл **requirements.txt** должен содержать все зависимости
```commandline
pyTelegramBotAPI==4.9.0
python-dotenv==0.21.1

requests~=2.32.3
loader~=2017.9.11
```

3. Настройка конфигурации
Создайте файл **.env** в корне проекта и добавьте в него ваши ключи.
```commandline
TELEGRAM_BOT_TOKEN = ваш_токен_бота
RAPID_API_KEY = ваш_ключ
```
Токен бота — @BotFather

API-ключ TMDb — @kinopoiskdev_bot

4. Запуск бота
```commandline
python bot.py
```
Или для постоянной работы (с авто-рестартом):
```commandline
nohup python bot.py &
```

5. Проверка работы
   1) Откройте Telegram.
   2) Найдите бота по имени
   3) Отправьте команду **/start** — должно появиться приветственное сообщение.

### Пример структуры бота
```
movie-finder-bot/
├── bot.py           # Основной код бота
├── .env             # Конфигурация
├── requirements.txt # Зависимости
└── movies.db        # База данных (создаётся автоматически)
```
