import border_segmentation as bs
import web_data_parser as wdp

web_data = 'https://www.livelib.ru/books/filming/listview/biglist/~'
web_pages_count = 2


def main():
    image, books = bs.get_book_border('debug_data/debug_books_1.jpg')

    for book in books:
        print("[(x0={}, y0={}), (x1={}, y1={})]".format(book.x0, book.y0, book.x1, book.y1))

    # wdp.save_data_base(web_data, web_pages_count)


if __name__ == '__main__':
    main()
