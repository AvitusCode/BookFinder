import csv


def show_movies(movies_metadata):
    for pos_idx, movie_id in movies_metadata.movies_pos_id:
        print(f"[{pos_idx}]: {movies_metadata.movies_info[movie_id]}")


def movie_interface(recommender, movies_metadata):
    while True:
        command = input("[rh] Recommend film on history, [rf] Recommend on film, [m] Rank film, "
                        "[q] Select another user, [h] Show movies again")

        match command:
            case "rh":
                print(recommender.recommend_on_history())
            case "rf":
                movie_id = input("Select movieId: ")
                if movie_id not in movies_metadata.movies_info.keys():
                    print("No such movie, try again")
                print(recommender.recommend_on_movie(movie_id))
            case "m":
                movie_id = input("Select movieId: ")
                rank = input("Set a raiting: ")
                if movie_id not in movies_metadata.movies_info.keys():
                    print("No such movie, try again")
                return movie_id, rank
            case "h":
                show_movies(movies_metadata)
            case "q":
                return -1, -1


class UserMetadata(object):
    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating


def data_on_save(g, users_choises):
    # TODO: save user data to raiting csv
    pass


def run_interface(g, recommender, users, movies_metadata):
    print("\n\nPlease rate the movie after watching! :D")
    print("List of the movies")
    show_movies(movies_metadata)

    users_choises = {}
    while True:
        command = input("[u] Select a user, [h] Show movies again, [q] Quiet")
        match command:
            case "u":
                name = input("Enter your name: ")
                for user in users:
                    if user.name == name:
                        movie_id, rank = movie_interface(recommender, movies_metadata)
                        if movie_id == -1 and rank == -1:
                            continue
                        users_choises[user.user_id].append(UserMetadata(user.user_id, movie_id, rank))
            case "h":
                show_movies(movies_metadata)
            case "q":
                break
            case _:
                print("Unpredicted input! Please, try again")

    recommender.close_session()
    data_on_save(g, users_choises)
