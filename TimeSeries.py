from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

import pandas as pd
import numpy as np
import matplotlib.pylab as plt


def test_stationarity(timeseries):
    
    #Determing rolling statistics
    rolmean = pd.Series(timeseries).rolling(window=16).mean()
    rolstd = pd.Series(timeseries).rolling(window=16).std()

    #Plot rolling statistics:
    plt.plot(timeseries, color='blue',label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    
    print(dfoutput)
    
def reduceTrendMA(timeseries):
    
    #Take log to penalize large values    
    ts_log = np.log(timeseries)
    
    #Smoothing
    moving_avg = pd.Series(ts_log).rolling(window=7).mean()
    
    fig = plt.figure()
    plt.plot(ts_log)
    plt.plot(moving_avg, color='red')
    plt.show()

    #Subtract MA
    ts_log_MA = ts_log - moving_avg
    ts_log_MA.dropna(inplace=True)
    
    return ts_log_MA

def reduceTrendEMA(timeseries):
    
    #Take log to penalize large values    
    ts_log = np.log(timeseries)
    
    #Smoothing
    ema = pd.Series(ts_log).ewm(span=7, adjust=False).mean()
    
    fig = plt.figure()
    plt.plot(ts_log)
    plt.plot(ema, color='red')
    plt.show()

    #Subtract MA
    ts_log_ema = ts_log - ema
    ts_log_ema.dropna(inplace=True)
    
    return ts_log_ema

def reduceSzn(timeseries):
    
    #Take log to penalize large values    
    ts_log = np.log(timeseries)
    
    ts_log_dif = ts_log - ts_log.shift()
    
    plt.plot(ts_log_dif)
    
    ts_log_dif.dropna(inplace=True)
    
    return ts_log_dif

def arima(timeseries):
    
    logTS = np.log(timeseries)
    
    model = ARIMA(logTS , order=(20,1,10))
    model_fit = model.fit()
    results = model_fit.fittedvalues
    
    results = results[31:]
    
    plt.plot(logTS[31:])
    plt.plot(results, color='red')
    plt.show()
    
    prediction = np.exp(results)
    
    plt.plot(timeseries[31:])
    plt.plot(prediction , color = 'red')
    plt.show()
    
    


# path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'
# df = pd.read_csv(path + 'oil.csv')

# #visualize oil data over time
# time = pd.to_datetime(df['date'])
# oil = df['dcoilwtico'].interpolate() 
# oil = oil.iloc[1:]

# plt.plot(oil)

# test_stationarity(oil)

path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'
df = pd.read_csv(path + 'Data.csv')

auto = df.loc[df['family'] == 'AUTOMOTIVE']
autoSales = auto.groupby(['date']).agg({'sales':'sum'})
autoSales = autoSales['2017-01-01':]
sales = autoSales['sales']

#plt.plot(autoSales['sales'])

#test_stationarity(autoSales['sales'])

#autoSales_MA = reduceTrendMA(autoSales['sales'])

#test_stationarity(autoSales_MA)

#autoSales_EMA = reduceTrendEMA(autoSales['sales'])

# autoSales_Szn = reduceSzn(autoSales['sales'])

# test_stationarity(autoSales_Szn)

arima(sales)

