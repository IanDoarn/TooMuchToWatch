from datafilereader import DataFileReader
from media import Movie, Series, Media
from filters import TitleFilter, RatingFilter, GenreFilter

dfr = DataFileReader(r'NetflixUSA_Oct15_cleaned.txt')

filters = [
    [GenreFilter, Series],
    [RatingFilter, '> 4.0']
]

dfr.search(filters=filters)

for line in dfr.master_list:
    print(str(line))
