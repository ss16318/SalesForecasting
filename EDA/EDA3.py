# On Promotion Analysis

import pandas as pd
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'

path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'

df = pd.read_csv(path + 'Data.csv')

d = df[['onpromotion','sales','family']]
d.loc[ d['onpromotion'] > 0 , 'onpromotion'] = 1

salesMean = d.groupby(['onpromotion']).agg({"sales" : "mean"})
salesStd = d.groupby(['onpromotion']).std()
salesMed = d.groupby(['onpromotion']).median()

data = d.groupby(['onpromotion','family']).agg({"sales" : "mean"}).reset_index()

onSale = data.loc[data['onpromotion'] == 1]
offSale = data.loc[data['onpromotion'] == 0]
offSale = offSale[offSale['family'] != 'BOOKS']

promSales = pd.concat([ onSale['sales'] , offSale['sales'] ] ,  axis=1)
promSales.columns = ['on' , 'off']
promSales['diff'] = ( promSales['on'] - promSales['off'] ) / promSales['off']



# data = data.sort_values('sales', ascending=True)
# data['onpromotion'] = data['onpromotion'].astype(str)
  
# fig = px.bar(data, x="family", y="sales", color="onpromotion", barmode ='group')
# fig.show()