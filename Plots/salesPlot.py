## Forecast Display

import plotly.graph_objects as go
import pandas as pd
import numpy as np

path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'
hist = pd.read_csv(path + 'Data.csv')
future = pd.read_csv('PredPLot.csv')

pred = np.load('PredPLot.npy')

#choose automotive from store one data
hist = hist.loc[hist['family'] == 'AUTOMOTIVE']
hist = hist.loc[hist['store_nbr'] == 1]
hist = hist.loc[hist['date'] >= '2017-07-01']

past = hist[['date', 'sales']]

pastPred = hist[['date']]
last = len(pred)
latestpred = pred[last-47:]

pastPred['sales'] = latestpred.tolist()


# dict for the dataframes and their names
dfs = {"Actual Past Sales" : past, "Predicted Past Sale" : pastPred , "Predicted Future Sales": future}

# plot the data
fig = go.Figure()

for i in dfs:
    fig = fig.add_trace(go.Scatter(x = dfs[i]["date"] , y = dfs[i]["sales"] , name = i ))
    fig.update_layout(title_text= "Latest Automotive Sales in Store 1", title_x=0.5)
fig.show()
