from datetime import datetime

# Open and read the files
with open('transactions_Products.csv', 'r') as f:
    products_lines = f.readlines()[1:]  # Skip the header

with open('transactions_Sales.csv', 'r') as f:
    sales_lines = f.readlines()[1:]  # Skip the header

with open('transactions_Returns.csv', 'r') as f:
    returns_lines = f.readlines()[1:]  # Skip the header

# Parse the products
products = {line.split(',')[0]: (line.split(',')[1], float(line.split(',')[2])) for line in products_lines}

# Parse the sales
sales = [(line.split(',')[2], int(line.split(',')[3]), float(line.split(',')[4]), datetime.strptime(line.split(',')[1], '%Y-%m-%d').weekday()) for line in sales_lines]

# Parse the returns
returns = [line.split(',')[0] for line in returns_lines]

# Filter out the returned transactions
sales = [sale for sale in sales if sale[0] not in returns]

# Calculate the total units sold, total amount sold, average discount, and total discounted amount per product
units_sold = {}
amount_sold = {}
discounts = {}
weekday_sales = [0]*7
for product_id, quantity, discount, weekday in sales:
    if product_id in products:
        product_name, price = products[product_id]
        if product_name in units_sold:
            units_sold[product_name] += quantity
            amount_sold[product_name] += quantity * price
            discounts[product_name].append(discount)
        else:
            units_sold[product_name] = quantity
            amount_sold[product_name] = quantity * price
            discounts[product_name] = [discount]
        weekday_sales[weekday] += 1

# Calculate the average discount and total discounted amount per product
average_discount = {product: sum(discounts[product])/len(discounts[product]) for product in discounts}
total_discounted_amount = {product: amount_sold[product]*average_discount[product] for product in average_discount}

# Sort by units sold and select the top 3
top_3_units = sorted(units_sold.items(), key=lambda x: x[1], reverse=True)[:3]

# Sort by amount sold and select the top 3
top_3_amount = sorted(amount_sold.items(), key=lambda x: x[1], reverse=True)[:3]

# Print the output for units sold
print("Top 3 products by units sold:")
for product, units in top_3_units:
    print(f"{product:>20} {units:>3}")

# Print the output for amount sold
print("\nTop 3 products by amount sold:")
for product, amount in top_3_amount:
    print(f"{product:>20} ${amount:>,.2f}")

# Print the turnover for all sales
print("\nTurnover for all sales: ${:>,.2f}".format(sum(amount_sold.values())))

# Print the table of all products
print("\n+---+--------------------+---+-----------+------+-----------+")
for product_id, (product_name, price) in products.items():
    units = units_sold.get(product_name, 0)
    amount = amount_sold.get(product_name, 0)
    average = average_discount.get(product_name, 0)
    total = total_discounted_amount.get(product_name, 0)
    print(f"|{product_id:>3}|{product_name:>20}|{units:>3}|${amount:>,.2f}|{average:.2f}%|${total:>,.2f}|")
print("+---+--------------------+---+-----------+------+-----------+")

# Print the number of transactions per weekday
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for i, sales in enumerate(weekday_sales):
    print(f"{weekdays[i]:>9}:{sales:>3}")

# Print the returned products
print("\nReturned products:")
for product_id in returns:
    if product_id in products:
        product_name = products[product_id]
        print(f"{product_id} {product_name:<20} {returns.count(product_id):>3}")
    else:
        print(f"{product_id} Product not found in products list {returns.count(product_id):>3}")

# Write the total units sold per product to a text file
with open('transactions_units.txt', 'w') as f:
    for product_name, units in units_sold.items():
        f.write(f"{product_name},{units}\n")

# Continue from the existing code

# Parse the sales again to include price and discount
sales = [(line.split(',')[2], int(line.split(',')[3]), float(line.split(',')[4]), float(line.split(',')[5])) for line in sales_lines]

# Filter out the returned transactions again
sales = [sale for sale in sales if sale[0] not in returns]

# Calculate the total amount sold, average discount, and total discounted amount per product
amount_sold = {}
discounts = {}
for product_id, quantity, price, discount in sales:
    if product_id in products:
        if products[product_id] in amount_sold:
            amount_sold[products[product_id]] += quantity * price
            discounts[products[product_id]].append(discount)
        else:
            amount_sold[products[product_id]] = quantity * price
            discounts[products[product_id]] = [discount]

# Calculate the average discount and total discounted amount per product
average_discount = {product: sum(discounts[product])/len(discounts[product]) for product in discounts}
total_discounted_amount = {product: amount_sold[product]*average_discount[product] for product in average_discount}

# Sort by amount sold and select the top 3
top_3_amount = sorted(amount_sold.items(), key=lambda x: x[1], reverse=True)[:3]

# Print the output for amount sold
print("\nTop 3 products by amount sold:")
for product, amount in top_3_amount:
    print(f"{product:>20} ${amount:>,.2f}")

# Print the turnover for all sales
print("\nTurnover for all sales: ${:>,.2f}".format(sum(amount_sold.values())))

# Print the table of all products
print("\n+---+--------------------+---+-----------+------+-----------+")
for product_id, product_name in products.items():
    units = units_sold.get(product_name, 0)
    amount = amount_sold.get(product_name, 0)
    average = average_discount.get(product_name, 0)
    total = total_discounted_amount.get(product_name, 0)
    print(f"|{product_id:>3}|{product_name:>20}|{units:>3}|${amount:>,.2f}|{average:.2f}%|${total:>,.2f}|")
print("+---+--------------------+---+-----------+------+-----------+")

# Print the returned products
print("\nReturned products:")
for product_id in returns:
    product_name = products[product_id]
    print(f"{product_id} {product_name:<20} {returns.count(product_id):>3}")

# Write the total units sold per product to a text file
with open('transactions_units.txt', 'w') as f:
    for product_name, units in units_sold.items():
        f.write(f"{product_name},{units}\n")