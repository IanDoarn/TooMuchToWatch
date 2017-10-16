import re
from media import Media


class Filter:
    def __init__(self, data: Media, expression=None):
        """

        :type data: object
        """
        self.data = data
        self.expression = expression

    def __contains__(self, item):
        pass

    def __eq__(self, other):
        pass

    def use(self, *args, **kwargs):
        pass


class TitleFilter(Filter):
    def __init__(self, data, expression=None):
        super(TitleFilter, self).__init__(data, expression=expression)
        self.title = self.data.title
        self.string = expression

    def __contains__(self, string):
        return len(re.findall(r'(?i)(?:^|\W){}(?:$|\W)'.format(string), self.title)) > 0

    def use(self):
        return self.__contains__(self.string)


class GenreFilter(Filter):
    def __init__(self, data, expression=None):
        super(GenreFilter, self).__init__(data, expression=expression)
        self.genre = expression

    def __eq__(self, other):
        return isinstance(self.data, other)

    def use(self):
        return self.__eq__(self.genre)


class RatingFilter(Filter):
    def __init__(self, data, expression=None):
        super(RatingFilter, self).__init__(data, expression=expression)
        self.rating = self.data.rating

        if self.rating is None:
            raise TypeError('{} {} does not have a rating.'.format(
                self.data.title, self.data.year
            ))

    def compare(self):
        """
        Evaluate a comparison using given expression
        
        :return: bool
        """
        return eval("{}{}".format(str(self.rating), self.expression))

    def use(self):
        return self.compare()


class YearFilter(Filter):
    def __init__(self, data, expression=None):
        super(YearFilter, self).__init__(data, expression=expression)
        self.year = self.data.year

    def compare(self):
        """
        Evaluate a comparison using given expression

        :return: bool
        """
        return eval("{}{}".format(str(self.year[0]), self.expression))

    def use(self):
        return self.compare()


class RuntimeFilter(Filter):
    def __init__(self, data, expression=None):
        super(RuntimeFilter, self).__init__(data, expression=expression)
        self.runtime = self.data.runtime

    def compare(self):
        """
        Evaluate a comparison using given expression

        :return: bool
        """
        return eval("{}{}".format(str(self.runtime), self.expression))

    def use(self):
        return self.compare()
