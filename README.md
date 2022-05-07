# River_Data
## Exploring and Prediciting River Flows

Data for this project is broken into 2 parts. Part 1 is the water data which is from USGS WaterFlow and part 2 is the precipitation data which is from NOAA. The goal of this exploration and analysis is to understand the relationship of water flow (cfs) and rain precipitation. Once the exploration and analysis is completed I will attempt to build a model that will feed into a PowerBI dashboard. The goal of this ambitious project is to rate a river's ability to move water through its system. The beginning grades for this ability will be slow, average, and fast. This will be useful information when planning a trip to a river as storms push water through rivers in varying rates. 


Main file is Analysis.ipynb

DischargeAnalysis.ipynb begins the exploration of water flow data

New data is initated with PullNewData.ipynb (working document) which calls the 2 data sources and appends the new information to CurrentPrecip.csv and CurrentWater.csv

River flows pulled with WaterPull.py

Precipitation data pulled with Gov_Weather_Api.ipynb (not used)

Forecast of precipitation pulled with ForecastPrecip.py

