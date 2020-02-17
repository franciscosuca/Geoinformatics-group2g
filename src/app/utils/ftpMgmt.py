import os
import pandas as pd
import ftplib

# Connection parameters
server = "opendata.dwd.de"
user = "anonymous"
pwd = ""

# FTP Connection
ftp = ftplib.FTP(server)
res = ftp.login(user = user, passwd= pwd)

# Donwload a txt file
def grabFile(ftpfullname, localfullname):

    try:
        ret = ftp.cwd(".")
        # ftp.retrlines('LIST')                                              # A dummy action to chack the connection and to provoke an exception if necessary.
        localfile = open(localfullname, 'wb')
        ftp.retrbinary('RETR ' + ftpfullname, localfile.write, 1024)    # Retrieve a file in binary transfer mode.
        localfile.close()
    
    except ftplib.error_perm:
        print("[FTP ERROR] Operation not permitted or file not found or not logged in.")

    except ftplib.error_temp:
        print("[FTP ERROR] Timeout.")

    except ConnectionAbortedError:
        print("[FTP ERROR] Connection aborted.")
        
# Generate Pandas Dataframe from FTP directory
def gen_df_from_ftp_dir_listing(ftp, ftpdir):
    lines = []
    flist = []
    try:    
        res = ftp.retrlines("LIST " + ftpdir, lines.append)               # Retrieve a file or directory listing in ASCII transfer mode.
        print("[FTP SESSION]", res)
    except:
        print("[FTP ERROR] ftp.retrlines() failed. ftp timeout? Reconnect!")
        return  
    if len(lines) == 0:
        print("[FTP ERROR] ftp dir is empty")
        return
    for line in lines:
        # print(line[56:])
        [ftype, fsize, fname] = [line[0:1], int(line[31:42]), line[56:]]
        # itemlist = [line[0:1], int(line[31:42]), line[56:]]
        # flist.append(itemlist)
        fext = os.path.splitext(fname)[-1]                              # .zip
        # print(fext)
        if fext == ".zip":
            station_id = int(fname.split("_")[2])                   # Station number (i.e. 1500)
            # print(fname, station_id)
        else:
            station_id = "na"
        flist.append([station_id, fname, fext, fsize, ftype])
    
    df_ftpdir = pd.DataFrame(flist,columns=["station_id", "name", "ext", "size", "type"])
    return(df_ftpdir)

# next function