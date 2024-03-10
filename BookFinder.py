from Globals import GlobalOptions
from border_segmentation import get_book_border
from book_recognizer import book_recognizer_func
from web_data_parser import save_data_base
from film_info import get_film_info
from Rating import make_rating
from TrainModule import prepare_raw_data
from RecomendationSystem import get_recommendation_system
from Interface import run_interface
import sys
import argparse

# TODO: after this steps the project will be finish
# 1) fix bugs in recommender system
# 2) More flexible saving and loading mechanism for the the film and the user info
# 3) fix easyOCR ML moder trainer
#


def main():
    g = GlobalOptions()
    parser = argparse.ArgumentParser(prog='BookFinder')
    parser.add_argument('filename', help='Input path to the picture')
    parser.add_argument('-t', '--train', action='store_true', help='Prepare raw picture data for training')
    parser.add_argument('-d', '--debug', action='store_true', help='Run with debug mode if need')
    parser.add_argument('-w', '--web', action='store_true', help='Collect data base about a filmed books')
    args = parser.parse_args()
    g.is_train_necessary = args.train
    g.is_debug = args.debug
    g.is_need_web_info = args.web

    # Prepare raw data for training if necessary
    if g.is_train_necessary and g.train_data_count != 0:
        try:
            prepare_raw_data(g)
            print('Data preparation for training has succeed')
        except ValueError as err:
            print(f"ValueError {err=}, {type(err)=}")
        sys.exit(0)

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
    movies_metadata, users = make_rating(g, books)

    # 5) Build recommender system
    recommender = get_recommendation_system(g)

    # 6) Run console user interface
    run_interface(g, recommender, users, movies_metadata)


if __name__ == '__main__':
    main()
