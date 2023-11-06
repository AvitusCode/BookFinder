import Book
from Kino import KP


DEBUG: bool = False


def read_secret_token() -> str:
    with open('token.txt') as file:
        token = file.readline()
        if not token:
            raise Exception("There is no token in the file!")

        return token

    raise Exception("There is no token file!")


def get_film_info(books):
    kino = KP(token=read_secret_token(), tries=10)

    filmed_books = []

    if DEBUG:
        tenet = kino.get_film_by_id(1236063)
        print(tenet.ru_name, tenet.year)
        print(", ".join(tenet.genres))
        print(", ".join(tenet.countries))
        print("Rank {}".format(tenet.kp_rate))
        return filmed_books

    for book in books:
        search = kino.search_by_keywords(book.get_book_name())
        if not search:
            continue

        for item in search:
            film = Book.BookInfo(book.get_author_name(), item.ru_name)
            film.set_year(int(item.year))
            film.set_genres(" ".join(item.genres))
            film.set_countries(" ".join(item.countries))
            film.set_rating(item.kp_rate)
            film.set_duration(item.duration)
            filmed_books.append(film)

    return filmed_books
