import re
import pandas as pd
import numpy as np
import requests
import json
import time
import datetime as dt

# Functions for Rain types
def LightRain(s):
    if re.search('Slight Chance Rain',s):
        value = 1
    elif re.search('Light Rain',s):
        value = 1  
    else: value = 0
    return value

def Rain(s):
    if re.search('Rain',s): 
        value = 1
    elif re.search('precipitation',s): 
        value = 1
    else: value = 0
    return value

def HeavyRain(s):
    if re.search('Heavy Rain',s):
        value = 1
    else: value = 0
    return value

def Snow(s):
    if re.search('Snow',s):
        value = 1
    else: value = 0
    return value

def WindTranslate(s):
    s = ' '+s
    l = len(s)-4
    value = s[l-2:l]
    return int(value)

def RainCoder(s):
    if s[2] == '1':
        x = 3
    elif s[0] == '1':
        x = 1
    elif s[1] == '1':
        x = 2
    else: x = 0
    return x

# Generalize name options to Today or a weekday
def nameChanger(x):
    if x == 'Sunday Night':
        x = 'Sunday'
    elif x == 'Monday Night':
        x = 'Monday'
    elif x == 'Tuesday Night':
        x = 'Tuesday'
    elif x == 'Wednesday Night':
        x = 'Wednesday'
    elif x == 'Thursday Night':
        x = 'Thursday'
    elif x == 'Friday Night':
        x = 'Friday'
    elif x == 'Saturday Night':
        x = 'Saturday'
    elif x == 'This Afternoon':
        x = 'Today'
    elif x == 'Tonight':
        x = 'Today'

    else: x
    return x

    
print('Forecast Rain Pulling...')
# Parameters
rivers_reference = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/RiverReferenceTable.csv')

sites = rivers_reference.USGS_ID.tolist()
string = ''

for i in sites:
    string = string+','+str(i)
sites=string[1:]

#sites=sites[0:1]

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

    print('Retrieving '+baseStation)
    # Retrieve Forecast for Lat Long Position
    forecast_json = requests.get(json_data['properties']['forecast']).json()
    try: 
        if forecast_json['status'] == 500:
            continue
    except:
        KeyError

    forecast = forecast_json['properties']['periods']
    Forecast_df_temp = pd.DataFrame(forecast)

    # Clean Data
    Forecast_df_temp['startTime'] = pd.to_datetime(Forecast_df_temp.startTime,utc=True).dt.date
    Forecast_df_temp['endTime'] = pd.to_datetime(Forecast_df_temp.endTime,utc=True).dt.date
    Forecast_df_temp['Lat'] = lat
    Forecast_df_temp['Long'] = long
    Forecast_df_temp['Station'] = baseStation
    Forecast_df_temp['WindMph'] = Forecast_df_temp.windSpeed.apply(lambda x: WindTranslate(x))

    # Generalize Name's of Day
    Forecast_df_temp['WeekdayName'] = Forecast_df_temp.name.apply(lambda x: nameChanger(x))
  
    # Create Rain and Snow  Features
    Forecast_df_temp['LightRainFlag'] = Forecast_df_temp.shortForecast.apply(lambda x: LightRain(x))
    Forecast_df_temp['HeavyRainFlag'] = Forecast_df_temp.shortForecast.apply(lambda x: HeavyRain(x))
    Forecast_df_temp['RainFlag'] = Forecast_df_temp.shortForecast.apply(lambda x: Rain(x))
    Forecast_df_temp['SnowFlag'] = Forecast_df_temp.shortForecast.apply(lambda x: HeavyRain(x))
    Forecast_df_temp['RainCode'] = Forecast_df_temp.LightRainFlag.astype(str) + Forecast_df_temp.RainFlag.astype(str) + Forecast_df_temp.HeavyRainFlag.astype(str)
    Forecast_df_temp['Rain'] = Forecast_df_temp.RainCode.apply(lambda x: RainCoder(x))
    
    Forecast_df_temp = Forecast_df_temp[['Station','number','WeekdayName','startTime','endTime'
                                        ,'Rain','SnowFlag','WindMph','windDirection','temperature'
                                        ,'LightRainFlag','RainFlag','HeavyRainFlag','RainCode','shortForecast','detailedForecast','Lat','Long']]

    Forecast_df = Forecast_df.append(Forecast_df_temp,ignore_index=True)
    
    # # Remove Duplicates
    # Forecast_df = Forecast_df.drop_duplicates()


# Transform Data for Loading    
Weather_Forecast = Forecast_df.set_index('Station').join(rivers_reference[['USGS Name','Name']].set_index('USGS Name'))
Weather_Forecast = Weather_Forecast.reset_index().rename(columns={'index':'Station','Name':'StationName'})
Weather_Forecast['Date_Name'] = Weather_Forecast.startTime.astype(str)+'_'+Weather_Forecast.StationName
Weather_Forecast['ForecastFromPresent'] = Weather_Forecast['number']
Weather_Forecast = Weather_Forecast[['StationName','ForecastFromPresent','WeekdayName','startTime','endTime'
                ,'Rain','SnowFlag','WindMph','windDirection','temperature'
                ,'LightRainFlag','RainFlag','HeavyRainFlag','RainCode','shortForecast','detailedForecast','Lat','Long','Date_Name']]

