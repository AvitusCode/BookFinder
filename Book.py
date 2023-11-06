

class BoundingBox(object):
    """
    The BoundingBox is defined by the vertex coordinates of the box;
    """

    def __init__(self, points):
        self.x0 = points[0] # (x0, y0)
        self.y0 = points[1]
        self.x1 = points[2] # (x1, y1)
        self.y1 = points[3]

    def center(self):
        x_center = int(self.x0 + self.x1) / 2
        y_center = int(self.y0 + self.y1) / 2

        return x_center, y_center

    def get_box_coordinates(self):
        return self.x0, self.y0, self.x1, self.y1


class BookInfo(object):
    """
    Information about filmed book
    """
    year: int
    genres: str
    countries: str
    rating: float
    duration: str

    def __init__(self, author: str, book: str):
        self.author = author
        self.book = book

    def __str__(self):
        return f"{self.author} - {self.book}\n{self.genres}\n{self.countries}\n{self.rating}\n"\
               f"{self.duration}\n"

    def get_author_name(self):
        return self.author

    def get_book_name(self):
        return self.book

    def set_year(self, year):
        self.year = year

    def set_genres(self, genres):
        self.genres = genres

    def set_countries(self, countries):
        self.countries = countries

    def set_rating(self, rating):
        self.rating = rating

    def set_duration(self, duration):
        self.duration = duration
