from dotenv import load_dotenv
import os

load_dotenv()

def get_config() -> dict:
    """
    Возвращает конфигурацию тг-бота и датасет
    :return: Токен и путь до датасета.
    """
    return {
        "tg_token": os.getenv("TELEGRAM_TOKEN"),
        "dataset_path": os.getenv("DATASET_PATH", "data/u.data")
    }
