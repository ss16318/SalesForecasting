#Choosing parameters for ARIMA

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf , plot_acf
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'

#Read data
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'
df = pd.read_csv(path + 'Data.csv')

#Choose automotive data from store 1
data = df.loc[df['family'] == 'AUTOMOTIVE']
data = data.loc[data['store_nbr'] == 1]

#Raw plot
fig = px.line(data, x='date', y="sales" , labels={ "date": "Dates" , "sales": "Sales"} , title="Raw Automotive Sales in Store 1")
fig.show()

#Log transform
salesData = data[['date','sales']].reset_index()
salesData['logSales'] = np.log(salesData['sales']+1)

fig = px.line(salesData, x='date', y="logSales" , labels={ "date": "Dates" , "logSales": " Log Transformed Sales"} )
fig.show()

salesData['diffLogSales'] = salesData['logSales'] - salesData['logSales'].shift()
fig = px.line(salesData, x='date', y="diffLogSales" , labels={ "date": "Dates" , "diffLogSales": " Difference of Log Transformed Sales"} )
fig.show()

#Test Stationarity (p-value << 0.05 therefore differencing = 0)

result = adfuller(salesData['logSales'])
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
  print('\t%s: %.3f' % (key, value))
  
# PACF (p is 3 lags)
plot_pacf(salesData['logSales'].diff().dropna())

# ACF (q is 1 lags)
plot_acf(salesData['logSales'].diff().dropna())


