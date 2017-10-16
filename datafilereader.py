from media import Media, Movie, Series
from filters import Filter, TitleFilter, GenreFilter, RatingFilter, \
    RuntimeFilter, YearFilter
import re

class DataFileReader:

    def __init__(self, file, filters=None):
        self.file = file
        self.filters = filters
        self.master_list = []

    def search(self, filters=None):
        self.master_list = []
        with open(self.file, 'r')as data_file:
            data = data_file.read().splitlines()

        for line in data:
            _line = self.__parse(line)
            if filters is None:
                self.master_list.append(_line)
            else:
                if self.__filter(filters, _line):
                    self.master_list.append(_line)

    @staticmethod
    def __filter(filters, data) -> bool:
        for f in filters:
            try:
                if f[0](data, expression=f[1]).use():
                    pass
                else:
                    return False
            except TypeError as type_error:
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
