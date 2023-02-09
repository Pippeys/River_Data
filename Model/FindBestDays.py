import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def FindBestDay(df):
    df['CFS_Slope'] = df.Value.diff()

    # Retrieve values of Slope
    SlopeValues = df.CFS_Slope.values

    # Define the threshold for what is a good day for fishing
    #       - slope between day CFS values must be at least 1 STD from the mean 
    border = df.CFS_Slope.mean()+(df.CFS_Slope.std()/2)

    # Define troughs that are below the threshold
    peaks, _ = find_peaks(-SlopeValues, height=border)

    # Logic to build the best day flag
    #       - if the value is a trough point or has a negative low and is above 1 STD from the mean then also consider a good day 
    bestdays = []
    for i in range(len(df.Value)):
        if i in peaks:
            x = 1
        elif (df.CFS_Slope[i]<0) & (df.Value[i]>=border):
            x = 1
        else: x = 0
        bestdays.append(x)
    df['BestDays'] = bestdays
    return df

