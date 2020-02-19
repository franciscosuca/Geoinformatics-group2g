import ftplib

# Initiate FTP connection
def initFtpConn(server, usr, pwd):
    ftp = ftplib.FTP(server)
    res = ftp.login(user = usr, passwd= pwd)
    return ftp, res

# Donwload a file from the FTP
def fileDownload(ftp, fileDirName, localDirName):
    try:
        ftp.cwd(".") # Checking connection to the FTP
        localfile = open(localDirName, 'wb')
        ftp.retrbinary('RETR ' + fileDirName, localfile.write, 1024) # Retrieve a file in binary transfer mode.
        localfile.close()
        print('[FTP SESSION] File donwloaded successfully.')
    
    except ftplib.error_perm:
        print("[FTP ERROR] Operation not permitted or file not found or not logged in.")

    except ftplib.error_temp:
        print("[FTP ERROR] Timeout.")

    except ConnectionAbortedError:
        print("[FTP ERROR] Connection aborted.")