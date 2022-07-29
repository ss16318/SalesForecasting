#Forecast

import pandas as pd
import numpy as np
from scipy import stats


# READ DATA
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'

df = pd.read_csv(path + 'Data.csv')
test = pd.read_csv(path + 'Test.csv')


# PREDICTION BASED OFF RECENT SALES
recentData = df.loc[(df['date'] >= '2017-07-31') & (df['date'] < '2017-08-16')]
recentSales = recentData['sales'].reset_index()


# PREDICTION BASED OFF HISTORICAL DAY
# historicalData = df.loc[(df['week'] >= 33) & (df['week'] < 36)]
# historicalData = historicalData.tail(recentSales.shape[0])

# salesAverage = historicalData.groupby(['dayofyear','store_nbr','family']).agg({'sales':'mean'})
# salesAverage = salesAverage['sales'].reset_index()


# PREDICTION BASED OFF ON PROMOTION
promData = df.groupby('family').agg({'onpromotion':'mean'})
promSales = df.groupby('family').agg({'sales':'mean'})

x = promData['onpromotion']
y = promSales['sales']

slope, intercept, r, p, std_err = stats.linregress(x, y)

def salesPredProm(x):
  return slope * x

predSalesP = list(map(salesPredProm, test['onpromotion']))
predSalesP = np.float_(predSalesP)


#COMBINE FORECASTS
pred1 = recentSales['sales'] *1
pred2 = predSalesP *0

forecast = pred1 + pred2


#REMOVE PRODUCTS NOT SOLD IN STORES
# remove = df.groupby(["store_nbr","family"]).sales.sum().reset_index()
# remove = remove[remove.sales == 0]

# indRem = remove.index.to_numpy()
# rem = indRem

# for i in range (2,17):
    
#     new = indRem + (1782*i)
    
#     rem = np.concatenate((rem,new))
    
# for a in range (rem.shape[0]):
    
#     ind = rem[a]
    
#     forecast[ind] = 0
    
    


# CREATE PREDICTION FILE 
ind = test['id']

pred = pd.DataFrame(columns = ['id', 'sales'])
pred['id'] = ind
pred['sales'] = forecast

pred.to_csv('Predictions.csv', index=False)




