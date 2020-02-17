import codecs
import pandas as pd

def precipitation_txt_to_csv(txtfile, csvfile):
    # Open the .txt file downloaded
    # file = codecs.open(txtfile,"r","utf-8")
    # r = file.readline()
    # file.close()
    
    # Skip the first two rows and set the column names.
    # df = pd.read_fwf(txtfile,index_col = 0)
    df = pd.read_csv(txtfile, sep = ';')

    print('[DATA FRAME] Sum of the RS_IND is: ', df['RS_IND'].sum())
    
    # write csv
    df.to_csv(csvfile, sep = ";")
    return(df)

def station_desc_txt_to_csv(txtfile, csvfile):
    # Open the .txt file downloaded
    file = codecs.open(txtfile,"r","utf-8")
    r = file.readline()
    file.close()
    # Split the text from the first line of the file (columns title)
    colnames_de = r.split()
    
    translate = {'Stations_id':'station_id',
     'von_datum':'date_from',
     'bis_datum':'date_to',
     'Stationshoehe':'altitude',
     'geoBreite': 'latitude',
     'geoLaenge': 'longitude',
     'Stationsname':'name',
     'Bundesland':'state'}
    # Translating the name of the columns from the dictionary created above
    colnames_en = [translate[h] for h in colnames_de]
    
    # Skip the first two rows and set the column names.
    df = pd.read_fwf(txtfile,skiprows=2,names=colnames_en, parse_dates=["date_from","date_to"],index_col = 0)
    
    # write csv
    df.to_csv(csvfile, sep = ";")
    return(df)