from media import Media, Movie, Series
from filters import TitleFilter, GenreFilter, RatingFilter, \
    RuntimeFilter, YearFilter
import re


def create_filters(**kwargs):
    filter_list = []

    title = kwargs.get('title')
    rating = kwargs.get('rating')
    genre = kwargs.get('genre')
    runtime = kwargs.get('runtime')
    year = kwargs.get('year')

    if not any([title, rating, genre, runtime, year]):
        raise KeyError('No valid kwargs supplied.')
    if title is not None:
        filter_list.append([TitleFilter, kwargs['title']])
    if rating is not None:
        filter_list.append([RatingFilter, kwargs['rating']])
    if genre is not None:
        if genre.lower() == 'movie':
            filter_list.append([GenreFilter, Movie])
        elif genre.lower() == 'series':
            filter_list.append([GenreFilter, Series])
        else:
            filter_list.append([GenreFilter, Media])
    if runtime is not None:
        filter_list.append([RuntimeFilter, kwargs['runtime']])
    if year is not None:
        filter_list.append([YearFilter, kwargs['year']])
    return filter_list


class DataFileReader:
    def __init__(self, file, filters=None):
        self.file = file
        self.filters = filters
        self.master_list = []
        self.current_list = None
        self.filter_list = filters
        self.__load()

    def __load(self):
        with open(self.file, 'r')as data_file:
            data = data_file.read().splitlines()
        for line in data:
            self.master_list.append(line)

    def search(self):
        self.current_list = []
        for line in self.master_list:
            _line = self.__parse(line)
            if self.filter_list is None:
                self.current_list.append(_line)
            else:
                if self.__filter(self.filter_list, _line):
                    self.current_list.append(_line)

    def update_filters(self, new_filters):
        if type(self.filter_list) is list:
            self.filter_list.extend(new_filters)
        else:
            self.filter_list = new_filters
        self.search()

    def clear_filters(self):
        self.filter_list = None
        self.search()

    @staticmethod
    def __filter(filters, data) -> bool:
        for f in filters:
            try:
                if f[0](data, expression=f[1]).use():
                    pass
                else:
                    return False
            except TypeError:
                pass
        return True

    def __parse(self, data, pattern=r'^(.*)\s(\(.*\))\s\|\s{3}(.*star.|),(\s.*|)$') -> Media:
        if re.match(pattern, data):
            r = re.search(pattern, data)
            title = r.group(1)
            year = r.group(2)
            length = r.group(4)[1:] if r.group(4) != '' else None
            rating = float(r.group(3).split(' ')[0]) if r.group(3) != '' else None
            genre = self.__get_genre(length)
            if genre == 'Unknown':
                return Media(title, year, length, rating, genre)
            elif genre == 'Movie':
                return Movie(title, year, length, rating, genre)
            elif genre == 'Series':
                return Series(title, year, length, rating, genre)
        else:
            raise ValueError('Invalid input format for data. [{}]'.format(data))

    @staticmethod
    def __get_genre(length):
        if length is None:
            return 'Unknown'
        elif re.match(r'^(\d{1,2}hr\s\d{1,2}m|\d{1,2}hr|\d{1,2}m)$', length):
            return 'Movie'
        elif re.match(r'^(\d{1,3})\s(Season|[eE]pisode|Part|Serie|Collection|Volume|Chapter|Set|Special)[s]?$',
                      length):
            return 'Series'
        else:
            raise ValueError(
                'Length does not match required format [%HH %MM] or [%Episodes \ %Seasons]. Input: {}'.format(
                    length))
