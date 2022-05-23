import pandas as pd
import urllib as url
import numpy as np
import json
import requests
import sys

# Load table of locations and Ids's
Ref = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/RiverReferenceTable.csv',
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
        sites+'&period=P20D&parameterCd='+
        parameters)
r=requests.get(link)
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
            water.loc[i] = [names,var,v['value'],v['dateTime']]
            i=1+i


# Break apart Date and Time
dates = [date[0:10] for date in water.DateTime]
times = [time[11:16] for time in water.DateTime]
water['DateTime'] = pd.to_datetime(pd.Series(dates)+' '+pd.Series(times))
water.Value = water.Value.astype(float)
waterpp = water.pivot_table(
                    index='DateTime',
                    columns=['VariableDescription','Name'],
                    values=['Value'])
water.VariableDescription.loc[
    water.VariableDescription == 'Discharge, cubic feet per second'] = 'Discharge'
water.VariableDescription.loc[
    water.VariableDescription == 'Temperature, water, degrees Celsius'] = 'Temperature'
water.VariableDescription.loc[
    water.VariableDescription =='pH, water, unfiltered, field, standard units' ] = 'pH'
water = water.sort_values(['Name','VariableDescription','DateTime'])

dts = pd.Series(pd.to_datetime(water.DateTime.astype(np.int64).groupby(np.arange(len(water))//16).mean()))
vals = pd.Series((water.Value.groupby(np.arange(len(water))//16).mean()))
ind = pd.Series((pd.Series(water.index).groupby(np.arange(len(water))//16).mean()).astype(int))
df = pd.concat([dts,vals,ind],axis=1)
info = water[['Name','VariableDescription']]
df = pd.merge(df,info,
              left_on=df[0],
              right_on=info.index,how='left')
df = df.drop(columns=['key_0',0])

full_df = pd.read_csv('CurrentWater.csv')
full_df = full_df.append(df)
full_df = full_df[['DateTime','Value','Name','VariableDescription']]
full_df.drop_duplicates(inplace=True)
full_df[['DateTime','Value','Name','VariableDescription']].to_csv('CurrentWater.csv',index=False)