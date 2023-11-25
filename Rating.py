from User import User
import json
import sys


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
            user = User(user_name, user_info['user_id'])
            user.years = user_info['years']
            user.rating = user_info['rating']
            user.duration = user_info['duration']
            user.genres = user_info['genres']
            user.countries = user_info['countries']

            users.append(user)

    return users


def match_rank(movie, users):
    rank = 0.0
    user_weight = len(users)
    for user in users:
        rank += user.in_years(movie.year) / user_weight
        rank += user.in_rating(movie.rating) / user_weight
        rank += user.in_genres(movie.genres) / user_weight
        rank += user.in_countries(movie.countries) / user_weight
        rank += user.in_duration(movie.duration) / user_weight

    return rank


def content_based_recommendations(users, movies):
    movie_rank = {}
    movie_id = 0

    for movie in movies:
        rank = match_rank(movie, users)
        movie_rank[rank] = movie_id
        movie_id += 1

    return dict(sorted(movie_rank.items(), reverse=True))


def make_rating(films, top_n=10):
    top_n = min(top_n, len(films))
    users = load_users_all()

    if len(users) == 0:
        print('WARNING: no users in the system!')
        sys.exit(0)

    movie_rank = content_based_recommendations(users, films)
    pos_in_rating = 1
    for _, value in movie_rank.items():
        print("Film № {} : {}, {}, rating {}".format(pos_in_rating, films[value].film_title, films[value].year,
                                                     films[value].rating))
        pos_in_rating += 1
        if pos_in_rating == top_n:
            break

    print("\n\nPlease, make a choice and enjoy watching! :D")
