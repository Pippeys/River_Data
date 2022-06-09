# River_Data
## Exploring and Prediciting River Flows

The goal of this project is to rate a river's ability to move water through its system, I'll be calling this "flushing". The beginning grades for flushing will be slow, average, and fast. This will be useful information when planning a trip to a river as storms affect rivers different rates. 

This ongoing project leverages 2 distinct API data feeds. One source is water data from [USGS WaterFlow](https://waterservices.usgs.gov/) and the other source is precipitation data from [NOAA](https://www.weather.gov/). The goal of this analysis is to understand the relationship of water flow (cfs) and rain precipitation. The project has three main parts: 

  - Data Wrangling & Explore
  - Analysis
  - Modeling


The current main file is [Analysis.ipynb](https://github.com/Pippeys/River_Data/blob/main/Analysis.ipynb) which is were I am exploring and analyzing the relationship of precipitation and waterflow. [DischargeAnalysis.ipynb](https://github.com/Pippeys/River_Data/blob/main/DischargeAnalysis.ipynb) begins to explore of water flow data. It's a basic exploration where I wanted to visually see the waterflow trends with peaks and troughs.



New data is initated with [PullNewData.ipynb](https://github.com/Pippeys/River_Data/blob/main/PullNewData.ipynb) (working document) which calls the 2 data sources and appends the new information to [CurrentPrecip.csv](https://github.com/Pippeys/River_Data/blob/main/CurrentPrecip.csv) and [CurrentWater.csv](https://github.com/Pippeys/River_Data/blob/main/CurrentWater.csv)

- River flows pulled with [WaterPull.py](https://github.com/Pippeys/River_Data/blob/main/PrecipPull.py)

- Forecast of precipitation pulled with [ForecastPrecip.py](https://github.com/Pippeys/River_Data/blob/main/ForecastPrecip.py)

- Precipitation data pulled with [Gov_Weather_Api.ipynb](https://github.com/Pippeys/River_Data/blob/main/Gov_Weather_Api.ipynb) (not used)


Current status & goals:
1. Retrieve ~10 years of river and weather data. (Completed)
2. Decide and develop a process to deal with poor data quality. (Current)
3. implement a daily automated process to retrieve and store data.
4. Develop a model for forecasting river flow based on current conditions. 
