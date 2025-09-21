import requests
from data_handler import get_api_config

# Получаем конфигурацию API
config = get_api_config()


def make_api_request(url: str, headers: dict, text: str) -> dict:
    """
    Функция для выполнения GET-запроса к API и возврата JSON-ответа

    :url: URL-ссылка эндпойнта
    :headers: Заголовки запроса
    :text: Данные для запроса (отзыв)
    :return: Словарь с ответом
    """
    try:
        response = requests.get(url, headers=headers, params={"text": text})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP-ошибка: {err}")
        return None


def analyze_pizza_api(text: str) -> dict:
    """
    Функция для анализа текста отзыва через Text Sentiment Analysis API и возврата результата.

    :text: Текст отзыва для анализа
    :return: Словарь с результатами анализа
    """
    headers = {
        "X-RapidAPI-Key": config["rapidapi_key"],
        "X-RapidAPI-Host": config["pizza_host"],
    }
    return make_api_request(config["pizza_url"], headers, text)


def analyze_wizzard_api(text: str) -> dict:
    """
    Функция для анализа текста отзыва через Sentiment Analyzer API и возврата результата.

    :text: Текст отзыва для анализа
    :return: Словарь с результатами анализа
    """
    headers = {
        "X-RapidAPI-Key": config["rapidapi_key"],
        "X-RapidAPI-Host": config["wizzard_host"],
    }
    return make_api_request(config["wizzard_url"], headers, text)
