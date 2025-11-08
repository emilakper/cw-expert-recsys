import numpy as np

def cosine_similarity(user1_ratings: dict, user2_ratings: dict) -> float:
    """
    Вычисление косинусного сходства между двумя пользователями
    на основе их оценок фильмов
    
    :param user1_ratings: словарь {movie_id: rating} для пользователя 1
    :param user2_ratings: словарь {movie_id: rating} для пользователя 2
    :return: косинусное сходство от -1 до 1
    """
    common_movies = set(user1_ratings.keys()) & set(user2_ratings.keys())
    
    if not common_movies:
        return 0.0
    
    vec1 = np.array([user1_ratings[movie] for movie in common_movies])
    vec2 = np.array([user2_ratings[movie] for movie in common_movies])
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)
