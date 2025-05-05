import requests
from typing import Optional, List, Dict
from config_data import config
from requests.exceptions import RequestException

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
    '&sortField=budget.value'
    '&sortType=1&budget.value='
)

HEADERS = {
    'X-API-KEY': config.RAPID_API_KEY,
    'X-API-HOST': 'api.kinopoisk.dev',
}


def search_by_budget(budget_range: str) -> Optional[List[Dict]]:
    """
    Поиск фильмов по бюджету с использованием API Кинопоиска.

    Args:
        budget_range (str): Диапазон бюджета в формате 'min-max' (например: '1000000-5000000')

    Returns:
        Optional[List[Dict]]: Список фильмов или None, если ничего не найдено

    Raises:
        RequestException: При ошибке запроса к API
        ValueError: При некорректном формате бюджета
    """
    try:
        if '-' not in budget_range:
            raise ValueError("Некорректный формат бюджета. Используйте формат 'min-max'")

        url = f"{BASE_URL}{budget_range}"

        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("total", 0) == 0:
            return None

        return data["docs"]

    except RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка в формате бюджета: {e}")
        return None
