import os
os.chdir('/Users/dane/src/fitbit')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# this data is in long format so there are no columns other than value
df = pd.read_csv('master_long.csv', names=['date', 'user', 'measure', 'value'], index_col=False)

# look for duplicate values
df[df.duplicated(['date', 'user', 'measure'])]

# the data would look better if we create a pivot table with columns for the possible measures
dfp = pd.pivot_table(df, index=['date', 'user'], columns='measure', values='value')

# simpler index
dane = pd.pivot_table(df[df.user == 'dane'], index='date', columns='measure', values='value')

y2015 = df[(df.date >= '2015-01-01') &  (df.date <= '2015-12-31')]
y2015 = pd.pivot_table(df[(df.date >= '2015-01-01') &  (df.date <= '2015-12-31')], index='date', columns='measure', values='value')
y2015.head(20)

# return only cindy's part of the index for all dates
p15.loc[pd.IndexSlice[:,'cindy'],:]
