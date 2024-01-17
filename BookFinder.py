from Globals import GlobalOptions
from border_segmentation import get_book_border
from book_recognizer import book_recognizer_func
from web_data_parser import save_data_base
from film_info import get_film_info
from Rating import make_rating
import sys
import argparse


def main():
    g = GlobalOptions()
    parser = argparse.ArgumentParser(prog='BookFinder')
    parser.add_argument('filename', help='Input path to the picture')
    parser.add_argument('-d', '--debug', action='store_true', help='Run with debug mode if need')
    parser.add_argument('-w', '--web', action='store_true', help='Collect data base about a filmed books')
    args = parser.parse_args()
    g.is_debug = args.debug
    g.is_need_web_info = args.web

    # 1) get books border
    image, books = get_book_border(g, str(args.filename))

    # (Optional step) load info about filming books
    if g.is_need_web_info:
        save_data_base(g.web_database_url, g.web_pages_count)

    # 2) recognize book
    books = book_recognizer_func(g, image, books)
    if len(books) == 0:
        print("Cannot recognize a books")
        sys.exit(0)

    if g.is_debug:
        for book in books:
            print("{}, {}".format(book.get_author_name(), book.get_book_name()))

    # 3) get information about films
    books = get_film_info(books)

    if len(books) == 0:
        print("Cannot find film from the database")
        sys.exit(0)

    # 4) make ranking list
    make_rating(g, books)


if __name__ == '__main__':
    main()
