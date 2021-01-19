#%%

from typing import DefaultDict
from numpy.core.fromnumeric import sort
import pandas as pd
import numpy as np
from pandas.core.tools.datetimes import to_datetime
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(11.7,8.27)})

#%%

monday = pd.read_csv('data/monday.csv', sep=';', date_parser=True)
tuesday = pd.read_csv('data/tuesday.csv', sep=';')
wednesday = pd.read_csv('data/wednesday.csv', sep=';')
thursday = pd.read_csv('data/thursday.csv', sep=';')
friday = pd.read_csv('data/friday.csv', sep=';')

#%%
monday['timestamp'] = to_datetime(monday['timestamp'],format='%Y-%m-%d %H:%M:%S')
#%%
monday[monday['customer_no']==1]

#%%
df = monday.groupby('customer_no')[['location']].count()

df.hist()

#monday['duplicate'] = monday.duplicated()

#%%
profile = ProfileReport(monday)
profile

#%%%
# 
#? Q1. Calculate the total number of customers in each section
q1 = monday.groupby('location')[['location']].count()

q1.plot(kind='bar')


#%%
#? Q2 : Calculate the total number of customers in each section over time

monday['hour'] = monday['timestamp'].dt.hour
q2 = monday.groupby(['hour','location'])[['timestamp']].count()


sns.lineplot(x='hour',y='timestamp', data=q2, hue='location')

#%%

#? Q3: Display the number of customers at checkout over time
#! Creating checkout for last consumers 

#Show last entry per consumer
# How can I get the location in here ?! 

df3 = monday.groupby(['customer_no'])[['timestamp','location']].max()
df4 = monday.groupby(['customer_no'],sort='timestamp').max('timestamp')
df5 = monday.groupby(['customer_no'])[['timestamp']].max()
monday['last_entry'] = If monday['timestamp'].max()
#monday[monday['timestamp']==df5['timestamp']]

#%%
monday

#Testing Testing Yes I saw! Try to run something
#%%
#? Q4. Calculate the time each customer spent in the market
time_spent = monday.groupby('customer_no')[['timestamp']].agg(np.ptp)

time = pd.to_timedelta(time_spent.timestamp).dt.total_seconds() / 60
#(time_spent.timestamp - pd.to_datetime('1970-01-01')).dt.total_seconds()

time.hist()
