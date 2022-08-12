# Time Series Sales Forecasting

## A Kaggle Challenge to forecast sales for a grocery store chain in Ecuador 

 See link: https://www.kaggle.com/competitions/store-sales-time-series-forecasting

------
### Overview

Daily sales of each of the *33 products* are forecasted in each of the *54 stores* for a *16 day* period.

Sales are predicted using an **ARIMA model** that was developed using training data and metadata.

* Training data compromised of daily sales of each product in each store over the past 4 years (and whether the products were on promotion)

* Metadata included holidays in Ecuador (dates and types), oil prices, store information (locations and types) and daily transaction data

This model achieved a 0.47 root mean squared logarithmic error (the accuracy metric used for the challenge)


------
### Specifics

#### Data Preparation

This task involved reading training and meta data from spreadsheets, converting them to dataframes and merging them appropriately
*(See DataPrep.py file)*

#### ARIMA 

##### Groundwork

ARIMA requires a *stationary* signal which means that there should be no *trend* or *seasonality* in the signal








