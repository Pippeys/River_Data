# River_Data
## Exploring and Prediciting River Flows

The goal of this project is to predict good fishing days in the near future. To begin, I decided to gather historical river flows, historical precipitation measure, and historical precipitation forecasts. The last of which is unattainable from the government datasets I have found. Due to the lack of historical forecast data, this will be an ongoing project as I will need to gather and store this data daily. 

The project can be broken up into 5 steps:
1. Data gather/generation
  -The project leverages 2 distinct API data feeds. One source is water data from [USGS WaterFlow](https://waterservices.usgs.gov/) and the other source is precipitation data from [NOAA](https://www.weather.gov/). The NOAA source includes the upcoming 7 day forecast as well.
  -New data is initated with [PullNewData.ipynb](https://github.com/Pippeys/River_Data/blob/main/PullNewData.ipynb) (working document) which calls the 2 data sources and appends the new information to [CurrentPrecip.csv](https://github.com/Pippeys/River_Data/blob/main/CurrentPrecip.csv), [NewWeatherForecast.csv](https://github.com/Pippeys/River_Data/blob/main/NewWeatherForecast.csv), and [CurrentWater.csv](https://github.com/Pippeys/River_Data/blob/main/CurrentWater.csv)
  - River flows pulled with [WaterPull.py](https://github.com/Pippeys/River_Data/blob/main/WaterPull.py)

  - Forecast of precipitation pulled with [ForecastPrecip.py](https://github.com/Pippeys/River_Data/blob/main/ForecastPrecip.py)

  - Precipitation data pulled with [PrecipPull.ipynb](https://github.com/Pippeys/River_Data/blob/main/PrecipPull.ipynb) (not used)

2. Data wrangling /Exploration
  -The current main exploration file is [Analysis.ipynb](https://github.com/Pippeys/River_Data/blob/main/Analysis.ipynb) which is were I am exploring and analyzing the relationship of precipitation and waterflow. [DischargeAnalysis.ipynb](https://github.com/Pippeys/River_Data/blob/main/DischargeAnalysis.ipynb) begins to explore of water flow data. It's a basic exploration where I wanted to visually see the waterflow trends with peaks and troughs.

3. Metric Creation
  - Define & categorize river drainage profile
  - Shift precipitation for best fit with CFS using correlation. (Shift will depend on river profile)
  - Weather Forecast variables to consider:
    - Short Description
    - Description

4. Choosing a model(s)...Theorizing
  - I know the weather forecast data will be varied as it, itself, is a forecast; however, I'm hopeful that observing 7 days of forecasts will help predict storm intensities. The first challenge for deciding a model will be testing how to predict the actual precipitation of a given day based on the forecast of that day. To be clear, if I want to predict 1/7/23 and the date today is 1/1/23, I will have 7 days of forecasts for 1/7/2023, with the confidence of the forecast increase as it gets closer to the current day. If I'm able to predict precipitation with any signicant confidence, then I can move on to a regression model of actual precipitation & actual CFS levels.

5. Deployment
  - Raspberry Pi?


