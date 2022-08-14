## On Promotion Code Snippets

#Prepare promotion data
df = df[['onpromotion','sales','family']]            #create promotion df
df.loc[ df['onpromotion'] > 0 , 'onpromotion'] = 1    #make promotion info binary    

test.loc[ test['onpromotion'] > 0 , 'onpromotion'] = 1    #make promotion info binary in test  

#take average sales for products on and off promotion
d = df.groupby(['onpromotion','family']).agg({"sales" : "mean"}).reset_index()

#create seperate DFs
onSale = d.loc[d['onpromotion'] == 1].reset_index()
offSale = d.loc[d['onpromotion'] == 0]
offSale = offSale[offSale['family'] != 'BOOKS'].reset_index()

#add sales for products on/off promotion together
promSales = pd.concat([ onSale['sales'] , offSale['sales'] ] ,  axis=1)
promSales.columns = ['on' , 'off']
promSales['diff'] = ( promSales['on'] - promSales['off'] ) / promSales['off']
promSales['family'] = onSale['family']

test['AdjustedSales'] = test['sales']

for x in range (test.shape[0]):
    
    if test.loc[x].at['family'] != 'BOOKS' and test.loc[x].at['onpromotion'] > 0 :
        
        mult = promSales.loc[ promSales['family'] == test.loc[x].at['family'] , 'diff' ]
        
        newSale = test.loc[x].at['sales'] * mult.values
        
        test.loc[test.index[x], 'AdjustedSales'] = newSale
        
         
submission = test[['id','AdjustedSales']]
submission.columns = ['id','sales']
submission.to_csv('Forecast.csv', index=False)
