import math

def cosine_similarity(user1_ratings: dict, user2_ratings: dict) -> float:
    """
    Вычисление косинусного сходства между двумя пользователями
    на основе их оценок фильмов
    
    :param user1_ratings: словарь для пользователя 1
    :param user2_ratings: словарь для пользователя 2
    :return: косинусное сходство от -1 до 1
    """
    common_movies = set(user1_ratings.keys()) & set(user2_ratings.keys())
    
    if not common_movies:
        return 0.0
    
    dot_product = 0.0
    norm1_squared = 0.0
    norm2_squared = 0.0

    for movie_id in common_movies:
        rating1 = user1_ratings[movie_id]
        rating2 = user2_ratings[movie_id]

        dot_product += rating1 * rating2
        norm1_squared += rating1 * rating1
        norm2_squared += rating2 * rating2
    
    norm1 = math.sqrt(norm1_squared)
    norm2 = math.sqrt(norm2_squared)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)
