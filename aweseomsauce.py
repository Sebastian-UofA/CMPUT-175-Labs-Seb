#!/usr/bin/env python
# coding: utf-8

# In[46]:


### Step 1: Read and Parse CSV Data


import datetime

def read_csv(filepath):
    data = []
    with open(filepath, 'r') as file:
        headers = file.readline().strip().split(',')
        for line in file:
            record = dict(zip(headers, line.strip().split(',')))
            data.append(record)
    return data

# Reading CSV Files
sales_data = read_csv('transactions_Sales_January.csv')
products_data = read_csv('transactions_Products_January.csv')

# Converting sales data dates and discounts to appropriate types
for sale in sales_data:
    sale['date'] = datetime.datetime.strptime(sale['date'], "%Y-%m-%d")
    sale['discount'] = float(sale['discount'])

### Step 2: Calculating Discount Averages and No Discount Transactions


# Setting up data structures
discounts_before = {}
discounts_after = {}
product_names = {product['Product_ID']: product['Product_Name'] for product in products_data}
for product in products_data:
    discounts_before[product['Product_ID']] = []
    discounts_after[product['Product_ID']] = []

# Aggregating discount data
for sale in sales_data:
    if sale['date'] < datetime.datetime(2024, 1, 8):
        discounts_before[sale['product_id']].append(sale['discount'])
    else:
        discounts_after[sale['product_id']].append(sale['discount'])

# Calculating metrics
def calculate_average(discounts):
    return sum(discounts) / len(discounts) if discounts else 0

total_transactions = len(sales_data)
no_discount_before = sum(1 for discounts in discounts_before.values() if not discounts)
no_discount_after = sum(1 for discounts in discounts_after.values() if not discounts)
percentage_no_discount_before = (no_discount_before / total_transactions) * 100
percentage_no_discount_after = (no_discount_after / total_transactions) * 100

# Formatted Output
print(f"{'':>51}<08-01  - >=08-01")
print(f"Average transaction without discount: {percentage_no_discount_before:5.2f}% - {percentage_no_discount_after:5.2f}%")
print("Average discount per product:")
for product_id in sorted(product_names.keys()):
    avg_before = calculate_average(discounts_before[product_id])
    avg_after = calculate_average(discounts_after[product_id])
    print(f"{product_id:>3} {product_names[product_id]:>20} {avg_before*100:5.2f}% - {avg_after*100:5.2f}%")


# In[47]:


import datetime

# Assuming read_csv function is already defined from previous question
sales_data = read_csv('transactions_Sales_January.csv')
products_data = read_csv('transactions_Products_January.csv')

# Setting up a dictionary to hold sales by weekday
weekday_sales = {i: {'count': 0, 'total_sales': 0.0} for i in range(7)}

# Extract product prices into a dict for easier access
product_prices = {product['Product_ID']: float(product['Price']) for product in products_data}

# Process each sale
for sale in sales_data:
    sale_date = datetime.datetime.strptime(sale['date'], "%Y-%m-%d")
    product_id = sale['product_id']
    quantity = int(sale['quantity'])
    discount = float(sale['discount'])  # Corrected conversion here
    product_price = product_prices.get(product_id, 0)  # Using get to avoid KeyError if product_id not found
    
    # Calculate the total sale amount after discount for this transaction
    total_sale_amount = (quantity * product_price) * (1 - discount)
    
    # Accumulate sales data
    weekday = sale_date.weekday()  # Monday is 0 and Sunday is 6
    weekday_sales[weekday]['count'] += 1
    weekday_sales[weekday]['total_sales'] += total_sale_amount

# Calculating averages and preparing printout
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(" +-----------+-----+-------------+")
print(" | Day       |NB Tr|    Turnover |")
print(" +-----------+-----+-------------+")
for i, day in enumerate(days):
    avg_transactions = round(weekday_sales[i]['count'] / 4)  # Assuming 4 weeks in January
    avg_turnover = "{:,.2f}".format(weekday_sales[i]['total_sales'] / 4)  # Formatting to 2 decimal places and adding commas
    print(f" | {day:<9} | {avg_transactions:3} | ${avg_turnover:>10} |")
