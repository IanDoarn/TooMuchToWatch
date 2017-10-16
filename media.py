import re


class Media:
    def __init__(self, title, year, length, rating, genre):
        self.title = title
        self.year = self.__get_year(year)
        self.length = length
        self.rating = rating
        self.genre = genre
        self.runtime = self.__get_runtime(length)

    def __get_year(self, year):
        if re.match(r'^\((\d{4}|\d{4}-\d{4})\)$', year):
            r = re.search(r'^\((\d{4}|\d{4}-\d{4})\)$', year)
            if len(r.groups()) == 1:
                return [r.group(1)]
            return list(r.groups()[1:])

    def __get_runtime(self, length):
        if length is not None:
            try:
                if re.match(r'^(\d{1,2}hr\s\d{1,2}m)$', length):
                    r = re.search(r'^(\d{1,2}hr)\s(\d{1,2}m)$', length)
                    hour = int(r.group(1)[:-2])
                    minute = int(r.group(2)[:-1])
                    return (hour * 60) + minute
                elif re.match(r'^(\d{1,2}hr)$', length):
                    return int(length[:-2]) * 60
                elif re.match(r'^(\d{1,3}m)$', length):
                    return int(length[:-1])
                else:
                    return None
            except TypeError as error:
                print(error, str(self))
        else:
            return None

    def __str__(self):
        return "Title: {} | Year: {} | Rating: {} stars | Length: {}m".format(
            self.title, self.year, self.rating, self.length
        )


class Series(Media):

    def __init__(self, title, year, length, rating, genre):
        super(Series, self).__init__(title, year, length, rating, genre)
        self.genre = 'Series'
        self.series_type = length.split(' ')[1]

    def __str__(self):
        return "Title: {} | Year: {} | Rating: {} stars | Length: {}m | Genre: {} | Type: {}".format(
            self.title, self.year, str(self.rating), str(self.length), self.genre, self.series_type
        )


class Movie(Media):

    def __init__(self, title, year, length, rating, genre):
        super(Movie, self).__init__(title, year, length, rating, genre)
        self.genre = 'Movie'

    def __str__(self):
        return "Title: {} | Year: {} | Rating: {} stars | Length: {}m | Genre: {}".format(
            self.title, self.year, str(self.rating), str(self.length), self.genre
        )
