import Book
import math
import Plotter as plt
import Rotating as rot
import easyocr
from thefuzz import fuzz

# EASYOCR configuration
reader = easyocr.Reader(['ru'], gpu=False)
DEBUG: bool = True


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


def make_rotate_by_angle(image, angle):
    image_height, image_width = image.shape[0:2]
    image_rotated = rot.rotate_image(image, angle)
    image_rotated = rot.crop_around_center(
        image_rotated,
        *rot.largest_rotated_rect(
            image_width,
            image_height,
            math.radians(angle)
        )
    )

    return image_rotated


def book_match(image_text):
    if DEBUG:
        print(image_text)

    with open("res/data_base.txt", "r", encoding="utf-8") as base:
        while True:
            line = base.readline()
            if not line:
                break

            author, book = line.split(' - ')
            concat = author + book
            concat = concat.lower()
            for text in image_text:
                ratio_author = fuzz.token_sort_ratio(text, author.lower())
                ratio_book = fuzz.token_sort_ratio(text, book.lower())
                ratio = fuzz.token_sort_ratio(text, concat)
                if ratio_author >= 75 or ratio_book >= 75 or ratio >= 75:
                    return Book.BookInfo(author, book), True

    return Book.BookInfo("None", "None"), False


def book_recognizer(image, borders):
    books = []
    books_founded_counter = 0
    for border in borders:
        try:
            image_cropped = image[border.y0:border.y1, border.x0:border.x1]

            for angle in [0, 90, 180, 270]:
                image_rotated = make_rotate_by_angle(image_cropped.copy(), angle)
                if DEBUG:
                    plt.image_plot(image_rotated, color='color')

                image_text = recognize_text(image_rotated)
                if len(image_text) == 0:
                    continue

                book, is_matched = book_match(image_text)

                if is_matched:
                    books.append(book)
                    books_founded_counter += 1
                    break

        except ValueError:
            print("Some error has occured")
            break
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            break

    print("Books was founded={}".format(books_founded_counter))
    return books
