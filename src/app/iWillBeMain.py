from utils.ftpMgmt import gen_df_from_ftp_dir_listing, grabFile
from utils.textMgmt import station_desc_txt_to_csv, precipitation_txt_to_csv
from utils.zipMgmt import extract_zip_file, extract_particular_file_zip

import os
import ftplib
import pandas as pd
import time

print('[INFO] Starting program...')

# Connection parameters
server = "opendata.dwd.de"
user = "anonymous"
pwd = ""

# Ftp directory
climate_dir = "/climate_environment/CDC/observations_germany/climate"
topic_dir =  "/hourly/precipitation/recent/"
station_desc_pattern = "_Beschreibung_Stationen.txt"
ftp_dir = climate_dir + topic_dir
targeted_station_file = "stundenwerte_RR_00044_akt.zip"

# Local directories
local_ts_dir = "data/DWD/" + topic_dir                                  # TS stands for "time series". Better add a trailing "/" to make life easier ... 
local_station_dir = local_ts_dir                                        # station info
extracted_dir = local_station_dir + 'extracted_files/'

os.makedirs(local_ts_dir,exist_ok = True)                               # it does not complain if the dir already exists.
os.makedirs(local_station_dir,exist_ok = True)                          # it does not complain if the dir already exists.

# FTP Connection
ftp = ftplib.FTP(server)
res = ftp.login(user = user, passwd= pwd)
print("[FTP SESSION]", res)

# FTP directory into pandas directories
df_ftpdir = gen_df_from_ftp_dir_listing(ftp, ftp_dir)
# print(df_ftpdir.head(10))

# Dataframe for files with "zip" extension 
df_zips = df_ftpdir[df_ftpdir['ext'] == '.zip']
df_zips.set_index("station_id", inplace = True)
# print(df_zips.head(10))

# Download the station description file
station_fname = df_ftpdir[df_ftpdir['name'].str.contains(station_desc_pattern)]['name'].values[0]
# print(station_fname)
print('[DATAFRAME] Grabbing file: ' + station_fname + " from FTP directory.")
grabFile(ftp_dir + station_fname, local_station_dir + station_fname)

# Transform .txt downloaded file to .csv
basename = os.path.splitext(station_fname)[0]
print('[INFO]', basename)
df_stations = station_desc_txt_to_csv(local_station_dir + station_fname, local_station_dir + basename + '.csv')
# print(df_stations.head(10))

# Select stations located in NRW from .csv file
station_ids_selected = df_stations[df_stations['state'].str.contains('Nordrhein-Westfalen')]
# print('[CSV] Index of stations within the selected area:\n', station_ids_selected.index) 
# print('[CSV] Amount of stations in the selected area:' , len(station_ids_selected)) 

# Download random zip file (TEST)
station_fname = df_ftpdir[df_ftpdir['name'].str.contains(targeted_station_file)]['name'].values[0]
print('[DATAFRAME] Grabbing file: ' + station_fname + " from FTP directory.")
grabFile(ftp_dir + station_fname, local_station_dir + station_fname)
# Extract zip file
extract_zip_file(local_station_dir + station_fname, extracted_dir)
# extract_particular_file_zip(local_station_dir + station_fname, 'produkt_rr_stunde_20180815_20200215_00044.txt')
precipitation_file = precipitation_txt_to_csv(extracted_dir + 'produkt_rr_stunde_20180815_20200215_00044.txt', extracted_dir + 'produkt_rr_stunde_20180815_20200215_00044.csv')