print(" +-----------+-----+-------------+")


# In[48]:


import matplotlib.pyplot as plt

# Convert the aggregated totals into lists for plotting, with transactions rounded
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
transactions = [round(weekday_sales[i]['count'] / 4) for i in range(7)]  # Rounded average transactions
turnovers = [weekday_sales[i]['total_sales'] / 4 for i in range(7)]  # Average turnover

# Plotting number of transactions per weekday
plt.figure(figsize=(10, 6))
bar_colors = ['tab:blue' if i < 5 else 'tab:red' for i in range(7)]
trans_bars = plt.bar(days, transactions, color=bar_colors)
plt.xlabel('Day of the Week')
plt.ylabel('Transactions')
plt.title('Average Number of Transactions by Weekday')
plt.bar_label(trans_bars)
plt.xticks(rotation=45)  # Rotate labels to fit better
plt.show()

# Plotting turnover amounts per weekday, formatted as requested
plt.figure(figsize=(10, 6))
turn_bars = plt.bar(days, turnovers, color=bar_colors)
plt.xlabel('Day of the Week')
plt.ylabel('Dollar Amount')
plt.title('Average Turnover by Weekday')

# Applying formatting to the turnover amounts for labels
def format_label(amount):
    return '${:,.0f}'.format(amount)
turn_labels = [format_label(turnover) for turnover in turnovers]

plt.bar_label(turn_bars, labels=turn_labels)
plt.xticks(rotation=45)  # Rotate labels for better readability
plt.show()


# In[49]:


import datetime

# Assuming read_csv function is already defined
returns_data = read_csv('transactions_Returns_January.csv')
# Assuming products_data and sales_data are already loaded as well
# You might need to re-read sales_data to ensure it includes all necessary details

# Convert return dates and associate returns with costs
return_costs = {}
for return_entry in returns_data:
    return_date_str = return_entry['date']
    return_date = datetime.datetime.strptime(return_date_str, "%Y-%m-%d").date()
    trans_id = return_entry['transaction_id']
    
    # Find the corresponding sale transaction
    related_sale = next((sale for sale in sales_data if sale['transaction_id'] == trans_id), None)
    
    # Calculate the shelving cost
    if related_sale:
        product_id = related_sale['product_id']
        quantity = int(related_sale['quantity'])
        product_price = float(next((product['Price'] for product in products_data if product['Product_ID'] == product_id), 0))
        
        shelving_cost = (product_price * quantity) * 0.1  # 10% of the item's original price
        
        if return_date not in return_costs:
            return_costs[return_date] = {'total_cost': 0, 'details': []}
        
        return_costs[return_date]['total_cost'] += shelving_cost
        return_costs[return_date]['details'].append((product_id, quantity, shelving_cost))

# Find the day with the highest return cost
max_cost_date, max_cost_data = max(return_costs.items(), key=lambda x: x[1]['total_cost'])

print(f"{max_cost_date.strftime('%A, %B %d, %Y')} Total Return Shelving(RS) Cost= ${max_cost_data['total_cost']:,.2f}")
print("Products Returned that day:")
print("PID         Product Name        NoI RS Cost")

for detail in max_cost_data['details']:
    product_id, quantity, shelving_cost = detail
    product_name = next((product['Product_Name'] for product in products_data if product['Product_ID'] == product_id), "")
    print(f"{product_id:<3} {product_name:20} {quantity:<3} ${shelving_cost:10,.2f}")


# In[50]:


# Assuming sales_data, products_data, and returns_data are already loaded
# Aggregate sales
product_sales = {}
for sale in sales_data:
    product_id = sale['product_id']
    quantity = int(sale['quantity'])
    if product_id not in product_sales:
        product_sales[product_id] = 0
    product_sales[product_id] += quantity

# Adjust for returns
for return_entry in returns_data:
    related_sale = next((sale for sale in sales_data if sale['transaction_id'] == return_entry['transaction_id']), None)
    if related_sale:
        product_id = related_sale['product_id']
        quantity = int(related_sale['quantity'])
        # Subtract the returns
        if product_id in product_sales:
            product_sales[product_id] -= quantity

