import re
import pandas as pd
import numpy as np
import requests
import json
import time
import datetime as dt

print('Forecast Rain Pulling...')
# Parameters
rivers_reference = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/RiverReferenceTable.csv')

sites = rivers_reference.USGS_ID.tolist()
string = ''

for i in sites:
    string = string+','+str(i)
sites=string[1:]

# URL to load json of data 
# Use format=rmd for readable URL
link = ('https://waterservices.usgs.gov/nwis/iv/?format=json&sites='+sites)
r=requests.get(link)
Geodata = json.loads(r.text)

Forecast_df = pd.DataFrame()

# Gather information from API
for i in range(len(Geodata['value']['timeSeries'])):
    lat = str(Geodata['value']['timeSeries'][i]['sourceInfo']['geoLocation']['geogLocation']['latitude'])
    long = str(Geodata['value']['timeSeries'][i]['sourceInfo']['geoLocation']['geogLocation']['longitude'])
    baseStation = Geodata['value']['timeSeries'][i]['sourceInfo']['siteName']
    # Search API for Lat Long Position
    r = requests.get('https://api.weather.gov/points/'+lat+','+long)
    json_data = r.json()

    # Retrieve Forecast for Lat Long Position
    forecast_json = requests.get(json_data['properties']['forecast']).json()
    try: 
        if forecast_json['status'] == 500:
            continue
    except:
        KeyError

    forecast = forecast_json['properties']['periods']
    Forecast_df_temp = pd.DataFrame(forecast).drop(columns='number')
    Forecast_df_temp['Lat'] = lat
    Forecast_df_temp['Long'] = long

    Forecast_df_temp['Station'] = baseStation
    Forecast_df = Forecast_df.append(Forecast_df_temp,ignore_index=True)

    # Cleaning DataFrame
    df = Forecast_df.drop_duplicates()
    df.startTime = pd.to_datetime(df.startTime,utc=True)
    df.endTime = pd.to_datetime(df.endTime,utc=True)
    df.drop(columns=['temperatureTrend','icon'],inplace=True)



# Functions for Rain types
def LightRain(s):
    if re.search('Slight Chance Rain',s):
        value = 1
    elif re.search('Light Rain',s):
        value = 1  
    else: value = 0
    return value

def Rain(s):
    if re.search('Rain Showers',s):
        value = 1
    else: value = 0
    return value

def HeavyRain(s):
    if re.search('Heavy Rain',s):
        value = 1
    else: value = 0
    return value

def WindTranslate(s):
    s = ' '+s
    l = len(s)-4
    value = s[l-2:l]
    return int(value)
    
# Create Rain Boolean Features
df['LightRain'] = df.shortForecast.apply(lambda x: LightRain(x))
df['Rain'] = df.shortForecast.apply(lambda x: Rain(x))
df['HeavyRain'] = df.shortForecast.apply(lambda x: HeavyRain(x))
df['WindMph'] = df.windSpeed.apply(lambda x: WindTranslate(x))

# Create final Dataframe with Key
WeatherForecast = df[['Station','name','startTime','endTime','temperature','windDirection','WindMph','LightRain','Rain','HeavyRain']]
WeatherForecast = WeatherForecast.set_index('Station').join(rivers_reference[['USGS Name','Name']].set_index('USGS Name'))
WeatherForecast = WeatherForecast.reset_index().rename(columns={'index':'Station','Name':'StationName'})
WeatherForecast['Date_Name'] = WeatherForecast.startTime.dt.date.astype(str)+'_'+WeatherForecast.StationName

# WeatherForecast.to_csv('WeatherForecast.csv',index=False)
full_df = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/Exploration/WeatherForecast.csv')
full_df.append(WeatherForecast).drop_duplicates()[['Station','name','startTime','endTime','temperature','windDirection','WindMph','LightRain','Rain','HeavyRain','StationName','Date_Name']].to_csv('WeatherForecast.csv')