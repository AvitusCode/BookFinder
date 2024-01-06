

class User(object):
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.years: str  # year-year
        self.genres: str
        self.countries: str
        self.rating: str
        self.duration: str  # diap in minutes

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
