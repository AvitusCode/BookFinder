import Book
import Rotating as rot
import easyocr
from thefuzz import fuzz
from multiprocessing import Pool
import os

# EASYOCR configuration
reader = easyocr.Reader(['ru'], gpu=False)


def recognize_text(image):
    result = reader.readtext(image,
                             allowlist='АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя -0123456789',
                             detail=1,
                             paragraph=False)
    output = []

    for (bbox, text, prob) in result:
        if len(text) < 3:
            continue
        output.append(text.lower())

    return output


def book_match(image_text, reliability):
    with open("res/data_base.txt", "r", encoding="utf-8") as base:
        while True:
            line = base.readline()
            if not line:
                break
            try:
                author, book = line.split(' - ')
                concat = author + book
                concat = concat.lower()
                for text in image_text:
                    ratio_author = fuzz.token_sort_ratio(text, author.lower())
                    ratio_book = fuzz.token_sort_ratio(text, book.lower())
                    ratio = fuzz.token_sort_ratio(text, concat)
                    if ratio_author >= reliability or ratio_book >= reliability or ratio >= reliability:
                        return Book.BookInfo(author, book), True
            except Exception as err:
                print(f"Error {err=}, {type(err)=}, in process {os.getpid()}")
                break

    return Book.BookInfo("None", "None"), False


def book_process(image, angle, reliability):
    image_rotated = rot.make_rotate_by_angle(image.copy(), angle)
    image_text = recognize_text(image_rotated)
    if len(image_text) == 0:
        return Book.BookInfo("None", "None"), False

    return book_match(image_text, reliability=reliability)


def book_recognizer_func(g, image, borders):
    books = []
    books_founded_counter = 0

    with Pool(processes=4) as pool:
        for border in borders:
            try:
                image_cropped = image[border.y0:border.y1, border.x0:border.x1]
                multiple_results = [pool.apply_async(book_process, args=(image_cropped, angle, g.fuzzy_reliability))
                                    for angle in [0, 90, 180, 270]]

                for res in multiple_results:
                    book, is_matched = res.get(timeout=60)

                    if is_matched:
                        books.append(book)
                        books_founded_counter += 1
                        continue
            except ValueError:
                print("Some error has occured")
                break
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                break

    print("Books was founded={}".format(books_founded_counter))
    return books
