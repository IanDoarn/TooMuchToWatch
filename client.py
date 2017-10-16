from datafilereader import DataFileReader, create_filters

dfr = DataFileReader(r'NetflixUSA_Oct15_cleaned.txt',
                     filters=create_filters(
                         genre='movie',
                         title='cat',
                         year='> 1999'
                     ))
dfr.search()

for i, line in enumerate(dfr.current_list):
    print(i + 1, str(line))
