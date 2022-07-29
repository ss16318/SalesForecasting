import pandas as pd
import numpy as np
import matplotlib.pylab as plt

from statsmodels.tsa.arima.model import ARIMA


def arima(timeseries,dates):
    
    #setup dataframe for forecast
    days = dates.shape[0]                           #count number of days
    
    out = pd.DataFrame(columns = ['date', 'sales']) #create dataframe
    out['date'] = dates                             #add column dates
    
    if timeseries.sum() < 10 :                      #if small sales predict zero sales
        
        out['sales'] = 0
    
    else:
        
        timeseries.loc[timeseries < 1] = 1          #set small values to 1
        
        logTS = np.log(timeseries)                  #take log to penalize higher values
    
        #create Auto-Regressive Integrate Moving Average Model
        model = ARIMA(logTS , order=(20,3,20))
        model_fit = model.fit()
    
        #forecast sales
        forecast = model_fit.forecast(days)     #choose number of days to forecast
        forecast = forecast.to_numpy()          #convert predictions from objects to np array
        forecast = np.exp(forecast)             #perform 'anti-log' of predictions
    
        out['sales'] = forecast

   
    return out

#Read data
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'

df = pd.read_csv(path + 'Data.csv')
test = pd.read_csv(path + 'Test.csv')


#Create prediction
pred = test[['id','date','store_nbr','family']]    #save important info from test
dates = pred['date'].unique()                      #save unique dates


#Only look at data from this year
df = df[ df['date'] > '2017-01-01' ]


#get groups of stores and products
products = df.groupby('family')
stores = df.groupby('store_nbr')

for pr in products:
    for st in stores:
        
        #get relevant rows based on unqiue product and store
        data = df.loc[df['family'] == pr[0]]
        data = data.loc[data['store_nbr'] == st[0]]
        
        #perform arima estimation for store and product
        forecast = arima(data['sales'],dates)
        
        #create store and product columns
        forecast['family'] = pr[0]
        forecast['store_nbr'] = st[0]
        
        #create dataframe to save sales forecast
        if pr[0] == 'AUTOMOTIVE' and st[0] == 1:
            salesForecast = forecast     
        else:
            salesForecast = pd.concat([salesForecast,forecast],axis=0)
        
        
        print(str(pr[0]) + ' ' + str(st[0]))


#save arima forecast data
pred = pred.merge(salesForecast, on=['store_nbr','date','family'], how='left')
prediction = pred[['id','sales']]
prediction.loc[ prediction['sales']>2000 , 'sales'] = 2000
prediction.to_csv('Predictions.csv', index=False)


#get recent sales
recentData = df.loc[(df['date'] >= '2017-07-31') & (df['date'] < '2017-08-16')]
recentSales = recentData['sales'].reset_index()


#combine recent sales with arima forecast
pred1 = recentSales['sales'] *0.5
pred2 = prediction['sales'] *0.5


# CREATE PREDICTION FILE 
ind = test['id']

submission = pd.DataFrame(columns = ['id', 'sales'])
submission['id'] = ind
submission['sales'] = forecast

submission.to_csv('submission.csv', index=False)





