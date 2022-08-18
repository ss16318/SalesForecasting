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
        
        hist = 100
        
        for i in range(hist):
            
            past = yTrain.shift(i)
            
            xTrain['sales' + str(i)] = past
            
        xTrain = xTrain.dropna()
        sales = xTrain['sales0']
        
        xTrain = xTrain.drop(['sales0'], axis=1)
        yTrain = yTrain.iloc[hist-1:]
        
        
        model = xgb.XGBRegressor(n_estimators=100 , eta = '0.1' )
        model.fit(xTrain,yTrain)
        
        
        test = test.drop(['date'], axis=1)
        days = test.shape[0] 
        
        for x in range (days):
            
            d = test.iloc[x]
        
            for i in range(hist):
                d['sales'+str(i)] = sales.iloc[-i]
            
            
            z = pd.DataFrame(d).transpose()
            z = z.drop(['sales0'], axis=1)
            
            forecast = model.predict(z)
            sales = sales.append(pd.Series(forecast))
            
        out['sales'] = sales.tail(days).reset_index(drop=True)
        
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
        
        #data = data.dropna()
        
        xTrain = data[['year','month','week','dayofyear','day_of_week','holiday_type']]
        yTrain = data['sales']
        
        test = test[['date','year','month','week','dayofyear','day_of_week','holiday_type']]
        
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


