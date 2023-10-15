from bs4 import BeautifulSoup
import urllib.request
import Book

debug_url = 'https://www.livelib.ru/books/filming/listview/biglist'


def get_book_info(line: str):
    if "alt=" not in line:
        return "None", "None"

    left = 0
    right = 0
    for i in range(len(line)):
        if line[i] == '\"' and left == 0:
            left = i
            continue
        if line[i] == '\"' and left != 0:
            right = i
            break

    res_line = line[left+1:right]
    if "-" not in res_line:
        return "None", "None"

    data = res_line.split(' - ')
    if len(data) != 2:
        return "None", "None"

    return data[0], data[1]


def get_web_data(url, pages: int):
    books_info = []
    pages += 1

    for i in range(1, pages):
        cur_url = url + str(i)
        req = urllib.request.urlopen(cur_url)
        soup = BeautifulSoup(req, 'lxml')
        for section in soup.find_all("img"):
            author, book = get_book_info(str(section))
            if author != "None" and book != "None":
                books_info.append(Book.BookInfo(author, book))

    return books_info


def save_data_base(url, pages: int):
    books_info = get_web_data(url, pages)

    with open("res/data_base.txt", "w", encoding="utf-8") as out:
        for info in books_info:
            out.write("{} - {}\n".format(info.get_author_name(), info.get_book_name()))
