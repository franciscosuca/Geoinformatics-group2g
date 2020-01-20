import pandas as pd
import os

print('Starting program...')

# Locating the file to open
cwd = os.getcwd()
files = os.listdir(cwd)

print('\nPATH: ' + cwd + '\n')
print('\nFILES: ')
for x in range(0, len(files)):
        print(files[x])
print('\n')

# Opening the file 
try:

        df = pd.read_csv('german_geo_stations_alter_1.txt', delimiter="\n")
        print(df)
        print('\n')
        # print('Object: ' + df.iloc[1].Stations_id)

except TypeError:
# except:
        print('An error has occured.')
        # print the error here