## TEST PREP

import pandas as pd


# Get Original Test Data
path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'
test = pd.read_csv(path + 'Test.csv')

# Get Unique Dates
dates = test['date'].unique()
test = pd.DataFrame(dates, columns = ['date'])

# Holidays
holidays = pd.read_csv(path + 'holidays_events.csv')
test = test.merge(holidays[['date','type']], on='date', how='left')

# Oil
oil = pd.read_csv(path + 'oil.csv')
test = test.merge(oil, on = 'date', how='left')
test = test.rename(columns = { "type" : "holiday_type" , "dcoilwtico" : "oil" })
test['oil'] = test['oil'].interpolate()

# Add Dates Breakdown & Convert to Datetime
test['date'] = pd.to_datetime(test['date'])

test['year'] = test['date'].dt.year
test['month'] = test['date'].dt.month
test['week'] = test['date'].dt.isocalendar().week
test['day_of_week'] = test['date'].dt.weekday
test['dayofyear'] = test['date'].dt.dayofyear

test.to_csv(path+'BoostTest.csv', index=False)

