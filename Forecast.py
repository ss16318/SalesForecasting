import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA


def arima(timeseries,dates):
    
    #setup dataframe for forecast
    days = dates.shape[0]                           #count number of days
    
    out = pd.DataFrame(columns = ['date', 'sales']) #create dataframe
    out['date'] = dates                             #add column dates
    
    if timeseries.sum() < 10 :                      #if small sales predict zero sales
        
        out['sales'] = 0
    
    else:
        
        #take log to penalize higher values and add 1 to remove log0 error
        logTS = np.log(timeseries+1)                  
    
        #create Auto-Regressive Integrate Moving Average Model
        model = ARIMA(logTS , order=(3,1,1))
        model_fit = model.fit()
    
        #forecast sales
        forecast = model_fit.forecast(days)     #choose number of days to forecast
        forecast = forecast.to_numpy()          #convert predictions from objects to np array
        forecast = np.exp(forecast)             #perform 'anti-log' of predictions
    
        out['sales'] = forecast-1               #remove +1 shift

   
    return out

#Read data
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'

df = pd.read_csv(path + 'Data.csv')
test = pd.read_csv(path + 'Test.csv')


#save unique dates
dates = test['date'].unique()                      


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
test = test.merge(salesForecast, on=['store_nbr','date','family'], how='left')
prediction = test[['id','sales']]
prediction.to_csv('Predictions.csv', index=False)








