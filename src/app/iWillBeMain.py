# from utils.ftpMgmt import gen_df_from_ftp_dir_listing, grabFile
# from utils.textMgmt import station_desc_txt_to_csv, precipitation_txt_to_csv
# from utils.zipMgmt import extract_zip_file, extract_particular_file_zip

# import ftplib
# import pandas as pd
# import time

import os
from utils.ftpConn import initFtpConn, fileDownload
from utils.dfGen import gen_df_stations
from utils.txt2csv import baseName, station_txt_to_csv

# Main
print('[INFO] Starting program...')

# FTP connection parameters
server = "opendata.dwd.de"
usr = "anonymous"
pwd = ""
# FTP directories to access
dwd_dir = "/climate_environment/CDC/observations_germany/climate"
stations_dir = "/daily/kl/historical/"
temperature_dir = "/daily/kl/historical/"
precipitation_dir = "/daily/more_precip/historical/"
# FTP files to access
station_file = "_Beschreibung_Stationen.txt"
targeted_station_file = "stundenwerte_RR_00044_akt.zip"

# Local directories to save the downloaded data
local_t_dir = "data/DWD/" + temperature_dir                                
local_p_dir = "data/DWD/" + precipitation_dir
local_s_dir = "data/DWD/" + "stations/"                                    
# Local directories to save the extracted data
local_t_e_dir = "data/DWD/" + temperature_dir + "extracted_files/"                             
local_p_e_dir = "data/DWD/" + precipitation_dir + "extracted_files/"
# Create the local directories
os.makedirs(local_t_dir,exist_ok = True)                               
os.makedirs(local_p_dir,exist_ok = True)                               
os.makedirs(local_s_dir,exist_ok = True)  
                         
# Connect to the FTP
ftp, res = initFtpConn(server, usr, pwd)

# Obtain the stations of NRW
df_stations = gen_df_stations(ftp, res, dwd_dir + stations_dir) # Create a data frame from the of the files in the directory 
station_fname = df_stations[df_stations['name'].str.contains(station_file)]['name'].values[0] # Find and extract the name of the station file name from the FTP
print('[FTP SESSION] Downloading the file: ' + station_fname + " from FTP directory.")
fileDownload(ftp, dwd_dir + stations_dir + station_fname, local_s_dir + station_fname) # Download the station description file
df_stations = station_txt_to_csv(local_s_dir + station_fname, local_s_dir + baseName(station_fname) + '.csv') # Generate a .csv file of the stations
print('[INFO] KL_Tageswerte_Beschreibung_Stationen file converted to .csv.')
df_stations_filtered =  df_stations[df_stations['state'].str.contains('Nordrhein-Westfalen')] # Filter stations located in NRW from .csv file
df_nrw_stations = df_stations_filtered.to_csv(local_s_dir + baseName(station_fname) + '_NRW' + '.csv', sep = ';') # Generate a .csv file of the NRW stations
print('[INFO] File with the stations of the NRW generated.')


# ARRAY TO FILTER LATER THE STATIONS FILES TO DOWNLOAD
# nrw_stations = []
# for h in range(0,len(df_stations_filtered.index)):
    # nrw_stations.append(df_stations_filtered.index[h])
# print(nrw_stations)


# Program to download the zip files of the preselected stations






## FTP Connection
# ftp = ftplib.FTP(server)
# res = ftp.login(user = user, passwd= pwd)
# print("[FTP SESSION]", res)
## FTP directory into pandas directories
# df_ftpdir = gen_df_from_ftp_dir_listing(ftp, ftp_dir)
# print(df_ftpdir.head(10))
## Dataframe for files with "zip" extension (#USELESS)
# df_zips = df_ftpdir[df_ftpdir['ext'] == '.zip']
# df_zips.set_index("station_id", inplace = True)
# print(df_zips.head(10))
## Download the station description file
# station_fname = df_ftpdir[df_ftpdir['name'].str.contains(station_file)]['name'].values[0]
# print('[DATAFRAME] Grabbing file: ' + station_fname + " from FTP directory.")
# grabFile(ftp_dir + station_fname, local_station_dir + station_fname)
## Transform .txt downloaded file to .csv
# basename = os.path.splitext(station_fname)[0]
# print('[INFO]', basename)
# df_stations = station_desc_txt_to_csv(local_station_dir + station_fname, local_station_dir + basename + '.csv')
# # print(df_stations.head(10))
## Select stations located in NRW from .csv file
# station_ids_selected = df_stations[df_stations['state'].str.contains('Nordrhein-Westfalen')]
# # print('[CSV] Index of stations within the selected area:\n', station_ids_selected.index) 
# # print('[CSV] Amount of stations in the selected area:' , len(station_ids_selected)) 


## Download random zip file (TEST)
# station_fname = df_ftpdir[df_ftpdir['name'].str.contains(targeted_station_file)]['name'].values[0]
# print('[DATAFRAME] Grabbing file: ' + station_fname + " from FTP directory.")
# grabFile(ftp_dir + station_fname, local_station_dir + station_fname)

## Extract zip file
# extract_zip_file(local_station_dir + station_fname, extracted_dir)
# # extract_particular_file_zip(local_station_dir + station_fname, 'produkt_rr_stunde_20180815_20200215_00044.txt')
# precipitation_file = precipitation_txt_to_csv(extracted_dir + 'produkt_rr_stunde_20180815_20200215_00044.txt', extracted_dir + 'produkt_rr_stunde_20180815_20200215_00044.csv')
