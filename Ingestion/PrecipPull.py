# https://towardsdatascience.com/getting-weather-data-in-3-easy-steps-8dc10cc5c859
# https://www.ncdc.noaa.gov/cdo-web/webservices/v2#data
import sys
import requests
import pandas as pd
import json
from datetime import datetime,date, timedelta

print('Precipitation Data Pulling...')

Token = 'ziLDJecqBlvTSNGOzOmPPLmBZtXSfBwR'

referencedata = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/RiverReferenceTable.csv')
referencedata['ZipCode2'] = referencedata['ZipCode'].fillna(0).astype(int)
today = date.today()
Dateslist = [today - timedelta(days = day) for day in range(7)]
startdate = min(Dateslist)
enddate = max(Dateslist)
print(startdate,enddate)
all_data = pd.read_csv('CurrentPrecip.csv',index_col=0).drop_duplicates()

for row in range(0,len(referencedata)):
    print(referencedata.Name[row],' Zip Codes')
    name = referencedata.Name[row]
    zipcode = referencedata.ZipCode[row]
    zipcode2 = referencedata.ZipCode2[row]
    print(zipcode,' ',zipcode2)


    data_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=PRCP&units=metric&limit=1000&locationid=ZIP:'+str(zipcode)+'&startdate='+str(startdate)+'&enddate='+str(enddate)
    
    r = requests.get(data_url, headers={'token':Token})
    d = json.loads(r.text)

    # print(json.dumps(d, indent=4, sort_keys=True))
 
    if len(d) == 0:
        data_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=PRCP&limit=1000&locationid=ZIP:'+str(zipcode2)+'&startdate='+str(startdate)+'&enddate='+str(enddate)
        r = requests.get(data_url, headers={'token':Token})
        d = json.loads(r.text)

    dates = []
    precips = []
    # print(d)
    # break

    #get all items in the response which are precipitation readings
    try:
        precip = [item for item in d['results'] if item['datatype']=='PRCP']
        precips += [item['value'] for item in precip]
        dates += [item['date'] for item in precip]
    except KeyError:
        print('No data available at this Zip Code: ',zipcode2)
        continue

    df = pd.DataFrame()
    df['Date'] = [datetime.strptime(d, '%Y-%m-%dT%H:%M:%S') for d in dates]
    if len(precips) > 0:
        df['Precip'] = [v for v in precips]

    df['Name'] = name
    all_data = all_data.append(df,ignore_index=True)
# print(all_data)
all_data.to_csv('C:/Users/Scott/Desktop/Projects/River_Data/Ingestion/CurrentPrecip.csv')