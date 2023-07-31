
# Note: This code is written in standard Python, but the main development and data analysis
# were performed using Jupyter Notebook in Visual Studio Code (VSC) for easier handling of data frames.

# Import necessary libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

# Step 1: Combine data from multiple files into a single DataFrame
files = [file for file in os.listdir('Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data')]
all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/" + file)
    all_months_data = pd.concat([all_months_data, df])

# Save the consolidated data to a CSV file
all_months_data.to_csv('all_data.csv', index=False)

# Step 2: Read the consolidated data from the CSV
all_data = pd.read_csv('all_data.csv')

# Step 3: Data Preprocessing

# Remove rows with NaN values
nan_df = all_data[all_data.isna().any(axis=1)]  # Dataframe containing rows with NaN values
all_data = all_data.dropna(how='all')  # Remove rows with all NaN values

# Remove rows with "Or" in the Order Date column (corresponding to invalid data)
temp_df = all_data[all_data['Order Date'].str[0:2] == 'Or']
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

# Extract the month from the Order Date
all_data['Months'] = all_data['Order Date'].str[0:2].astype('int32')

# Convert Quantity Ordered and Price Each columns to float and add a Sales column
all_data['Quantity Ordered'] = all_data['Quantity Ordered'].astype('float')
all_data['Price Each'] = all_data['Price Each'].astype('float')
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

# Analysis 1: What was the best month for Sales, and how much was earned that month?
results = all_data.groupby('Months').sum()['Sales']

# Print the results
print("Monthly Sales:")
print(results)

# Plot the results
months = range(1, 13)
plt.bar(months, results)
plt.xticks(months)
plt.ylabel('SALES IN USD($)')
plt.xlabel('Months')
plt.title('Monthly Sales Analysis')
plt.savefig('images/monthly_sales.png')
plt.show()

# Analysis 2: Which city had the highest number of sales?
all_data['City'] = all_data['Purchase Address'].apply(lambda x: x.split(',')[1])
all_data['State'] = all_data['Purchase Address'].apply(lambda x: x.split(',')[2].split(' ')[1])
results2 = all_data.groupby('City').sum()['Sales']

# Print the results
print("\nCity-wise Sales:")
print(results2)

# Plot the results
c = all_data['City'].unique()
c = [city for city, df in all_data.groupby('City')]
plt.bar(c, results2)
plt.xticks(c, rotation='vertical')
plt.ylabel('SALES IN USD($)')
plt.xlabel('City in US')
plt.title('City-wise Sales Analysis')
plt.savefig('images/city_sales.png')
plt.show()

# Analysis 3: What time should we display ads to maximize the likelihood of customers buying products?
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour

# Plot the results
hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of orders')
plt.title('Time-based Analysis')
plt.grid()
plt.savefig('images/time_analysis.png')
plt.show()

# Analysis 4: What products are often sold together?
df = all_data[all_data['Order ID'].duplicated(False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()

count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

# Print the results
print("\nFrequently Sold Together:")
for key, value in count.most_common(10):
    print(key, value)
