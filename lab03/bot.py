import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from data_handler import DataProcessor
from collab_filtering import CollaborativeFiltering
from config import get_config
import random

config = get_config()
bot = Bot(token=config["tg_token"])
dp = Dispatcher()

data_processor = DataProcessor()
cf_engine = CollaborativeFiltering(data_processor)

user_sessions = {}

@dp.message(CommandStart())
async def start_command(message: Message) -> None:
    """Обработчик команды /start"""
    user_sessions[message.from_user.id] = {
        'step': 'awaiting_ranking',
        'movies_to_rank': []
    }
    
    movies_to_rank = await get_movies_for_ranking(5)
    user_sessions[message.from_user.id]['movies_to_rank'] = movies_to_rank
    
    response = (
        "Привет! Я бот для рекомендации фильмов.\n\n"
        "Расставь эти 5 фильмов в порядке от самого любимого к наименее любимому:\n\n"
    )
    
    for i, (movie_id, title) in enumerate(movies_to_rank, 1):
        response += f"{i}. {title}\n"
    
    response += (
        "\nОтправь номера в нужном порядке через запятую.\n"
        "Например, если самый любимый - фильм №3, затем №1, затем №5, затем №2, затем №4:\n"
        "`3, 1, 5, 2, 4`"
    )
    
    await message.answer(response)

async def get_movies_for_ranking(count: int = 5) -> list:
    """
    Получить фильмы для ранжирования пользователем
    
    :param count: количество фильмов для выбора
    :return: список кортежей (movie_id, title)
    """
    movie_ratings_count = data_processor.ratings_df.groupby('movie_id').size()
    popular_movies_ids = movie_ratings_count.nlargest(50).index.tolist()
    
    selected_movies = random.sample(popular_movies_ids, count)
    
    movies_with_titles = []
    for movie_id in selected_movies:
        title = data_processor.get_movie_title(movie_id)
        movies_with_titles.append((movie_id, title))
    
    return movies_with_titles

@dp.message()
async def handle_movie_ranking(message: Message) -> None:
    """
    Обработка ранжирования фильмов пользователем
    
    :param message: сообщение от пользователя с порядком фильмов
    """
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await start_command(message)
        return
    
    user_session = user_sessions[user_id]
    
    if user_session['step'] != 'awaiting_ranking':
        await message.answer("Пожалуйста, начните с команды /start")
        return
    
    try:
        ranking = [int(x.strip()) for x in message.text.split(',')]
        movies_to_rank = user_session['movies_to_rank']
        
        if (len(ranking) != len(movies_to_rank) or 
            not all(1 <= num <= len(movies_to_rank) for num in ranking) or
            len(set(ranking)) != len(ranking)):
            await message.answer(
                f"Пожалуйста, введите все числа от 1 до {len(movies_to_rank)} "
                f"без повторений через запятую.\n"
                f"Например: 3, 1, 5, 2, 4"
            )
            return
        
        virtual_user_ratings = {}
        
        rating_scores = [5.0, 4.5, 4.0, 3.5, 3.0]
        
        for position, movie_rank in enumerate(ranking):
            movie_index = movie_rank - 1
            movie_id, title = movies_to_rank[movie_index]
            rating = rating_scores[position]
            virtual_user_ratings[movie_id] = rating
            
            print(f"Пользователь поставил фильму '{title}' позицию {position+1} → оценка {rating}")
        
        await message.answer(
            "Отлично! Ты расставил фильмы по предпочтениям.\n"
            "Сейчас подберу рекомендации на основе твоего выбора..."
        )
        
        recommendations = await cf_engine.generate_recommendations(virtual_user_ratings)
        
        if recommendations:
            response = "Вот что тебе может понравиться:\n\n"
            for i, (movie_id, score) in enumerate(recommendations, 1):
                title = data_processor.get_movie_title(movie_id)
                response += f"{i}. {title} (возможно вы оцените на: {score:.2f})\n"
        else:
            response = "К сожалению, не удалось найти рекомендации. Попробуй выбрать другие фильмы."
        
        await message.answer(response)
        
        del user_sessions[user_id]
        
    except ValueError:
        await message.answer("Пожалуйста, введите числа через запятую. Например: 3, 1, 5, 2, 4")

async def main() -> None:
    """Запуск бота"""
    await data_processor.load_data()
    print("Данные загружены, бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())