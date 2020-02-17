from zipfile import ZipFile

def extract_zip_file(fileName, pathName):
    with ZipFile(fileName, 'r') as zip:
        # print('[ZIP] Files within the zip:')
        # zip.printdir()
        print('[ZIP] Extracting files...')
        zip.extractall(path = pathName)
        print('[ZIP] Extraction completed.')

def extract_particular_file_zip(fileName, eFileName):
    with ZipFile(fileName, 'r') as zip:
        # print('[ZIP] Files within the zip:')
        # zip.printdir()
        print('[ZIP] Extracting files...')
        zip.extract(eFileName)
        print('[ZIP] Extraction completed.')