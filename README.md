# Time Series Sales Forecasting

## A Kaggle Challenge to forecast sales for a grocery store chain in Ecuador 

 See link: https://www.kaggle.com/competitions/store-sales-time-series-forecasting

------
### Overview

Daily sales of each of the *33 products* are forecasted in each of the *54 stores* for a *16 day* period.

Sales were forecasted using two approahces: **ARIMA model** (AutoRegressive Integrated Moving Average) and **XGBoost model** (eXtreme Gradient Boosting)

The challenge used a root mean squared logarithmic error (RMSLE) metric to measure performance. It was found that the XGBoost model performed better achieving an RMSLE of 0.43 (while the ARIMA model achieved 0.44). However, given the similarity in error measure, further analysis should be carried out to definitively determine the better model. 

Two types of data were used for the models:

* **Training data** compromised of daily sales of each product in each store over the past 4 years (and whether the products were on promotion)

* **Metadata** included holidays in Ecuador (dates and types), oil prices, store information (locations and types) and daily transaction data


------
### Specifics

#### Data Preparation (used in both approaches)

This task involved reading training and meta data from spreadsheets, converting them to dataframes and merging them appropriately.

------

#### ARIMA 

##### Approach
The ARIMA model was deployed to predict sales for each product in each store independently. While the independence assumption simplifies the forecasting problem, it is unrealistic as sales most likely depend on other factors such as holidays, oil prices, sales of other products, product discounts etc....

##### Groundwork

ARIMA requires a *stationary* signal which means that there should be no *trend* or *seasonality* in the signal

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/Raw.png)

The raw data above shows appears to be non-stationary. Hence, a log transform was performed on the data, which can be seen below. Using the "eye-ball test", we can see that the effect of large spikes is reduced, which hopefully improves stationarity.

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/Log.png)

To double check, the *Augmented Dickey-Fuller* test was implemented and yielded a p-value of less than 0.05. This confirmed sufficient stationarity of the transformed signal.

##### Choosing parameters (p,d,q)

3 parameters must be chosen for the ARIMA model: 
* p (the order autoregressive model)
* d (the differencing order) 
* q (the order of the moving average model)

While the log transform of the signal is sufficiently stationary to perform ARIMA, a differencing order of 1 was used (**d=1**), which represents the change in singal intensity. As can be seen below, the mean is varies less, hence this signal has a higher degree of stationarity.

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/DiffLog.png)

The partial autocorrelation function (PACF) was used to determine the order of **p=3** (see PACF graph below)

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/PACF.png)

The autocorrelation function (ACF) was used to determine the order of **q=1** (see ACF graph below)

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/ACF.png)

Therefore, the ARIMA parameters (3,1,1) were used in the forecasting task. *(Note that in determining these parameters there is a level of subjectiveness and that these parameters were tuned accordingly to minimize the error metric of the challenge)*

##### Results

Below is a graph showing ARIMA results on in-sample and out-of-sample data from Automotive sales in Store 1. Noticeably, the predictions do not flucatuate as much as the sales, rather they hover around the mean. In the out-of-sample predictions, the predictions are essentially constant (which may be due to the Moving Average component not contributing to the prediction beacause there is no way to measure error with out-of-sample data). 

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/Sales.png)

##### Conclusion

This model yielded a reasonalby high accuracy of 0.44 RMSLE. While variations of this model made a greater attempt to model sales flucuations, these results suggest that simply predicting sales to be the historical mean is a justifiable forecasting approach. 

------

#### XGBoost 

##### Approach
Similar to the ARIMA approach, individual models were trained to predict sales for each product in each store. However, holiday data and oil prices were also features used by the boosting model.

##### Groundwork

Oil sales were not listed every day, so some values were interpolated (see graphs below).

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/rawOil.png)

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/interOil.png)

Holiday information was converted from text to binary (holiday or no holiday)

Dates were broken down into years, months, weeks, days etc...

For each training point sales history spanned over the last 100 days *(note by increasing the number of sales history features, the number of training samples decreased - hence there is a sweet spot in this trade-off)*

As mentioned, the model was trained using not just sales history, but holidays, date breakdowns etc... Therefore, the testing data had to be processed in order to match the features used during training.

*(Note that although testing included oil price as a feature, performance with this feature decreased - hence it was not included in the final XGBoost model)*

##### Choosing Parameters

Through trial-and-error the following parameters were used:

* Number of Trees = 100

* Learning rate = 0.1

* The boosting model predicted sales through regression (not classification)

##### Results

Again, in-sample and out-of-sample data from Automotive sales in Store 1 is shown below (using XGBoost this time).

![alt text](https://github.com/ss16318/SalesForecasting/blob/main/Plots/SalesBoost.png)

##### Conclusion

From the graph, it is clear that this approach makes a greater attempt to forecast sales volatility (although not all the way to the extremes). This model achieved the most accurate RMSLE score of 0.43 and placed 70th out of 604 teams on the Kaggle Leaderboard.

------

#### Verdict

Instead of using the ARIMA model, a simple historical sales average would yield acceptable results. 

The XGBoost model produced marginally better results, but it importantly forecasted volatility. Hence, there is potential that further work into developing more insightful features and tuning parameters will result in a more accurate model that is able to forecast greater volatility.  










