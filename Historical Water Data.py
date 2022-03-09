import sys
import pandas as pd
import urllib as url
import json
import requests

# Load table of locations and Ids's
Ref = pd.read_excel('C:/Users/Scott/Desktop/Projects/River_Data/RiverReferenceTable.xlsx',
                    dtype={'WaterDischarge': str, 'PHLevel': str,'WaterTemp': str})
sites = Ref.USGS_ID.tolist()
string = ''

for i in sites:
    string = string+','+str(i)
sites=string[1:]

# Metrics to load from stations
# 00060 = discharge
# 00400 = PH level
# 00010 = water temperature
parameters = '00060'+','+'00400'+','+'00010'

# URL to load json of data 
# Use format=rmd for readable URL
link = ('https://waterservices.usgs.gov/nwis/iv/?format=json&sites='+
    sites+'&period=P208W&parameterCd='+
    parameters)

r = requests.get(link)
r.raise_for_status()
data = json.loads(r.text)

#Create empty DataFrame with columns
water = pd.DataFrame(columns=['Name','VariableDescription','Value','DateTime'])

i=0
for items in data['value']['timeSeries']:
    for name in items['sourceInfo']:
        if name == 'siteName':
            # Station name
            names = items['sourceInfo'][name]
    for name in items:
         if name == 'variable':
            # Parameter Description 
            var = items[name]['variableDescription']
    for values in items['values']:
        for v in values['value']:
            # Append values for each column
            water.Name.loc[i] = names
            water.VariableDescription.loc[i] = var
            water.Value.loc[i] = v['value']
            water.DateTime.loc[i] = v['dateTime']
            #print(water.loc[i])
            i=1+i
wt = pd.concat([water.Name,water.VariableDescription,water.Value,water.DateTime],axis=1)

# Break apart Date and Time
dates = [date[0:10] for date in wt.DateTime]
times = [time[11:16] for time in wt.DateTime]
wt['DateTime'] = pd.to_datetime(pd.Series(dates)+' '+pd.Series(times))
wt.Value = wt.Value.astype(float)
wtpp = wt.pivot_table(
                    index='DateTime',
                    columns=['VariableDescription','Name'],
                    values=['Value'])
wt.VariableDescription.loc[
    wt.VariableDescription == 'Discharge, cubic feet per second'] = 'Discharge'
wt.VariableDescription.loc[
    wt.VariableDescription == 'Temperature, water, degrees Celsius'] = 'Temperature'
wt.VariableDescription.loc[
    wt.VariableDescription =='pH, water, unfiltered, field, standard units' ] = 'pH'
import numpy as np
wt = wt.sort_values(['Name','VariableDescription','DateTime'])

dts = pd.Series(pd.to_datetime(wt.DateTime.astype(np.int64).groupby(np.arange(len(wt))//16).mean()))
vals = pd.Series((wt.Value.groupby(np.arange(len(wt))//16).mean()))
ind = pd.Series((pd.Series(wt.index).groupby(np.arange(len(wt))//16).mean()).astype(int))
df = pd.concat([dts,vals,ind],axis=1)
info = wt[['Name','VariableDescription']]
df = pd.merge(df,info,
              left_on=df[0],
              right_on=info.index,how='left')
df = df.drop(columns=['key_0',0])

df.to_csv('C:/Users/Scott/Desktop/Projects/River_Data/Historical River Flows.csv')