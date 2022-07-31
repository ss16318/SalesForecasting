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
        
        #take log to penalize higher values and add 1 to remove log0 error
        logTS = np.log(timeseries+1)                  
    
        #create Auto-Regressive Integrate Moving Average Model
        model = ARIMA(logTS , order=(2,1,2))
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


#Prepare promotion data
df = df[['onpromotion','sales','family']]            #create promotion df
df.loc[ df['onpromotion'] > 0 , 'onpromotion'] = 1    #make promotion info binary    

test.loc[ test['onpromotion'] > 0 , 'onpromotion'] = 1    #make promotion info binary in test  

#take average sales for products on and off promotion
d = df.groupby(['onpromotion','family']).agg({"sales" : "mean"}).reset_index()

#create seperate DFs
onSale = d.loc[d['onpromotion'] == 1].reset_index()
offSale = d.loc[d['onpromotion'] == 0]
offSale = offSale[offSale['family'] != 'BOOKS'].reset_index()

#add sales for products on/off promotion together
promSales = pd.concat([ onSale['sales'] , offSale['sales'] ] ,  axis=1)
promSales.columns = ['on' , 'off']
promSales['diff'] = ( promSales['on'] - promSales['off'] ) / promSales['off']
promSales['family'] = onSale['family']


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

test['AdjustedSales'] = test['sales']

for x in range (test.shape[0]):
    
    if test.loc[x].at['family'] != 'BOOKS' and test.loc[x].at['onpromotion'] > 0 :
        
        mult = promSales.loc[ promSales['family'] == test.loc[x].at['family'] , 'diff' ]
        
        newSale = test.loc[x].at['sales'] * mult.values
        
        test.loc[test.index[x], 'AdjustedSales'] = newSale
        
         
submission = test[['id','AdjustedSales']]
submission.columns = ['id','sales']
submission.to_csv('Forecast.csv', index=False)






