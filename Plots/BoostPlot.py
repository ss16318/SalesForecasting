## Visualizing

import pandas as pd
import plotly.graph_objects as go
import numpy as np
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


hist = pd.read_csv(path + 'Data.csv')

pred = pd.read_csv('predFut.csv')

#choose automotive from store one data
hist = hist.loc[hist['family'] == 'AUTOMOTIVE']
hist = hist.loc[hist['store_nbr'] == 1]
hist = hist.loc[hist['date'] >= '2017-07-01']

past = hist[['date', 'sales']]


# dict for the dataframes and their names
dfs = {"Actual Past Sales" : past, "Predicted Future Sales": pred}

# plot the data
fig = go.Figure()

for i in dfs:
    fig = fig.add_trace(go.Scatter(x = dfs[i]["date"] , y = dfs[i]["sales"] , name = i ))
    fig.update_layout(title_text= "Latest Automotive Sales in Store 1", title_x=0.5)
fig.show()