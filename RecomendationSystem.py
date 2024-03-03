import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


class ContentBasedRecommender(object):
    '''
    Here we will build simple Content-Based Recommendation System:
    It is a type of recommendation system which works on the principle of similar content.
    If a user is watching a movie, then the system will check about other movies of similar content or the same genre of
    the movie the user is watching.
    '''

    def __init__(self, movies, rating_pivot, nn_algo):
        self.movies = movies
        self.rating_pivot = rating_pivot
        self.nn_algo = nn_algo
        self.history = []        # Storing a history of the recommendations
        self.is_hist = False     # Check if history is empty

    def recommend_on_movie(self, movie_id, n_recommends=5):
        self.is_hist = True
        self.history.append(movie_id)

        distance, neighbors = self.nn_algo.kneighbors([self.rating_pivot.loc[movie_id]], n_neighbors=n_recommends + 1)
        movie_ids = [self.rating_pivot.iloc[i].name for i in neighbors[0]]
        recommendations = [str(self.movies[self.movies['movieId'] == mid]['title']).split('\n')[0].split('  ')[-1]
                           for mid in movie_ids if mid not in [movie_id]]

        return recommendations[:n_recommends]

    def recommend_on_history(self, n_recommends=5):
        if not self.is_hist:
            return print('No history found')

        hist = np.array([list(self.rating_pivot.loc[mid]) for mid in self.history])
        distance, neighbors = self.nn_algo.kneighbors([np.average(hist, axis=0)],
                                                      n_neighbors=n_recommends + len(self.history))

        movie_ids = [self.rating_pivot.iloc[i].name for i in neighbors[0]]
        recommendations = [str(self.movies[self.movies['movieId'] == mid]['title']).split('\n')[0].split('  ')[-1]
                           for mid in movie_ids if mid not in self.history]

        return recommendations[:n_recommends]

    def close_session(self):
        try:
            with open("res/films_history.txt", "w") as file:
                for movie_id in self.history:
                    file.write(f"{movie_id}\n")
        except Exception as ex:
            print(f"Cannot open a file for save {ex}")

    def open_session(self):
        try:
            with open("res/films_history.txt", "r") as file:
                while line := file.readline():
                    self.history.append(int(line))
        except Exception as ex:
            print(f"Cannot open a file for read or have a parsing problem {ex}")


def get_recommendation_system(g):
    movies = pd.read_csv(g.movies_data, sep=';', encoding='utf8').drop('Unnamed: 3', axis=1)
    ratings = pd.read_csv(g.ranking_data, sep=';')
    rating_pivot = ratings.pivot_table(values='rating', columns='userId', index='movieId').fillna(0)

    nn_algo = NearestNeighbors(metric='cosine')
    nn_algo.fit(rating_pivot)

    recommender = ContentBasedRecommender(movies, rating_pivot, nn_algo)
    recommender.open_session()

    return recommender
