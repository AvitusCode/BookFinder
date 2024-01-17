import os
import time
import xml.etree.ElementTree as xml
import requests
import json
import decimal
import sys


# API for the data extraction from this resource: https://kinopoiskapiunofficial.tech


def rank_to_float(rank):
    decimal_value = decimal.Decimal(rank)
    decimal_value = decimal_value.quantize(decimal.Decimal(f"0.{'0' * 1}"))
    return float(decimal_value)


class FILM:
    def __init__(self, input_data: dict):
        data = input_data['data']
        self.kp_id = data['filmId']
        self.name = data['nameRu'] if data['nameEn'] == '' else data['nameEn']
        self.ru_name = data['nameRu']
        self.year = data['year'].split('-')[0] if data['type'] != 'FILM' else data['year']
        self.duration = data['filmLength']
        self.tagline = data['slogan'] if data['slogan'] is not None else '-'
        self.description = data['description']
        self.genres = [genre['genre'] for genre in data['genres']]
        self.countries = [country['country'] for country in data['countries']]
        self.age_rating = data['ratingAgeLimits']
        self.kp_rate = rank_to_float(input_data['ratingKinopoisk'])
        self.imdb_rate = rank_to_float(input_data['ratingImdb'])
        self.kp_url = data['webUrl']
        self.poster = data['posterUrl']
        self.poster_preview = data['posterUrlPreview']


class SEARCH:
    def __init__(self, data: dict, is_film: bool = False, raiting = '0.0'):
        self.kp_id = data['filmId']
        self.name = data['nameRu'] if data['nameEn'] == '' else data['nameEn']
        self.ru_name = data['nameRu']
        self.year = data['year'].split('-')[0] if not is_film else data['year']
        self.duration = data['filmLength']
        self.genres = [genre['genre'] for genre in data['genres']]
        self.countries = [country['country'] for country in data['countries']]
        self.kp_rate = rank_to_float(data['rating'] if not is_film else raiting)
        self.kp_url = f'https://www.kinopoisk.ru/film/{data["filmId"]}/'
        self.poster = data['posterUrl']
        self.poster_preview = data['posterUrlPreview']


class KP:
    def __init__(self, token, tries):
        self.token = token
        self.tries = tries
        self.headers = {'X-API-KEY': self.token, 'Content-Type': 'application/json'}
        self.api_version = 'v2.1'
        self.API = 'https://kinopoiskapiunofficial.tech/api/' + self.api_version + '/'
        self.version = self.api_version + '.2-release'
        self.about = 'KinoPoiskAPI'

    def get_film_by_id(self, film_id):
        cache = CACHE('FIND').load()

        if str(film_id) in cache:
            print('film was founded in cache!')
            data = {}
            for a in cache[str(film_id)]:
                data[a] = cache[str(film_id)][a]
            return FILM(data)

        request = requests.get(f'https://rating.kinopoisk.ru/{film_id}.xml')
        kp_rate = 0
        imdb_rate = 0

        if not self.is_request_failed(request):
            rate_request = request.text
            try:
                kp_rate = xml.fromstring(rate_request)[0].text
            except IndexError:
                kp_rate = 0
            try:
                imdb_rate = xml.fromstring(rate_request)[1].text
            except IndexError:
                imdb_rate = 0

        for _ in range(self.tries):
            try:
                request = requests.get(self.API + 'films/' + str(film_id), headers=self.headers)

                if self.is_request_failed(request):
                    time.sleep(0.5)
                    continue

                request_json = json.loads(request.text)
                request_json['ratingKinopoisk'] = kp_rate
                request_json['ratingImdb'] = imdb_rate
                cache[str(film_id)] = request_json

                CACHE('FIND').write(cache)
                return FILM(request_json)
            except (json.decoder.JSONDecodeError, KeyError):
                print('catch exception wile parsing film info')
                sys.exit(-1)

    def search_by_keywords(self, query):
        for _ in range(self.tries):
            try:
                request = requests.get(self.API + 'films/search-by-keyword', headers=self.headers,
                                       params={"keyword": query, "page": 1})

                if self.is_request_failed(request):
                    time.sleep(0.5)
                    continue

                request_json = json.loads(request.text)
                output = []
                for film in request_json['films']:
                    try:
                        output.append(SEARCH(film))
                    except (Exception, BaseException):
                        continue

                cache = CACHE('FIND').load()
                for film in cache:
                    if str(cache[str(film)]['data']['nameRu']).strip() == str(query).strip():
                        output.append(SEARCH(cache[str(film)]['data'], is_film=True, raiting=cache[str(film)]['ratingKinopoisk']))

                return output
            except (json.decoder.JSONDecodeError, KeyError):
                print('catch exception wile parsing film info')
                sys.exit(-1)

        print('Search request timeout')
        return None

    @staticmethod
    def is_request_failed(req):
        if req.status_code != 200:
            print("Request error, status={}".format(req.status_code))
            return True
        elif req.status_code == 402:
            print("To much requests for this day!")
            return True
        return False


class CACHE:
    json_buffer = {}

    def __init__(self, cache_type: str):
        self.PATH = os.path.dirname(os.path.abspath(__file__))
        self.path_to_file = ''

        if cache_type == 'FIND':
            self.path_to_file = '/res/cache_find.json'
        elif cache_type == 'SEARCH':
            self.path_to_file = '/res/cache_search.json'
        else:
            raise ValueError('Invalid cache type argument in the film_info API')

    def load(self) -> dict:
        try:
            with open(self.PATH + self.path_to_file, 'r', encoding='utf-8') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            with open(self.PATH + self.path_to_file, 'w', encoding='utf-8') as f:
                f.write('{}')
                return {}

    def append(self, json_object):
        self.json_buffer.update(json_object)

    def flush(self):
        self.write(self.json_buffer)

    def write(self, cache: dict, indent: int = 4):
        with open(self.PATH + self.path_to_file, 'w', encoding='utf-8') as f:
            if len(cache) == 0:
                return None
            return json.dump(cache, f, indent=indent)
