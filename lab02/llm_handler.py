import aiohttp
import json
from config import get_config

config = get_config()

async def query_llm_api(url: str, host: str, payload: dict, api_type: str = "rapid", use_authorization: bool = False) -> dict:
    """
    Асинхронный POST-запрос к LLM API.

    :param url: URL на LLM.
    :param host: Хост для заголовка.
    :param payload: Данные запроса.
    :param api_type: Тип API ("rapid" для RapidAPI, "hf" для Hugging Face).
    :param use_authorization: Флаг для добавления Authorization в RapidAPI.
    :return: Словарь с ответом или None при ошибке.
    """
    if api_type == "rapid":
        headers = {
            "x-rapidapi-key": config["rapid_key"],
            "x-rapidapi-host": host,
            "Content-Type": "application/json"
        }
        if use_authorization:
            headers["Authorization"] = "Bearer I can do this all day !!"
    elif api_type == "hf":
        headers = {
            "Authorization": f"Bearer {config['hf_token']}",
            "Content-Type": "application/json"
        }
    else:
        raise ValueError("Неверный api_type: rapid или hf")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=60)) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as err:
        print(f"Ошибка API: {err}")
        return None

async def get_qwen_response(user_query: str, context: str = "") -> str:
    """
    Запрос к Qwen3-8B через Hugging Face Router.
    """
    payload = {
        "messages": [
            {"role": "system", "content": f"You are a movie advisor. {context}"},
            {"role": "user", "content": user_query}
        ],
        "model": "Qwen/Qwen3-8B:nscale",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.6,
            "top_p": 0.95,
            "top_k": 20,
            "min_p": 0,
            "presence_penalty": 1.0,
            "enable_thinking": True
        }
    }
    response = await query_llm_api(config["hf_url"], config["hf_host"], payload, api_type="hf")
    return response["choices"][0]["message"]["content"] if response and "choices" in response else None

async def get_gpt4_response(user_query: str, context: str = "") -> str:
    payload = {
        "system_prompt": f"{context} You are movie advisor.",
        "user_prompt": user_query
    }
    response = await query_llm_api(config["gpt4_url"], config["gpt4_host"], payload, api_type="rapid", use_authorization=True)
    return response["response"] if response and "response" in response else None

async def get_gpt3_response(user_query: str, context: str = "") -> str:
    payload = [
        {"role": "system", "content": f"{context} You are movie advisor."},
        {"role": "user", "content": user_query}
    ]
    response = await query_llm_api(config["gpt3_url"], config["gpt3_host"], payload, api_type="rapid")
    return response["text"] if response and "text" in response else None
