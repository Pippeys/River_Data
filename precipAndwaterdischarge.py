import pandas as pd
import datetime as dt
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
precip_df = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/Historical/HistoricalPrecip.csv')
water_df = pd.read_csv('C:/Users/Scott/Desktop/Projects/River_Data/Historical/HistoricalDischarge.csv')
refer_df = pd.read_excel('C:/Users/Scott/Desktop/Projects/River_Data/Historical/ModelDemo.xlsx',sheet_name='Reference')

water_df['DateTime'] = water_df.DateTime.astype(str).apply(lambda x: x[:10])
water_df['DateTime'] = pd.to_datetime(water_df.DateTime,format='%Y-%m-%d')
water_df['Date'] = water_df['DateTime'].dt.date
refer_df.drop(columns='Name')
refer_df['Name'] = refer_df['USGS Name']
precip_df = precip_df.groupby(['Date','Name']).mean().astype(str).reset_index()
precip_df['NameDate'] = precip_df.Name+precip_df.Date.astype(str)
water_df = water_df.loc[water_df.VariableDescription=='Discharge'].groupby(['Date','Name']).mean().reset_index()
water_df['NameDate'] = water_df.Name+water_df.Date.astype(str)
precip_df['PrecipInches'] = precip_df.Precip.astype(float).apply(lambda x: x/2.54)
river_df = water_df.join(precip_df['PrecipInches'])
river_df = river_df.set_index('Name').join(refer_df.set_index('Name')).reset_index()
river_df = river_df.loc[river_df.Value>0]


plt.figure(figsize=[10,10])
fig = px.line(river_df, x="Date", y="Value",color='Name',
        line_group='FishType',hover_name='FishType')
# sns.lineplot(data=river_df,x='Date',y='Value',hue='Name')
fig.show()