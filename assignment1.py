# author: Sebastian Perez
# References: 
# https://www.geeksforgeeks.org/python-program-to-find-the-highest-3-values-in-a-dictionary/
# https://www.w3schools.com/python/python_datetime.asp


import datetime

def read_products(filename1):
    products = {}
    with open(filename1, 'r') as file:
        next(file)
        for line in file:
            product_ID, product_name, price = line.strip().split(',')
            products[product_ID] = {'name': product_name, 'price': float(price)}
    return products

def read_sales(filename2):
    sales = {}
    with open(filename2, 'r') as file:
        next(file)  # Skip header
        for line in file:
            transaction_ID, date, product_ID, quantity, discount = line.strip().split(',')
            sales[transaction_ID] = {'date': date, 'product_id': product_ID, 'quantity': int(quantity),
                                     'discount': float(discount)}
    return sales

def read_returns(filename3):
    returns = {}
    with open(filename3, 'r') as file:
        next(file)  # Skip header
        for line in file:
            transaction_ID, date = line.strip().split(',')
            returns[transaction_ID] = {'transaction_id': transaction_ID, 'date': date}
    return returns

def top_units_sold(products, sales, returns):
    net_units_sold = {}
    # Loop through sales dictionary key = transaction_ID, value = transation_details (this is another dictoinary)
    for transaction_ID, transation_details in sales.items(): 
        # account for returned items
        if transaction_ID not in returns:
            product_ID = transation_details['product_id']
            quantity = transation_details['quantity']
            if product_ID in net_units_sold: # check if product_ID is slready in net_units_sold dictionary
                net_units_sold[product_ID] += quantity
            else:
                net_units_sold[product_ID] = quantity 

    # Sort the dictionary by value in descending order and take the first 3 items
    top_3_products = sorted(net_units_sold.items(), key=lambda x: x[1], reverse=True)[:3] # sort the dictionary by value in descending order and take the first 3 items x = item, x[1] = value, reverse = True to sort in descending order

    for product_ID, quantity in top_3_products:
        product_name = products[product_ID]['name']
        print(f"{product_name:>20} {quantity:>3}")

def top_product_sales(products, sales, returns):
    net_sales = {}
    for transaction_ID, transation_details in sales.items():
        if transaction_ID not in returns:
            product_ID = transation_details['product_id']
            quantity = transation_details['quantity']
            discount = transation_details['discount']
            price = products[product_ID]['price']
            if product_ID in net_sales:
                net_sales[product_ID] += int(quantity) * price * (1 - discount / 100)
            else:
                net_sales[product_ID] = int(quantity) * int(price) * (1 - discount / 100)
    
    top_3_sales = sorted(net_sales.items(), key=lambda x: x[1], reverse=True)[:3] # sort the dictionary by value in descending order and take the first 3 items x = item, x[1] = value, reverse = True to sort in descending order

    for product_ID, total_sales in top_3_sales:
        product_name = products[product_ID]['name']
        amount_formatted = f"${total_sales:,.2f}"  # Format the amount with comma separator for thousands and two decimal places
        print(f"{product_name:>20} {amount_formatted:>10}")

def print_table_border():
    print("+---+--------------------+---+-----------+------+-----------+")

def calculate_product_stats(products, sales, returns):
    product_stats = {}
    DISCOUNT_DIVISOR = 100

    for product_id, product_details in products.items():
        total_units_sold = 0
        total_sales_amount = 0
        total_discounts = 0
        total_discounted_amount = 0
        total_transactions = 0

        for sale_id, sale_details in sales.items():
            if sale_details['product_id'] == product_id and sale_id not in returns:
                quantity = sale_details['quantity']
                discount = sale_details['discount']
                price = product_details['price']

                total_units_sold += quantity
                total_sales_amount += quantity * price * (1 - discount / DISCOUNT_DIVISOR)
                total_discounts += discount
                total_discounted_amount += price * discount 
                total_transactions += 1

        average_discount = total_discounts / total_transactions if total_transactions > 0 else 0

        product_stats[product_id] = { 
            'name': product_details['name'],
            'total_units_sold': total_units_sold,
            'total_sales_amount': total_sales_amount,
            'average_discount': average_discount,
            'total_discounted_amount': total_discounted_amount
        }

    return product_stats

def print_turnover_table(product_stats):
    print_table_border()
    print(f"|{'ID':<3}|{'Product Name':<20}|{'Units':<3}|{'Sales':<11}|{'Disc.':<6}|{'Disc. Amt':<11}|")
    print_table_border()

    sorted_product_stats = sorted(product_stats.items(), key=lambda x: x[1]['total_discounted_amount'], reverse=True)
    
    for product_id, stat_details in sorted_product_stats:
        product_name = stat_details['name']
        total_units_sold = stat_details['total_units_sold']
        total_sales_amount = f'${stat_details["total_sales_amount"]:>10,.2f}'
        average_discount = f'{stat_details["average_discount"]:06.2f}%'
        total_discounted_amount = f'${stat_details["total_discounted_amount"]:>10,.2f}'
        
        print_table_border()
        print(f"|{product_id:<3}|{product_name:<20}|{total_units_sold:>3}|{total_sales_amount}|{average_discount}|{total_discounted_amount}|")
    
    print_table_border()
def transactions_by_weekday(sales, returns):
    weekday_transactions = {
        'Monday': 0,
        'Tuesday': 0,
        'Wednesday': 0,
        'Thursday': 0,
        'Friday': 0,
        'Saturday': 0,
        'Sunday': 0
    }

    # loops through the sales dictionary and increments the count for the weekday for every transaction it appears on
    for transaction_ID, sale_details in sales.items():
        if transaction_ID not in returns:
            weekday = datetime.datetime.strptime(sale_details['date'], '%Y-%m-%d').strftime('%A') # convert date to weekday
            weekday_transactions[weekday] += 1 # increment the count for the weekday for every transaction it appears on

    # Print transaction for every weekday
    print("Number of Transactions per Weekday:")
    for weekday, value in weekday_transactions.items():
        print(f"{weekday:<9}:{value:>3}")

def returned_products(products, sales, returns):
    returned_products = {}
    for transaction_ID, return_details in returns.items():
        # if transaction_ID is in returns, check for its presence in sales 
        if transaction_ID in sales:
            product_ID = sales[transaction_ID]['product_id']
            if product_ID in returned_products:
                returned_products[product_ID] += 1
            else:
                returned_products[product_ID] = 1

    # Print the number of returned products for each product
    print("Number of Returned Products:")
    for product_ID, count in returned_products.items():
        product_name = products[product_ID]['name']
        print(f"{product_ID:<3} {product_name:<20} {count:>3}")

def record_product_performance(products, sales, returns):
    with open("transactions_units.txt", "w") as file:
        for product_id, product_details in products.items():
            total_units_sold = 0
            for transaction_ID, sale_details in sales.items():
                if sale_details['product_id'] == product_id and transaction_ID not in returns:
                    total_units_sold += sale_details['quantity']
            file.write(f"{product_id},{total_units_sold}\n")

    
def main():
    products = read_products('transactions_Products.csv')
    sales = read_sales('transactions_Sales.csv')
    returns = read_returns('transactions_Returns.csv')

    print('-'*50)
    top_units_sold(products, sales, returns)
    print('-'*50)
    top_product_sales(products, sales, returns)
    print()
    print_turnover_table(calculate_product_stats(products, sales, returns))
    print()
    transactions_by_weekday(sales, returns)
    print('-'*50)
    returned_products(products, sales, returns)
    record_product_performance(products, sales, returns)

    
if __name__ == '__main__':
    main()