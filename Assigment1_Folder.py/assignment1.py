# Open and read the files
with open('transactions_Products.csv', 'r') as f:
    products_lines = f.readlines()[1:]  # Skip the header

with open('transactions_Sales.csv', 'r') as f:
    sales_lines = f.readlines()[1:]  # Skip the header

with open('transactions_Returns.csv', 'r') as f:
    returns_lines = f.readlines()[1:]  # Skip the header

# Parse the products
products = {line.split(',')[0]: line.split(',')[1] for line in products_lines}

# Parse the sales
sales = [(line.split(',')[2], int(line.split(',')[3])) for line in sales_lines]

# Parse the returns
returns = [line.split(',')[0] for line in returns_lines]

# Filter out the returned transactions
sales = [sale for sale in sales if sale[0] not in returns]

# Calculate the total units sold per product
units_sold = {}
for product_id, quantity in sales:
    if product_id in products:
        if products[product_id] in units_sold:
            units_sold[products[product_id]] += quantity
        else:
            units_sold[products[product_id]] = quantity

# Sort by units sold and select the top 3
top_3 = sorted(units_sold.items(), key=lambda x: x[1], reverse=True)[:3]

# Print the output
for product, units in top_3:
    print(f"{product:>20} {units:>3}")