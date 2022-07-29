# Second Level EDA

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


path = 'C:/Users/sebas/Desktop/Kaggle/ForecastingData/'
df = pd.read_csv(path + 'Data.csv')


oil = df["dcoilwtico"]

# promData = df.groupby('family').agg({'onpromotion':'mean'})
# promSales = df.groupby('family').agg({'sales':'mean'})

# x = promData['onpromotion']
# y = promSales['sales']

# slope, intercept, r, p, std_err = stats.linregress(x, y)

# def myfunc(x):
#   return slope * x + intercept

# mymodel = list(map(myfunc, x))

# plt.scatter(x,y)
# plt.plot(x, mymodel)
# plt.xlabel('No. Items On Promotion')
# plt.ylabel('Sales')
# plt.show()


# products = df.groupby('family')

# for x in products:
    
#     prodData = df.loc[df['family'] == x[0]]
    
#     prom = prodData['onpromotion']
#     sales = prodData['sales']
#     oil = prodData["dcoilwtico"]
    
#     plt.scatter(prom,sales)
#     plt.xlabel('# items on promotion')
#     plt.ylabel('Sales')
#     plt.title(x[0])
#     plt.show()
    
#     plt.scatter(oil,sales)
#     plt.xlabel('Oil Price')
#     plt.ylabel('Sales')
#     plt.title(x[0])
#     plt.show()
    
    
products = df.groupby('store_type')

for x in products:
    
    prodData = df.loc[df['store_type'] == x[0]]
    
    prom = prodData['onpromotion']
    sales = prodData['sales']
    
    plt.scatter(prom,sales)
    plt.xlabel('# items on promotion')
    plt.ylabel('Sales')
    plt.title(x[0])
    plt.show()
    

