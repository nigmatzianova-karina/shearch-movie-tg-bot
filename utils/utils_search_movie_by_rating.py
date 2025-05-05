import requests
from typing import Optional, List, Dict
from config_data import config
from requests.exceptions import RequestException, JSONDecodeError

BASE_URL = (
    'https://api.kinopoisk.dev/v1.4/'
    'movie?page=1&limit=100'
    '&selectFields=name'
    '&notNullFields=name'
    '&notNullFields=description'
    '&notNullFields=year'
    '&notNullFields=rating.kp'
    '&notNullFields=rating.imdb'
    '&notNullFields=ageRating'
    '&notNullFields=genres.name'
    '&notNullFields=countries.name'
    '&notNullFields=poster.url'
    '&sortField=rating.kp'
    '&sortType=1&rating.kp='
)

HEADERS = {
    'X-API-KEY': config.RAPID_API_KEY,
    'X-API-HOST': 'api.kinopoisk.dev'
}


def search_by_rating(rating: str) -> Optional[List[Dict]]:
    """
    Поиск фильмов по рейтингу Кинопоиска.

    Args:
        rating (float): Минимальный рейтинг фильма (от 0 до 10)

    Returns:
        Optional[List[Dict]]: Список фильмов с указанным рейтингом или None, если ничего не найдено

    Raises:
        ValueError: Если передан некорректный рейтинг
        RequestException: При ошибке запроса к API
    """
    try:
        url = f"{BASE_URL}{rating}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get('docs') or data.get('total', 0) == 0:
            return None

        return data['docs']

    except RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except JSONDecodeError:
        print("Ошибка декодирования JSON ответа")
        return None
