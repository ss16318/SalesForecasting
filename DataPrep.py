# Organizing data into a large data frame

import pandas as pd
  
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'

#Load Data
oil = pd.read_csv(path + 'oil.csv')
stores = pd.read_csv(path + 'stores.csv')
transactions = pd.read_csv(path + 'transactions.csv')
holidays = pd.read_csv(path + 'holidays_events.csv')
train = pd.read_csv(path + 'train.csv')

#Merge Data
df = train.merge(stores, on='store_nbr', how='left')
df = df.merge(transactions, on=['store_nbr','date'], how='left')
df = df.merge(holidays, on='date', how='left')
df = df.merge(oil, on = 'date', how='left')

#Format DF
df = df.rename(columns = {"type_x" : "store_type", "type_y" : "holiday_type" , "dcoilwtico" : "oil"})

df['oil'] = df['oil'].interpolate()


df['date'] = pd.to_datetime(df['date'])

#Add time scale metrics
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter
df['week'] = df['date'].dt.isocalendar().week
df['day_of_week'] = df['date'].dt.weekday
df['dayofyear'] = df['date'].dt.dayofyear

#Convert NaN transactions to 0
df['transactions'] = df['transactions'].fillna(0)

#Save data
df.to_csv(path+'Data.csv', index=False)