# Compile the order information
order_info = []
for product_id, sales_count in product_sales.items():
    product_name = next((product['Product_Name'] for product in products_data if product['Product_ID'] == product_id), "")
    order_info.append((product_id, product_name, sales_count))

# Sort by Product ID
order_info.sort(key=lambda x: x[0])

# Write to a file and print the information
with open('order_supplier_January.txt', 'w') as f:
    for entry in order_info:
        product_id, product_name, sales_count = entry
        # Writing to file
        line = f"{product_id} {product_name} {sales_count}\n"
        f.write(line)
        
        # Print to screen
        print(f"{product_id:>3} {product_name:<20} {sales_count:>3}")


# In[51]:


# Assuming sales_data, products_data, and returns_data are preloaded as before

# Step 1: Aggregate sales and adjust for returns
product_sales = {product['Product_ID']: {'count': 0, 'dates': []} for product in products_data}
for sale in sales_data:
    product_id = sale['product_id']
    product_sales[product_id]['count'] += int(sale['quantity'])
    product_sales[product_id]['dates'].append(sale['date'][:10])  # Assuming the date is in the first 10 characters

for return_entry in returns_data:
    related_sale = next((sale for sale in sales_data if sale['transaction_id'] == return_entry['transaction_id']), None)
    if related_sale:
        product_id = related_sale['product_id']
        product_sales[product_id]['count'] -= int(related_sale['quantity'])  # Adjusting for returns

# Step 2 & 3: Determine if there are products that were never sold or find the ones with the least sales
never_sold_products = [pid for pid, details in product_sales.items() if details['count'] == 0]
least_sold_count = min(details['count'] for details in product_sales.values()) if not never_sold_products else None

# Step 4: Print the output based on the data
if never_sold_products:
    for product_id in never_sold_products:
        product_name = next(product['Product_Name'] for product in products_data if product['Product_ID'] == product_id)
        print(f"{product_id:>3} {product_name:20}")
else:
    least_sold_products = [(pid, details) for pid, details in product_sales.items() if details['count'] == least_sold_count]
    for product_id, details in least_sold_products:
        product_name = next(product['Product_Name'] for product in products_data if product['Product_ID'] == product_id)
        sales_dates = ', '.join(details['dates'])
        print(f"{product_id:>3} {product_name:20} {details['count']:3} [{sales_dates}]")


# In[52]:


import numpy as np
import matplotlib.pyplot as plt

# Assuming products_data and sales_data are preloaded

# Step 1: Calculate the average discount for each product
discounts_by_product = {}
for sale in sales_data:
    product_id = sale['product_id']
    discount = float(sale['discount'])
    if product_id not in discounts_by_product:
        discounts_by_product[product_id] = []
    discounts_by_product[product_id].append(discount)

average_discounts = {pid: np.mean(discounts) for pid, discounts in discounts_by_product.items()}

# Step 2: Prepare data for analysis
prices = []
averages = []
for product in products_data:
    product_id = product['Product_ID']
    price = float(product['Price'])
    if product_id in average_discounts:  # Ensure there's a corresponding discount
        prices.append(price)
        averages.append(average_discounts[product_id])

# Step 3: Calculate the Pearson correlation coefficient
r = np.corrcoef(prices, averages)
print(f"Pearson Correlation= {r[0,1]:.3f}")

# Step 4: Plotting the data points and linear regression line
x = np.array(prices)
y = np.array(averages)
coef = np.polyfit(x, y, 1)
poly1d_fn = np.poly1d(coef)  # Function for the linear regression line

plt.figure(figsize=(8, 6))
plt.plot(x, y, 'bo', label='Avg Discounts vs. Price')  # Data points in blue
plt.plot(x, poly1d_fn(x), '--k', label='Regression Line')  # Regression line in black dashed

plt.xlabel('Product Price ($)')
plt.ylabel('Average Discount (%)')
plt.title('Average Discounts Obtained vs. Product Price')
plt.legend()
plt.grid(True)
plt.show()

