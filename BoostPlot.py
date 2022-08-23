## Visualizing

import pandas as pd
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'

#Plot Oil 
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'

rawOil = pd.read_csv(path + 'oil.csv')
interOil = rawOil.interpolate()

fig = px.line(interOil, x='date', y="dcoilwtico" , labels={ "date": "Dates" , "dcoilwtico": "Oil Price"} , title="Interpolated Oil Price" )
fig.show()

fig = px.scatter(rawOil,x='date', y="dcoilwtico" , labels={ "date": "Dates" , "dcoilwtico": "Oil Price"} , title="Raw Oil Price" )
fig.show()

