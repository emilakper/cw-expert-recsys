import aiohttp
from config import get_config

config = get_config()

async def query_llm_api(url: str, host: str, payload: dict, use_authorization: bool = False) -> dict:
    """
    Выполняет асинхронный POST-запрос на LLM в RapidAPI.

    :url: URL на LLM
    :host: Хост для заголовка
    :payload: Данные запроса
    :return: Словарь с ответом или None при ошибке 
    """
    headers = {
        "x-rapidapi-key": config["rapid_key"],
        "x-rapidapi-host": host,
        "Content-Type": "application/json"
    }
    if use_authorization:
        headers["Authorization"] = "Bearer I can do this all day !!"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as err:
        print(f"Ошибка API: {err}")
        return None
    
async def get_gpt4_response(user_query: str, context: str = "") -> str:
    """
    Запрос к GPT4o API с учетом контекста.
    :user_query: Текст запроса пользователя.
    :context: Дополнительный контекст.
    :return: Ответ от GPT или None.
    """
    payload = {
        "system_prompt": f"{context} You are movie advisor.",
        "user_prompt": user_query
    }
    response = await query_llm_api(config["gpt4_url"], config["gpt4_host"], payload, use_authorization=True)
    return response["response"] if response and "response" in response else None

async def get_gpt3_response(user_query: str, context: str = "") -> str:
    """
    Запрос к GPT3 API с учетом контекста.
    :user_query: Текст запроса пользователя.
    :context: Дополнительный контекст.
    :return: Ответ от GPT или None.
    """
    payload = [
        {"role": "system", "content": f"{context} You are movie advisor."},
        {"role": "user", "content": user_query}
    ]
    response = await query_llm_api(config["gpt3_url"], config["gpt3_host"], payload)
    return response["text"] if response and "text" in response else None
