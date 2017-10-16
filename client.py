from datafilereader import DataFileReader, create_filters

dfr = DataFileReader(r'NetflixUSA_Oct15_cleaned.txt',
                     filters=create_filters(
                         genre='movie',
                         title='cool',
                         year='> 1999',
                         rating='> 3.5',
                         runtime='== 60'
                     ))
dfr.search()

for i, line in enumerate(dfr.current_list):
    print(i + 1, ':', str(line))
