from dotenv import load_dotenv
import os

load_dotenv()

def get_config() -> dict:
    """
    Возвращает конфигурациб тг-бота и RapidAPI
    :return: Словарь с токенами и URL.
    """
    return {
        "tg_token": os.getenv("TELEGRAM_TOKEN"),
        "rapid_key": os.getenv("RAPIDAPI_KEY"),
        "gpt4_host": os.getenv("GPT4_HOST"),
        "gpt4_url": os.getenv("GPT4_URL"),
        "gpt3_host": os.getenv("GPT3_HOST"),
        "gpt3_url": os.getenv("GPT3_URL")
    }