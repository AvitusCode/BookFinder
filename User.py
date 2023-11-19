

class User(object):

    years: str  # year-year
    genres: str
    countries: str
    rating: str
    duration: str  # diap in minutes

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __str__(self):
        return f"{self.name}\nUserId: {self.user_id}\nPreferences:\nGenres:{self.genres}\nCountries{self.countries}\n" \
               f"Rating:{self.rating}\n" \
               f"Year:{self.years}\nDuration:{self.duration}\n"

    def data_to_dict(self):
        return {
            "years": self.years,
            "genres": self.genres,
            "countries": self.countries,
            "rating": self.rating,
            "duration": self.duration
        }

    def in_years(self, year):
        a, b = self.years.split("-")
        if int(a) <= year <= int(b):
            return 1
        else:
            return -1

    def in_rating(self, rating):
        a, b = self.rating.split("-")
        if float(a) <= rating <= float(b):
            return 1
        else:
            return -1

    def in_duration(self, duration):
        a, b = self.duration.split("-")
        if int(a) <= duration <= int(b):
            return 1
        else:
            return -1

    def in_countries(self, countries):
        data = self.countries.split(" ")
        data = [word.lower() for word in data]
        match = 0
        for country in countries:
            if country.lower() in data:
                match += 1
            else:
                match -= 1
        return match

    def in_genres(self, genres):
        data = self.genres.split(" ")
        data = [word.lower() for word in data]
        match = 0
        for genre in genres:
            if genre.lower() in data:
                match += 1
            else:
                match -= 1
        return match


