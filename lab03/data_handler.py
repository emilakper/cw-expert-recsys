import pandas as pd
from config import get_config

class DataProcessor:
    def __init__(self) -> None:
        """
        Инициализация обработчика данных для работы с датасетом
        """
        self.config = get_config()
        self.ratings_df = None
        self.user_item_table = None
        self.movie_titles = None
    
    async def load_data(self) -> None:
        """Асинхронная загрузка данных из датасета"""
        self.ratings_df = pd.read_csv(
            self.config["dataset_path"], 
            sep='\t',
            names=['user_id', 'movie_id', 'rating', 'timestamp']
        )
        
        dataset_dir = '/'.join(self.config["dataset_path"].split('/')[:-1])
        movies_path = f"{dataset_dir}/u.item"
        
        try:
            self.movie_titles = pd.read_csv(
                movies_path, 
                sep='|', 
                encoding='latin-1',
                header=None,
                usecols=[0, 1],
                names=['movie_id', 'title']
            )
            print(f"Загружено {len(self.movie_titles)} названий фильмов")
        except Exception as e:
            print(f"Ошибка загрузки названий фильмов: {e}")
            self.movie_titles = pd.DataFrame(columns=['movie_id', 'title'])
        
        await self._create_user_item_table()
    
    async def _create_user_item_table(self) -> None:
        """Создание таблицы пользователь × фильм"""
        self.user_item_table = self.ratings_df.pivot(
            index='user_id', 
            columns='movie_id', 
            values='rating'
        ).fillna(0)
    
    def get_user_ratings(self, user_id: int) -> dict:
        """
        Получить оценки конкретного пользователя
        
        :param user_id: ID пользователя
        :return: словарь {movie_id: rating} с ненулевыми оценками
        """
        if user_id in self.user_item_table.index:
            user_ratings = self.user_item_table.loc[user_id]
            return {movie_id: rating for movie_id, rating in user_ratings.items() if rating > 0}
        return {}
    
    def get_all_users(self) -> list:
        """
        Получить список всех пользователей
        
        :return: список ID пользователей
        """
        return self.user_item_table.index.tolist()
    
    def get_movie_title(self, movie_id: int) -> str:
        """
        Получить название фильма по ID
        
        :param movie_id: ID фильма
        :return: название фильма
        """
        if self.movie_titles is not None and not self.movie_titles.empty:
            title_row = self.movie_titles[self.movie_titles['movie_id'] == movie_id]
            return title_row['title'].iloc[0] if not title_row.empty else f"Фильм {movie_id}"
        return f"Фильм {movie_id}"
