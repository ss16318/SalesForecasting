# Time Series Sales Forecasting

## A Kaggle Challenge to forecast sales for a grocery store chain in Ecuador 

 See link: https://www.kaggle.com/competitions/store-sales-time-series-forecasting

------
### Overview

Daily sales of each of the *33 products* are forecasted in each of the *54 stores* for a *16 day* period.

Sales are predicted using an **ARIMA model** (AutoRegressive Integrated Moving Average) that was developed using training data and metadata.

* Training data compromised of daily sales of each product in each store over the past 4 years (and whether the products were on promotion)

* Metadata included holidays in Ecuador (dates and types), oil prices, store information (locations and types) and daily transaction data

This model achieved a 0.44 root mean squared logarithmic error (the accuracy metric used for the challenge)


------
### Specifics

#### Data Preparation

This task involved reading training and meta data from spreadsheets, converting them to dataframes and merging them appropriately
*(See DataPrep.py file)*

#### ARIMA 

##### Groundwork

ARIMA requires a *stationary* signal which means that there should be no *trend* or *seasonality* in the signal

The raw data below shows appears to be fairly stationary. However, it was decided to air on the side of caution and perform a log transform on the data, which can be seen below the raw data. Using the "eye-ball test", we can see that the effect of large spikes is reduced, which hopefully ensures stationarity. 

To double check, the *Augmented Dickey-Fuller* test was implemented and yielded a p-value of less than 0.05. This confirmed the stationarity of the signal.

##### Choosing parameters

3 parameters must be chosen for the ARIMA model: 
* p (the order autoregressive model)
* d (the differencing order) 
* q (the order of the moving average model)









