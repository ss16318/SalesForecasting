import pandas as pd
import numpy as np

forecast = pd.read_csv('predictions.csv')

forecast.replace([np.inf, -np.inf, 1], 0, inplace=True)

# READ DATA
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'

df = pd.read_csv(path + 'Data.csv')
test = pd.read_csv(path + 'Test.csv')


# PREDICTION BASED OFF RECENT SALES
recentData = df.loc[(df['date'] >= '2017-07-31') & (df['date'] < '2017-08-16')]
recentSales = recentData['sales'].reset_index()

#COMBINE FORECASTS
pred1 = recentSales['sales'] *0.5
pred2 = forecast['sales'] *0.5

forecast = pred1 + pred2

# CREATE PREDICTION FILE 
ind = test['id']

pred = pd.DataFrame(columns = ['id', 'sales'])
pred['id'] = ind
pred['sales'] = forecast

pred.to_csv('submission.csv', index=False)