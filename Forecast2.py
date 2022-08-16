import pandas as pd
import numpy as np
import xgboost as xgb


def binHol(df):
    
    df['holiday_type'] = df['holiday_type'].notnull().astype("int")
    df['holiday_type'] = df['holiday_type'].replace(np.nan, 0)
    
    return df


def boost(xTrain,yTrain,test):
    
    out = pd.DataFrame(columns = ['date', 'sales']) #create dataframe
    out['date'] = test['date']                     #add column dates
    
    if yTrain.sum() < 10 :                      #if small sales predict zero sales
        
        out['sales'] = 0
    
    else:
        
        model = xgb.XGBRegressor(n_estimators=100)
        model.fit(xTrain,yTrain)
        
        test = test.drop(['date'], axis=1)
        
        out['sales'] = model.predict(test)
        
    return out

#Read data
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'

df = pd.read_csv(path + 'Data.csv')
test = pd.read_csv(path + 'BoostTest.csv') 

test = binHol(test) 
df = binHol(df)             

#get groups of stores and products
products = df.groupby('family')
stores = df.groupby('store_nbr')


for pr in products:
    for st in stores:
        
        #get relevant rows based on unqiue product and store
        data = df.loc[df['family'] == pr[0]]
        data = data.loc[data['store_nbr'] == st[0]]
        
        xTrain = data[['year','month','dayofyear','day_of_week','oil','holiday_type','week']]
        yTrain = data['sales']
        
        #perform arima estimation for store and product
        forecast = boost(xTrain,yTrain,test)
        
        #create store and product columns
        forecast['family'] = pr[0]
        forecast['store_nbr'] = st[0]
        
        #create dataframe to save sales forecast
        if pr[0] == 'AUTOMOTIVE' and st[0] == 1:
            salesForecast = forecast     
        else:
            salesForecast = pd.concat([salesForecast,forecast],axis=0)
        
        print(str(pr[0]) + ' ' + str(st[0]))


#save boost forecast data
layout = pd.read_csv(path + 'Test.csv')
layout['date'] = layout['date'].astype('datetime64[ns]')
salesForecast['date'] = salesForecast['date'].astype('datetime64[ns]')
pred = layout.merge(salesForecast, on=['store_nbr','date','family'], how='left')
prediction = pred[['id','sales']]
prediction.to_csv('Predictions.csv', index=False)


