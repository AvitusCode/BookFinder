from User import User
import json
import sys
import numpy as np
from Globals import _COUNTRIES_
from Globals import _GENRES_


# A few support functions
def null_array(n):
    x = np.zeros(n, dtype=float)
    return x


def check_correctness(user_diap: str, y, info: str):
    a, _ = user_diap.split('-')
    a = float(a)
    y = float(y)

    if a <= y:
        print(info)
        return False

    return True


def make_country_feature_vec(features: str):
    vec = null_array(len(_COUNTRIES_))
    splited_features = features.split(', ')

    for i in range(len(_COUNTRIES_)):
        for country in splited_features:
            if country.lower() == _COUNTRIES_[i].lower():
                vec[i] = 1.0

    return vec


def make_genres_feature_vec(features: str):
    vec = null_array(len(_GENRES_))
    splited_features = features.split(', ')

    for i in range(len(_GENRES_)):
        for genre in splited_features:
            if genre.lower() == _GENRES_[i].lower():
                vec[i] = 1.0

    return vec


def rho_func(feature_diap: str, y, weight: float):
    a, b = feature_diap.split('-')
    a = float(a)
    b = float(b)
    y = float(y)

    if a <= y <= b:
        return 0.0
    elif y < a:
        return np.fabs(a - y) / weight
    else:
        return np.fabs(b - y) / weight


def cosine_similarity(x, y):
    x_size = len(x)
    y_size = len(y)

    if x_size < y_size:
        np.pad(x, (0, y_size - x_size), mode='constant')
    if y_size < x_size:
        np.pad(y, (0, x_size - y_size), mode='constant')

    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)

    if norm_y == 0.0 or norm_x == 0.0:
        return 0.0

    return np.fabs(np.dot(x, y)) / (norm_x * norm_y)


def load_user_by_name(name):
    with open("users_profile.json", 'r') as file:
        data = json.load(file)
        if name not in data:
            return None

        user_info = data[name]
        user = User(name, user_info['user_id'])
        user.years = user_info['years']
        user.rating = user_info['rating']
        user.duration = user_info['duration']
        user.genres = user_info['genres']
        user.countries = user_info['countries']

        return user


def load_users_all():
    users = []
    with open("users_profile.json", 'r') as file:
        data = json.load(file)

        for user_name, user_info in data.items():
            is_ok = True
            user = User(user_name, user_info['user_id'])
            user.years = user_info['years']
            user.rating = user_info['rating']
            user.duration = user_info['duration']
            user.genres = user_info['genres']
            user.countries = user_info['countries']

            is_ok = is_ok and check_correctness(user.years, 1899, f"ERROR: user {user_name} year")
            is_ok = is_ok and check_correctness(user.duration, 0, f"ERROR: user {user_name} duration")
            is_ok = is_ok and check_correctness(user.rating, 0, f"ERROR: user {user_name} input rank")
            if not is_ok:
                continue
            if len(user.countries) == 0 or len(user.genres) == 0:
                print(f"ERROR: user {user_name} empty country and/or genres")
                continue

            users.append(user)

    return users


def match_rank(g, movie, users):
    rank = 0.0
    for user in users:
        rank += 1.0 - rho_func(user.years, movie.year, g.year_diap)
        rank += 1.0 - rho_func(user.rating, movie.rating, g.rank_diap)
        rank += 1.0 - rho_func(user.duration, movie.duration, g.duration_diap)
        rank += cosine_similarity(make_genres_feature_vec(user.genres), make_genres_feature_vec(movie.genres))
        rank += cosine_similarity(make_country_feature_vec(user.countries), make_country_feature_vec(movie.countries))
        rank /= 5.0

    return rank


def content_based_recommendations(g, users, movies):
    rank_movie = []
    movie_id = 0

    for movie in movies:
        rank = match_rank(g, movie, users)
        rank_movie.append((rank, movie_id))
        movie_id += 1

    srank_movie = sorted(rank_movie, key=lambda tup: tup[0], reverse=True)
    return srank_movie


def make_rating(g, films, top_n=20):
    top_n = min(top_n, len(films))
    users = load_users_all()

    if len(users) == 0:
        print('WARNING: no users in the system!')
        sys.exit(0)

    try:
        movie_rank = content_based_recommendations(g, users, films)
    except ValueError as verr:
        print(f"Error during rating process: {verr}")
        return

    pos_in_rating = 1
    for rank, id in movie_rank:
        print("Film № {} : {}, {}, rating {}".format(pos_in_rating, films[id].film_title, films[id].year,
                                                     films[id].rating))
        if g.is_debug:
            print(f"rank = {rank}, id = {id}")

        pos_in_rating += 1
        if pos_in_rating == top_n:
            break

    print("\n\nPlease, make a choice and enjoy watching! :D")
