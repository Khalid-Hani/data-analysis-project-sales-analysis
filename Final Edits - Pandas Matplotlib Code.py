# %%
import os
import pandas as pd

# %%
files = [file for file in os.listdir('Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data')]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/" + file)
    all_months_data = pd.concat([all_months_data , df])
    
all_months_data.to_csv('all_data.csv' , index=False)

# %%
# to read and update the DF :

all_data =pd.read_csv('all_data.csv')
all_data.head()

# %%

###augment data with aditionla colums 
# drop th Nan cells befor:
nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()



# %%
# we have to drop many row 
all_data = all_data.dropna(how='all')
all_data.head()

# %%
#find OR and delete it

temp_df = all_data[all_data['Order Date'].str[0:2]=='Or']
temp_df.head()

# %%
all_data= all_data[all_data['Order Date'].str[0:2]!='Or']


# %%

all_data['Months'] = all_data['Order Date'].str[0:2]
all_data['Months'] = all_data['Months'].astype('int32')
all_data.head()


# %%
# add a slaes column 
all_data['Quantity Ordered'] = all_data['Quantity Ordered'].astype('float')
all_data['Price Each'] = all_data['Price Each'].astype('float')

all_data['Sales'] = all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()

# %% [markdown]
# ####Q1 ---> What was the best month for Sales ? and How much was earned that month?

# %%
results  = all_data.groupby('Months').sum()['Sales']


# %%
print(results)


# %%



# %%
import matplotlib.pyplot as plt
months = range(1,13)
plt.bar(months , results)
plt.xticks(months)
#plt.yticks(results)
plt.ylabel('SALES IN USD($)')
plt.xlabel('Months')
plt.show

# %% [markdown]
# #### which city had the highst number of slaes
# 

# %%
all_data.head()

# %%
## add a City column 

# %%
# using .apply() function 

all_data['City'] = all_data['Purchase Address'].apply(lambda x:x.split(',')[1])

# %%
all_data.head()

# %%


# %%
# To find the stat as we ll is impoprtna

all_data['State'] = all_data['Purchase Address'].apply(lambda x:x.split(',')[2])
all_data['State'] = all_data['State'].apply(lambda x:x.split(' ')[1])
all_data.head()

# %%
#  SO whats the hihts City ?

#results2  = all_data.groupby(['City' , 'State']).sum()['Sales']
results2  = all_data.groupby(['City']).sum()['Sales']



# %%
print(results2)

# %%
import matplotlib.pyplot as plt

c = all_data['City'].unique()
c = [city for city , df in all_data.groupby('City')]
plt.bar(c  , results2)
plt.xticks(c , rotation = 'vertical')
plt.yticks(results2)
plt.ylabel('SALES IN USD($)')
plt.xlabel('City in Us')
plt.show

# %% [markdown]
# #### what time should we display the ads to max liklihood of coustomers buying products?

# %%
all_data.head()

# %%
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

# %%
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data.head()

# %%
import matplotlib.pyplot as plt

hours = [hour for hour , df in all_data.groupby('Hour')]
plt.plot(hours  , all_data.groupby(['Hour']).count())
#t = range(1,25)
plt.xticks(hours)
plt.xlabel('Hourse')
plt.ylabel('Number of oeders')
plt.grid()
plt.show()

# %% [markdown]
# ### What products are often sold to gether ?
# 

# %%
all_data.head()

# %%
df = all_data[all_data['Order ID'].duplicated(False)]    

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))

df = df[['Order ID' , 'Grouped']].drop_duplicates()
df.head()

# %%
from itertools import combinations
from collections import Counter

# %%
count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list ,2)))
    
for key , value in count.most_common(10):
    print(key,value)



