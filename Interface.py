import pandas as pd


def show_movies(movies_metadata):
    for i in range(movies_metadata.size):
        print(f"[{i}]: id={movies_metadata.movies_id[i]}, {movies_metadata.movies_info[i]}")


def movie_interface(recommender, movies_metadata):
    while True:
        command = input("[rh] Recommend film on history, [rf] Recommend on film, [m] Rank film, "
                        "[q] Select another user, [h] Show movies again\n")

        match command:
            case "rh":
                print(recommender.recommend_on_history())
            case "rf":
                movie_id = int(input("Select movieId: "))
                if movie_id not in movies_metadata.movies_id:
                    print("No such movie, try again")
                    continue
                print(recommender.recommend_on_movie(movie_id))
            case "m":
                movie_id = int(input("Select movieId: "))
                if movie_id not in movies_metadata.movies_id:
                    print("No such movie, try again")
                    continue
                rank = float(input("Set a raiting: "))
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
    line = []
    for user_id, metadata in users_choises:
        line.append([int(user_id), int(metadata.movie_id), metadata.rating, 0])

    if len(line) != 0:
        df_new_data = pd.DataFrame(line, columns=["userId", "movieId", "rating", "timestamp"])
        df_new_data.to_csv(g.movies_data, mode='a', sep=';', header=False, index=False)


def run_interface(g, recommender, users, movies_metadata):
    print("\n\nPlease rate the movie after watching! :D")
    print("List of the movies")

    users_choises = {}
    while True:
        command = input("[u] Select a user, [h] Show movies again, [q] Quiet\n")
        match command:
            case "u":
                name = str(input("Enter your name: "))
                user_choised = False
                for user in users:
                    if user.name.lower() == name.lower():
                        movie_id, rank = movie_interface(recommender, movies_metadata)
                        if movie_id == -1 and rank == -1:
                            user_choised = True
                            break
                        users_choises.update({user.user_id: UserMetadata(user.user_id, movie_id, rank)})
                        user_choised = True
                        break
                if not user_choised:
                    print("WARNING: this user does not exist")
            case "h":
                show_movies(movies_metadata)
            case "q":
                break
            case _:
                print("Unpredicted input! Please, try again")

    recommender.close_session()
    data_on_save(g, users_choises)
