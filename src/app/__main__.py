import os
from utils.ftpConn import initFtpConn
from utils.data import get_stations_data, get_zip_files, extract_zip_file, clip_files

if __name__ == "__main__":
    pass

# FTP connection parameters
server = "opendata.dwd.de"
usr = "anonymous"
pwd = ""

# FTP directories to access
dwd_dir = "/climate_environment/CDC/observations_germany/climate/"
temperature_stations_dir = "daily/kl/historical/"
temperature_dir = "daily/kl/historical/"
precipitation_stations_dir = "daily/more_precip/historical/"
precipitation_dir = "daily/more_precip/historical/"

# Local directories to save the downloaded data
local_t_dir = "data/DWD/" + temperature_dir                                
local_p_dir = "data/DWD/" + precipitation_dir    
local_ts_dir = "data/DWD/" + temperature_stations_dir + "stations/"  
local_ps_dir = "data/DWD/" + precipitation_stations_dir + "stations/" 
local_t_e_dir = "data/DWD/" + temperature_dir + "unzip_files/"                             
local_p_e_dir = "data/DWD/" + precipitation_dir + "unzip_files/"

print('[INFO] Executing 1st script...')

# Create the local directories
os.makedirs(local_t_dir,exist_ok = True)                               
os.makedirs(local_p_dir,exist_ok = True)
os.makedirs(local_ts_dir,exist_ok = True)  
os.makedirs(local_ps_dir,exist_ok = True)  
                     
# Function to connect to the FTP
ftp, res = initFtpConn(server, usr, pwd)

# Function to obtain temperature & precipitation data from stations that belongs to the NRW
get_stations_data(ftp, res, dwd_dir + temperature_stations_dir, local_ts_dir)
get_stations_data(ftp, res, dwd_dir + precipitation_stations_dir, local_ps_dir)

print('[INFO] Executing 2nd script...')

# Function to download the zip files of the preselected stations from QGIS analysis
temperature_preSelectedStations = [555,617,7374,1078,1590,1303,3321,5064,13901,13670]
precipitation_preSelectedStations = [5733,1999,5502,14175,14177,1590]
temperature_files_names = get_zip_files(ftp, res, dwd_dir + temperature_dir, local_t_dir,temperature_preSelectedStations)
precipitation_files_names = get_zip_files(ftp, res, dwd_dir + precipitation_dir, local_p_dir,precipitation_preSelectedStations)

# Function to unzip the downloaded files and convert them to csv files
extract_zip_file(local_t_dir, local_t_e_dir, temperature_files_names)
extract_zip_file(local_p_dir, local_p_e_dir, precipitation_files_names)

# Files with dates of interest in CSV format
clip_files(local_t_dir, local_t_e_dir, "temperature")
clip_files(local_p_dir, local_p_e_dir, "precipitation")



