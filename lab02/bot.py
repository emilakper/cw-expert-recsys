import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from llm_handler import get_gpt4_response, get_gpt3_response, get_qwen_response
from config import get_config

config = get_config()
bot = Bot(token=config["tg_token"])
dp = Dispatcher()

current_model = "gpt4"

@dp.message(CommandStart())
async def start_command(message: Message) -> None:
    """Обработчик команды /start"""
    await message.answer(f"Hi, I'm film recommendation bot.\n"
                         "Commands:\n"
                         "/setmodel gpt4 - choose GPT-4o\n"
                         "/setmodel gpt3 - choose GPT-3\n"
                         "/setmodel qwen - выбрать Qwen3-8B\n"
                         "Send request, like 'Recommend a movie like Interstellar'.")

@dp.message(Command("setmodel"))
async def set_model(message: Message) -> None:
    """Обработчик команды /setmodel для выбора модели"""
    global current_model
    model = message.text.split()[1].lower() if len(message.text.split()) > 1 else ""
    if model in ["gpt4", "gpt3", "qwen"]:
        current_model = model
        await message.answer(f"Model chosen: {current_model}")
    else:
        await message.answer("Unknown model. Use /setmodel gpt4/gpt3/qwen.")

@dp.message()
async def handle_query(message: Message) -> None:
    query = message.text.strip()
    if current_model == "qwen":
        response = await get_qwen_response(query)
    elif current_model == "gpt4":
        response = await get_gpt4_response(query)
    else:
        response = await get_gpt3_response(query)
    if response:
        max_len = 4000
        parts = [response[i:i+max_len] for i in range(0, len(response), max_len)]
        for part in parts:
            await message.answer(part)
    else:
        await message.answer("Error on API server side.")


async def main() -> None:
    """Запуск бота"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
