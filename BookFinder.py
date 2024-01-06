from Globals import GlobalOptions
from border_segmentation import get_book_border
from book_recognizer import book_recognizer_func
from web_data_parser import save_data_base
from film_info import get_film_info
from Rating import make_rating
import sys

# TODO: testing and debuging +
# 1) improve book border recognition
# 2) improve book text recognition


def main():
    g = GlobalOptions()
    # 1) get books border
    image, books = get_book_border(g, 'debug_data/debug_books_5.jpg')

    # (Optional step) load info about filming books
    if g.is_need_web_info:
        save_data_base(g.web_database_url, g.web_pages_count)

    # 2) recognize book
    books = book_recognizer_func(g, image, books)
    if len(books) == 0:
        print("Cannot recognize a books")
        sys.exit(0)

    # 3) get information about films
    books = get_film_info(books)

    if len(books) == 0:
        print("Cannot find film from the database")
        sys.exit(0)

    # 4) make ranking list
    make_rating(g, books)


if __name__ == '__main__':
    main()
