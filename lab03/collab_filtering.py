from data_handler import DataProcessor
from similarity import cosine_similarity

class CollaborativeFiltering:
    def __init__(self, data_processor: DataProcessor) -> None:
        """
        Инициализация обработчика коллаборативной фильтрации
        
        :param data_processor: обработчик данных для работы с оценками пользователей
        """
        self.dp = data_processor
    
    async def generate_recommendations(self, virtual_user_ratings: dict, num_recommendations: int = 5) -> list:
        """
        Генерация рекомендаций на основе оценок виртуального пользователя
        используя User-Based Collaborative Filtering
        
        :param virtual_user_ratings: словарь виртуального пользователя
        :param num_recommendations: количество возвращаемых рекомендаций
        :return: список кортежей c id фильмов и предсказанными рейтингами
        """
        print(f"ВИРТУАЛЬНЫЙ ПОЛЬЗОВАТЕЛЬ с разнообразными оценками:")
        for movie_id, rating in virtual_user_ratings.items():
            title = self.dp.get_movie_title(movie_id)
            print(f"   - {movie_id}: {title} = {rating}")
        
        candidate_users = set()
        for movie_id in virtual_user_ratings.keys():
            movie_ratings = self.dp.ratings_df[self.dp.ratings_df['movie_id'] == movie_id]
            users_who_watched = set(movie_ratings['user_id'].tolist())
            candidate_users.update(users_who_watched)
        
        if len(candidate_users) < 50:
            user_activity = self.dp.ratings_df.groupby('user_id').size()
            active_users = user_activity.nlargest(100).index.tolist()
            candidate_users.update(active_users)
        
        print(f"Кандидатов для сравнения: {len(candidate_users)} пользователей")
        
        similar_users = []
        for real_user_id in candidate_users:
            real_user_ratings = self.dp.get_user_ratings(real_user_id)
            
            common_movies = set(virtual_user_ratings.keys()) & set(real_user_ratings.keys())
            if len(common_movies) < 3:
                continue
                
            similarity = cosine_similarity(virtual_user_ratings, real_user_ratings)
            
            if similarity > 0.1:
                similar_users.append((real_user_id, similarity))
        
        similar_users.sort(key=lambda x: x[1], reverse=True)
        similar_users = similar_users[:20]
        
        print(f"Найдено похожих пользователей: {len(similar_users)}")
        for i, (user_id, sim) in enumerate(similar_users[:5], 1):
            print(f"   {i}. User {user_id}: сходство {sim:.3f}")
        
        if not similar_users:
            print("Нет похожих пользователей")
            return []
        
        movie_scores = {}
        watched_movies = set(virtual_user_ratings.keys())
        
        for similar_user_id, similarity in similar_users:
            similar_user_ratings = self.dp.get_user_ratings(similar_user_id)
            
            for movie_id, rating in similar_user_ratings.items():
                if movie_id not in watched_movies:
                    if movie_id not in movie_scores:
                        movie_scores[movie_id] = []
                    movie_scores[movie_id].append((rating, similarity))
        
        print(f"Собрано оценок для {len(movie_scores)} фильмов")
        
        predicted_ratings = []
        for movie_id, scores in movie_scores.items():
            if len(scores) < 2:
                continue
                
            total_weighted_score = sum(rating * similarity for rating, similarity in scores)
            total_similarity = sum(similarity for _, similarity in scores)
            
            if total_similarity > 0:
                predicted_rating = total_weighted_score / total_similarity
                predicted_rating = max(1.0, min(5.0, predicted_rating))
                predicted_ratings.append((movie_id, predicted_rating))
        
        print(f"Рассчитано рейтингов: {len(predicted_ratings)}")
        
        predicted_ratings.sort(key=lambda x: x[1], reverse=True)
        top_recommendations = predicted_ratings[:num_recommendations]
        
        print("Топ рекомендации:")
        for i, (movie_id, rating) in enumerate(top_recommendations, 1):
            title = self.dp.get_movie_title(movie_id)
            print(f"   {i}. {title}: {rating:.2f}")
        
        return top_recommendations
