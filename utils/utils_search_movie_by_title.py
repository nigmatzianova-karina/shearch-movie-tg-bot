import requests
from typing import Dict, Optional
from config_data import config
from urllib.parse import quote
from requests.exceptions import RequestException, JSONDecodeError

BASE_URL = 'https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&query='
HEADERS = {
    'X-API-KEY': config.RAPID_API_KEY,
    'X-API-HOST': 'api.kinopoisk.dev'
}


def search_by_title(title: str) -> Optional[Dict[str, str]]:
    """
    Поиск информации о фильме по названию через API Кинопоиска.

    Args:
        title (str): Название фильма для поиска

    Returns:
        Optional[Dict[str, str]]: Словарь с информацией о фильме или None, если фильм не найден

    Raises:
        RequestException: При ошибке HTTP-запроса
        ValueError: При отсутствии данных о фильме
    """
    try:
        encoded_title = quote(title)
        url = f"{BASE_URL}{encoded_title}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get('docs') or len(data['docs']) == 0:
            return None

        movie_data = data['docs'][0]

        return {
            'name': str(movie_data.get('name', 'Название не указано')),
            'description': f"{str(movie_data.get('description', 'Описание отсутствует'))[:500]}...",
            'KP': str(movie_data.get('rating', {}).get('kp', 'N/A')),
            'IMDb': str(movie_data.get('rating', {}).get('imdb', 'N/A')),
            'year': str(movie_data.get('year', 'Год не указан')),
            'genres': [genre.get('name', '') for genre in movie_data.get('genres', [])],
            'ageRating': str(movie_data.get('ageRating', 'N/A')),
            'countries': [country.get('name', '') for country in movie_data.get('countries', [])],
            'poster_url': movie_data.get('poster', {}).get('url', '')
        }

    except RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except JSONDecodeError:
        print("Ошибка декодирования JSON ответа")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None
