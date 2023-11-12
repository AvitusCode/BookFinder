from Globals import GlobalOptions
from border_segmentation import get_book_border
from book_recognizer import book_recognizer_func
from web_data_parser import save_data_base
import film_info as fi


# TODO:
# 1) improve book border recognition
# 2) improve book text recognition
# 3) make json file for base configuration (OPTIONAL)
# 4) Introduce algorithm for rating films
# 5) refactoring and debuging


# 19.11.2023 soft deadline
# 26.11.2023 hard deadline (The main pipeline should already be ready by this point.
# The remaining time will be devoted to improvements)

def main():
    g = GlobalOptions()
    # 1) get books border
    image, books = get_book_border(g, 'debug_data/debug_books_5.jpg')

    # load info about filming books
    if g.is_need_web_info:
        save_data_base(g.web_database_url, g.web_pages_count)

    # 2) recognize book
    books = book_recognizer_func(g, image, books)

    # 3) get information about films
    books = fi.get_film_info(books)

    for book in books:
        print(book)

    # TODO: read information about user preferences

    # TODO: making a list of the most suitable films


if __name__ == '__main__':
    main()