Avgs = Weather_Forecast.groupby('Date_Name').mean()[['Rain','WindMph','temperature','SnowFlag']]
StaticFields = Weather_Forecast.groupby('Date_Name').min()[['ForecastFromPresent','StationName','WeekdayName','startTime','endTime','windDirection']]

Condensed_df = StaticFields.join(Avgs).reset_index().drop_duplicates(subset=['Date_Name'])

# Condensed_df.to_csv('NewWeatherForecast.csv',index=False)

full_df = pd.read_csv('NewWeatherForecast.csv')
full_df.append(Condensed_df).drop_duplicates()[['Date_Name','ForecastFromPresent','StationName','WeekdayName','startTime','endTime','windDirection','Rain','WindMph','temperature','SnowFlag']].to_csv('NewWeatherForecast.csv',index=True)



#OLD - Nov22
# import re
# import pandas as pd
# import numpy as np
# import requests
# import json
# import time
# import datetime as dt

# print('Forecast Rain Pulling...')
# # Parameters
# rivers_reference = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/RiverReferenceTable.csv')

# sites = rivers_reference.USGS_ID.tolist()
# string = ''

# for i in sites:
#     string = string+','+str(i)
# sites=string[1:]

# # URL to load json of data 
# # Use format=rmd for readable URL
# link = ('https://waterservices.usgs.gov/nwis/iv/?format=json&sites='+sites)
# r=requests.get(link)
# Geodata = json.loads(r.text)

# Forecast_df = pd.DataFrame()

# # Gather information from API
# for i in range(len(Geodata['value']['timeSeries'])):
#     lat = str(Geodata['value']['timeSeries'][i]['sourceInfo']['geoLocation']['geogLocation']['latitude'])
#     long = str(Geodata['value']['timeSeries'][i]['sourceInfo']['geoLocation']['geogLocation']['longitude'])
#     baseStation = Geodata['value']['timeSeries'][i]['sourceInfo']['siteName']
#     # Search API for Lat Long Position
#     r = requests.get('https://api.weather.gov/points/'+lat+','+long)
#     json_data = r.json()

#     # Retrieve Forecast for Lat Long Position
#     forecast_json = requests.get(json_data['properties']['forecast']).json()
#     try: 
#         if forecast_json['status'] == 500:
#             continue
#     except:
#         KeyError

#     forecast = forecast_json['properties']['periods']
#     Forecast_df_temp = pd.DataFrame(forecast).drop(columns='number')
#     Forecast_df_temp['Lat'] = lat
#     Forecast_df_temp['Long'] = long

#     Forecast_df_temp['Station'] = baseStation
#     Forecast_df = Forecast_df.append(Forecast_df_temp,ignore_index=True)

#     # Cleaning DataFrame
#     df = Forecast_df.drop_duplicates()
#     df.startTime = pd.to_datetime(df.startTime,utc=True)
#     df.endTime = pd.to_datetime(df.endTime,utc=True)
#     df.drop(columns=['temperatureTrend','icon'],inplace=True)



# # Functions for Rain types
# def LightRain(s):
#     if re.search('Slight Chance Rain',s):
#         value = 1
#     elif re.search('Light Rain',s):
#         value = 1  
#     else: value = 0
#     return value

# def Rain(s):
#     if re.search('Rain Showers',s):
#         value = 1
#     else: value = 0
#     return value

# def HeavyRain(s):
#     if re.search('Heavy Rain',s):
#         value = 1
#     else: value = 0
#     return value

# def WindTranslate(s):
#     s = ' '+s
#     l = len(s)-4
#     value = s[l-2:l]
#     return int(value)
    
# # Create Rain Boolean Features
# df['LightRain'] = df.shortForecast.apply(lambda x: LightRain(x))
# df['Rain'] = df.shortForecast.apply(lambda x: Rain(x))
# df['HeavyRain'] = df.shortForecast.apply(lambda x: HeavyRain(x))
# df['WindMph'] = df.windSpeed.apply(lambda x: WindTranslate(x))

# # Create final Dataframe with Key
# WeatherForecast = df[['Station','name','startTime','endTime','temperature','windDirection','WindMph','LightRain','Rain','HeavyRain']]
# WeatherForecast = WeatherForecast.set_index('Station').join(rivers_reference[['USGS Name','Name']].set_index('USGS Name'))
# WeatherForecast = WeatherForecast.reset_index().rename(columns={'index':'Station','Name':'StationName'})
# WeatherForecast['Date_Name'] = WeatherForecast.startTime.dt.date.astype(str)+'_'+WeatherForecast.StationName

# # WeatherForecast.to_csv('WeatherForecast.csv',index=False)
# full_df = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/Exploration/WeatherForecast.csv')
# full_df.append(WeatherForecast).drop_duplicates()[['Station','name','startTime','endTime','temperature','windDirection','WindMph','LightRain','Rain','HeavyRain','StationName','Date_Name']].to_csv('WeatherForecast.csv')