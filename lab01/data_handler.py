from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()


def get_api_config() -> dict:
    """
    Функция для чтения конфигурации API из .env-файла
    """
    return {
        "rapidapi_key": os.getenv("RAPIDAPI_KEY"),
        "pizza_host": os.getenv("PIZZA_API_HOST"),
        "wizzard_host": os.getenv("API_WIZZARD_HOST"),
        "pizza_url": os.getenv("PIZZA_API_URL"),
        "wizzard_url": os.getenv("API_WIZZARD_URL"),
    }
