import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Data.csv')

#visualize oil data over time
time = df['date']
rawOil = df['dcoilwtico']
interOil = df['dcoilwtico'].interpolate()  #interpolate oil prices

plt.scatter(time, rawOil, s=0.1, color='b')
plt.plot(time,interOil,linewidth=0.8, color='r')
plt.xlabel('Time')
plt.ylabel('Oil Price')
plt.legend(['Raw Oil Prices','Oil Prices with Interpolation'])
plt.show()

#visualize store data

fig = plt.figure()

# Divide the figure into a 3x2 grid
ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)

fig.tight_layout()  #stop overlapping

#Sales by Store Type
salesST = df.groupby(['store_type']).agg({"sales" : "mean"})
ax = salesST.plot.bar(ax=ax1, legend=False)
ax.set_title("Average Sales per Store Type")
ax.xaxis.label.set_visible(False)
ax.set_ylabel("Sales")

#Sales by Store Cluster
salesSC = df.groupby(['cluster']).agg({"sales" : "mean"})
ax = salesSC.plot.bar(ax=ax3, legend=False)
ax.set_title("Average Sales Per Store Cluster")
ax.xaxis.set_visible(False)
ax.set_ylabel("Sales")

#Sales by Store Number
salesS = df.groupby(['store_nbr']).agg({"sales" : "mean"})
ax = salesS.plot.bar(ax=ax5, legend=False)
ax.set_title("Average Sales Per Store")
ax.xaxis.set_visible(False)
ax.set_ylabel("Sales")

storeData = df.loc[df['date']=='2013-01-01']
numCat = len(storeData.groupby(['family']).size())

#Sales by Store Type
countST = storeData.groupby(['store_type'])['store_type'].count() / numCat
ax = countST.plot.bar(ax=ax2, legend=False)
ax.set_title("Number of Stores by Type")
ax.xaxis.label.set_visible(False)

#Sales by Store Cluster
countSC = storeData.groupby(['cluster'])['cluster'].count() / numCat
ax = countSC.plot.bar(ax=ax4, legend=False)
ax.set_title("Number of Stores per Cluster")
ax.xaxis.set_visible(False)

plt.show()

# Product Plots
# Sales per Family
# Sales with or without promotion

# Location Plots
# Sales per city
# Sales per state
# Cities per state

# Sales Time
# Yearly Sales
# Monthly Sales
# Week day sales

# Transaction Plots
# Transaction per product
# Transaction per state
# Transactions per month
# Sales per transaction

# Special Day sales
# Sales per Holiday
# Sales per Holiday type



