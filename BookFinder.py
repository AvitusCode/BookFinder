import border_segmentation as bs
import book_recognizer as br
import film_info as fi
import web_data_parser as wdp

web_data = 'https://www.livelib.ru/books/filming/listview/biglist/~'
web_pages_count = 2

# TODO:
# 1) improve book border recognition
# 2) improve book text recognition
# 3) make json file for base configuration
# 4) Introduce algorithm for rating films
# 5) refactoring and debuging


def main():
    image, books = bs.get_book_border('debug_data/debug_books_5.jpg')

    # then wee save books to the file
    for book in books:
        print("[(x0={}, y0={}), (x1={}, y1={})]".format(book.x0, book.y0, book.x1, book.y1))

    # wdp.save_data_base(web_data, web_pages_count)
    books = br.book_recognizer(image, books)

    for book in books:
        print("{} - {}".format(book.author, book.book))

    # get information about films
    books = fi.get_film_info(books)

    for book in books:
        print(book)

    # TODO: read information about user preferences

    # TODO: making a list of the most suitable films


if __name__ == '__main__':
    main()
