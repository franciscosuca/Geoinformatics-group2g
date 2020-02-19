import os
import pandas as pd
        
# Generate Pandas Dataframe from the list of stations on the FTP directory
def gen_df_stations(ftp, res, ftpdir):
    lines = []
    flist = []
    try:    
        res = ftp.retrlines("LIST " + ftpdir, lines.append) # Retrieve a file or directory listing in ASCII transfer mode.
        print("[FTP SESSION] Files on directory: ", res)
    except:
        print("[FTP ERROR] ftp.retrlines() failed.")
        return  
    if len(lines) == 0:
        print("[FTP ERROR] ftp dir is empty.")
        return
    for line in lines:
        [ftype, fsize, fname] = [line[0:1], int(line[31:42]), line[56:]]
        fext = os.path.splitext(fname)[-1] # .zip
        if fext == ".zip":
            station_id = int(fname.split("_")[2]) # Station number (i.e. 1500)
        else:
            station_id = "na"
        flist.append([station_id, fname, fext, fsize, ftype])
    
    df = pd.DataFrame(flist,columns=["station_id", "name", "ext", "size", "type"])
    return(df)