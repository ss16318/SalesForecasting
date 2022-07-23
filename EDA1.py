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
ax6 = fig.add_subplot(326)

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
ax.xaxis.label.set_visible(False)
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
ax.xaxis.label.set_visible(False)

# Transactions by Product
transS = df.groupby(['store_nbr']).agg({"transactions" : "mean"})
ax = transS.plot.bar(ax=ax6, legend=False)
ax.set_title("Daily Transactions per Store")
x_axis = ax6.axes.get_xaxis()
x_axis.set_visible(False)

plt.subplots_adjust(hspace=0.7)
plt.show()


# Product Plots
fig = plt.figure()
fig.tight_layout()  #stop overlapping

#Sales by Product
salesPT = df.groupby(['family']).agg({"sales" : "sum"})
salesPT = salesPT.sort_values('sales', ascending=True)
ax = salesPT.head(10).plot.barh( legend=False)
ax.set_title("Top 10 Total Selling Products")
ax.set_ylabel("Product")
ax.set_xlabel("Sales")

plt.show()


# Location Plots

#State Plot
fig = plt.figure()
fig.tight_layout()

salesS = df.groupby(['state']).agg({"sales" : "mean"})
ax = salesS.plot.barh( legend=False)
ax.set_title("Average Sales per State")
ax.set_xlabel("Sales")

plt.show()

#City Plot
fig = plt.figure()
fig.tight_layout()

salesC = df.groupby(['city']).agg({"sales" : "mean"})
ax = salesC.plot.barh( legend=False)
ax.set_title("Average Sales per City")
ax.set_xlabel("Sales")

plt.show()

#City per State Plot
fig = plt.figure()
fig.tight_layout()

CvS = df.groupby('state')['city'].nunique()
ax = CvS.plot.barh( legend=False)
ax.set_title("Cities per State")

plt.show()

# Sales Time

fig = plt.figure()

#Yearly Plot
salesY = df.groupby(['year']).agg({"sales" : "sum"})
timeY = df['year'].unique()
plt.subplot(2,2,1)
plt.plot(timeY,salesY['sales'], linewidth=0.8, color='r')
plt.title("Total Sales per Year")
plt.ylabel("Sales")
plt.yticks(fontsize=12)
plt.tight_layout()

#Weekly Plot
salesW = df.groupby(['week']).agg({"sales" : "mean"})
timeW = df['week'].unique()
plt.subplot(2,2,2)
plt.plot(timeW,salesW['sales'], linewidth=0.8, color='r')
plt.title("Average Sales per Week")
plt.ylabel("Sales")
plt.tight_layout()

#Daily Plot
salesD = df.groupby(['day_of_week']).agg({"sales" : "mean"})
timeD = df['day_of_week'].unique()
plt.subplot(2,1,2)
plt.bar(timeD,salesD['sales'], linewidth=0.8, color='r')
plt.title("Average Sales per Day")
plt.ylabel("Sales")
plt.xticks(fontsize=8)
plt.tight_layout()

plt.show()

# Transaction Plot
transW = df.groupby(['week']).agg({"transactions" : "mean"})
SpTW = salesW['sales']/transW['transactions']
timeW = df['week'].unique()

fig = plt.figure()

plt.subplot(2,1,1)
plt.plot(timeW,transW['transactions'], linewidth=0.8, color='r')
plt.title("Average Transactions per Week")
plt.ylabel("Transactions")
plt.tight_layout()

plt.subplot(2,1,2)
plt.plot(timeW,SpTW, linewidth=0.8, color='r')
plt.title("Average Sales per Transactions each Week")
plt.ylabel("Sales per Transaction")
plt.tight_layout()

plt.show()

# Holidays
# OnPromotion


