
from utils.ftpConn import fileDownload
from utils.dfGen import gen_df_stations
from utils.txt2csv import baseName, station_txt_to_csv, kl_txt_to_csv, rs_txt_to_csv
from zipfile import ZipFile
import os

# FTP files to access
station_file = "_Beschreibung_Stationen.txt"

def get_stations_data(ftp, res, remoteDir, localDir):
    # Create a data frame from the files in the directory 
    df_stations = gen_df_stations(ftp, res, remoteDir) 
    # Find and extract the name of the station file name from the FTP
    station_fname = df_stations[df_stations['name'].str.contains(station_file)]['name'].values[0] 
    print('[FTP SESSION] Downloading the file: ' + station_fname + " from FTP directory.")
    # Download the station description file
    fileDownload(ftp, remoteDir + station_fname, localDir + station_fname) 
    # Generate a .csv file of the stations
    df_stations = station_txt_to_csv(localDir + station_fname, localDir + baseName(station_fname) + '.csv') 
    print('[INFO] KL_Tageswerte_Beschreibung_Stationen file converted to .csv.')
    # Filter stations located in NRW from .csv file
    df_stations_filtered =  df_stations[df_stations['state'].str.contains('Nordrhein-Westfalen')] 
    # Generate a .csv file of the NRW stations
    df_stations_filtered.to_csv(localDir + baseName(station_fname) + '_NRW' + '.csv', sep = ';') 
    print('[INFO] File with the stations of the NRW generated.')

def get_zip_files(ftp, res, remoteDir, localDir, preSelectedStations):
    # Create a data frame from the files in the directory 
    df_stations = gen_df_stations(ftp, res, remoteDir) 
    stations_id_from_directory = df_stations['station_id']
    preSelectedStations_names = []
    # Find and extract the id of the stations pre-selected
    for targeStation in preSelectedStations:
        for station in range (0, len(stations_id_from_directory)):
            if(df_stations['station_id'][station] == targeStation):
                print('[FTP SESSION] Station ', targeStation ,' found. File name related is: ', df_stations['name'][station])
                preSelectedStations_names.append(df_stations['name'][station])
    # Download the stations found on the server
    for targeStation in preSelectedStations_names:
        fileDownload(ftp, remoteDir + targeStation, localDir + targeStation) 

    return preSelectedStations_names

def extract_zip_file(inputPath, outputPath, preSelectedStations):
    for targeStation in preSelectedStations:
        with ZipFile(inputPath + targeStation, 'r') as zip:
            print('[ZIP] Extracting', targeStation)
            zip.extractall(path = outputPath)
            print('[ZIP] Extraction completed.')

def clip_files(localDir, localDir_unzip, climatic_var):
    climatic_files = []
    unzip_files = os.listdir(localDir_unzip)
    for unzip_file in unzip_files:
        if(unzip_file[0:19] == 'produkt_nieder_tag_'):
            climatic_files.append(unzip_file)
    for climatic_file in range (0, len(climatic_files)):
        if (climatic_var == 'temperature'):
            kl_txt_to_csv(localDir_unzip + climatic_files[climatic_file], localDir + climatic_files[climatic_file] + '.csv')
        elif(climatic_var == 'precipitation'):
            rs_txt_to_csv(localDir_unzip + climatic_files[climatic_file], localDir + climatic_files[climatic_file] + '.csv')
    print('[INFO] Stations files generated.')