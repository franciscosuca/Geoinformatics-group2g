import codecs
import pandas as pd
import os

def baseName(name):
    return os.path.splitext(name)[0]

def kl_txt_to_csv(txtfile, csvfile):
    df = pd.read_csv(txtfile, sep = ';')

    month_values = []
    year_values = []
    station_values = []
    temperature_values = []
    precipitation_values = []
    index = 0

    # Filter data according to the dates needed for the analysis
    for x in df['MESS_DATUM']:
        # if((x >= 20150509 and x <= 20160508) or (x >= 20160527 and x <= 20170526) or (x >= 20170701 and x <= 20180630)):  #case 2
        # if((x >= 20160320 and x <= 20160508) or (x >= 20170320 and x <= 20170526) or (x >= 20180320 and x <= 20180630)):    #case 3
        if((x >= 20160409 and x <= 20160508) or (x >= 20170427 and x <= 20170526) or (x >= 20180601 and x <= 20180630)):  #case 4
            month_value = x
            month_values.append(month_value)
            # if(x >= 20150509 and x <= 20160508):  #case 2
            # if(x >= 20160320 and x <= 20160508):    #case 3
            if(x >= 20160409 and x <= 20160508):  #case 4
                year_value = 2016
                year_values.append(year_value)
            # elif(x >= 20160527 and x <= 20170526):    #case 2
            # elif(x >= 20170320 and x <= 20170526):      #case 3
            elif(x >= 20170427 and x <= 20170526):    #case 4
                year_value = 2017
                year_values.append(year_value)
            # elif(x >= 20170701 and x <= 20180630):    #case 2
            # elif(x >= 20180320 and x <= 20180630):      #case 3
            elif(x >= 20180601 and x <= 20180630):    #case 4
                year_value = 2018
                year_values.append(year_value)
            station_value = df['STATIONS_ID'][index]
            station_values.append(station_value)
            precipitation_value = df[' RSK'][index]
            precipitation_values.append(precipitation_value)
            temperature_value = df[' TMK'][index]
            temperature_values.append(temperature_value)
        index = index + 1

    # Prepare data for new data frame
    data = {'Month_dates': month_values, 'year': year_values,'stationID': station_values, 'precipitation': precipitation_values,'temperature': temperature_values}
    dfn = pd.DataFrame(data)

    # write csv
    dfn.to_csv(csvfile, sep = ";")

def rs_txt_to_csv(txtfile, csvfile):
    df = pd.read_csv(txtfile, sep = ';')

    month_values = []
    year_values = []
    station_values = []
    precipitation_values = []
    index = 0

    # Filter data according to the dates needed for the analysis
    for x in df['MESS_DATUM']:
        # if((x >= 20150509 and x <= 20160508) or (x >= 20160527 and x <= 20170526) or (x >= 20170701 and x <= 20180630)):  #case 2
        # if((x >= 20160320 and x <= 20160508) or (x >= 20170320 and x <= 20170526) or (x >= 20180320 and x <= 20180630)):    #case 3
        if((x >= 20160409 and x <= 20160508) or (x >= 20170427 and x <= 20170526) or (x >= 20180601 and x <= 20180630)):  #case 4
            month_value = x
            month_values.append(month_value)
            # if(x >= 20150509 and x <= 20160508):  #case 2
            # if(x >= 20160320 and x <= 20160508):    #case 3
            if(x >= 20160409 and x <= 20160508):  #case 4
                year_value = 2016
                year_values.append(year_value)
            # elif(x >= 20160527 and x <= 20170526):    #case 2
            # elif(x >= 20170320 and x <= 20170526):      #case 3
            elif(x >= 20170427 and x <= 20170526):    #case 4
                year_value = 2017
                year_values.append(year_value)
            # elif(x >= 20170701 and x <= 20180630):    #case 2
            # elif(x >= 20180320 and x <= 20180630):      #case 3
            elif(x >= 20180601 and x <= 20180630):    #case 4
                year_value = 2018
                year_values.append(year_value)
            station_value = df['STATIONS_ID'][index]
            station_values.append(station_value)
            precipitation_value = df['  RS'][index]
            precipitation_values.append(precipitation_value)
        index = index + 1

    # Prepare data for new data frame
    data = {'Month_dates': month_values, 'year': year_values,'stationID': station_values, 'precipitation': precipitation_values}
    dfn = pd.DataFrame(data)
    
    # write csv
    dfn.to_csv(csvfile, sep = ";")
    return(df)

def station_txt_to_csv(txtfile, csvfile):
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