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
    for transaction_ID, transation_details in sales.items(): # Loop through sales dictionary key = transaction_ID, value = transation_details (this is another dictoinary)
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
        print('{:>20} {:>3}'.format(product_name, quantity))

def top_product_sales(products, sales, returns):
    net_sales = {}
    for transaction_ID, transation_details in sales.items():
        if transaction_ID not in returns:
            product_ID = transation_details['product_id']
            quantity = transation_details['quantity']
            price = products[product_ID]['price']
            if product_ID in net_sales:
                net_sales[product_ID] += quantity * price
            else:
                net_sales[product_ID] = quantity * price
    
    top_3_sales = sorted(net_sales.items(), key=lambda x: x[1], reverse=True)[:3] # sort the dictionary by value in descending order and take the first 3 items x = item, x[1] = value, reverse = True to sort in descending order

    for product_ID, total_sales in top_3_sales:
        product_name = products[product_ID]['name']
        amount_formatted = "${:,.2f}".format(total_sales)  # Format the amount with comma separator for thousands and two decimal places
        print("{:>20} {:>10}".format(product_name, amount_formatted))

def turnover_table(products, sales, returns):
    
    product_stats = {}
    for product_id, product_details in products.items(): # Loop through products dictionary key = product_id, value = product_details (this is another dictionnary)
        total_units_sold = 0
        total_sales_amount = 0
        total_discounts = 0
        total_discounted_amount = 0
        total_transactions = 0
        
        for sale_id, sale_details in sales.items(): # Loop through sales dictionary key = sale_id, value = sale_info (this is another dictionary)
            if sale_details['product_id'] == product_id and sale_id not in returns: # check if product_id is equal to product_id and sale_id is not in returns dictionary
                total_units_sold += sale_details['quantity']
                total_sales_amount += sale_details['quantity'] * product_details['price']
                total_discounts += sale_details['discount']
                total_discounted_amount += sale_details['quantity'] * product_details['price'] * (1 - sale_details['discount'] / 100)
                total_transactions += 1
        
        if total_transactions > 0:
            average_discount = total_discounts / total_transactions
        else:
            average_discount = 0
        
        product_stats[product_id] = { 
            'name': product_details['name'],
            'total_units_sold': total_units_sold,
            'total_sales_amount': total_sales_amount,
            'average_discount': average_discount,
            'total_discounted_amount': total_discounted_amount
        }
    
    # prints out the header for the table
    print("+---+--------------------+---+-----------+------+-----------+")
    print("|{:<3}|{:<20}|{:<3}|{:<11}|{:<6}|{:<11}|".format("ID", "Product Name", "Units", "Sales", "Disc.", "Disc. Amt"))
    print("+---+--------------------+---+-----------+------+-----------+")
    
    # Print each row with frame characters (repeats step for every product in the product_stats dictionary sorted in reverse by the total discounted amount) 
    for product_id, stat_details in sorted(product_stats.items(), key=lambda x: x[1]['total_discounted_amount'], reverse=True):
        product_name = stat_details['name']
        total_units_sold = stat_details['total_units_sold']
        total_sales_amount = stat_details['total_sales_amount']
        average_discount = stat_details['average_discount']
        total_discounted_amount = stat_details['total_discounted_amount']
        
        # Format the values according to the given formatting
        formatted_total_sales_amount = '${:>10,.2f}'.format(total_sales_amount)
        formatted_average_discount = '{:06.2f}%'.format(average_discount)
        formatted_total_discounted_amount = '${:>10,.2f}'.format(total_discounted_amount)
        
        # Print the row line
        print("+---+--------------------+---+-----------+------+-----------+")
        print("|{:<3}|{:<20}|{:>3}|{}|{}|{}|".format(
            product_id, product_name, total_units_sold, 
            formatted_total_sales_amount, formatted_average_discount, formatted_total_discounted_amount))
    
    # Print last line of the table
    print("+---+--------------------+---+-----------+------+-----------+")

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
        print("{:<9}:{:>3}".format(weekday, value))

def returned_products(products, sales, returns):
    returned_products = {}
    for transaction_ID, return_details in returns.items():
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
        print("{:<3} {:<20} {:>3}".format(product_ID, product_name, count))

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
    turnover_table(products, sales, returns)
    print()
    transactions_by_weekday(sales, returns)
    print('-'*50)
    returned_products(products, sales, returns)
    record_product_performance(products, sales, returns)

    
if __name__ == '__main__':
    main()