from datetime import datetime
# import matplotlib.pyplot as plt


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
            sales[transaction_ID] = {'date': date, 'product_id': product_ID, 'quantity': int(quantity),'discount': float(discount)}
    return sales

def read_returns(filename3):
    returns = {}
    with open(filename3, 'r') as file:
        next(file)  # Skip header
        for line in file:
            transaction_ID, date = line.strip().split(',')
            returns[transaction_ID] = {'transaction_id': transaction_ID, 'date': date}
    return returns

def date_averages(products, sales, returns):
    discount_date = datetime(2024, 1, 8)
    before_discounts = {}
    after_discounts = {}

    for transaction_ID, sale_details in sales.items():
        if transaction_ID not in returns:
            product_ID = sale_details['product_id']
            discount = sale_details['discount']
            date = datetime.strptime(sale_details['date'], '%Y-%m-%d')
            

            if product_ID not in before_discounts:
                before_discounts[product_ID] = {'total_discounts': 0, 'num_transactions': 0}
            if product_ID not in after_discounts:
                after_discounts[product_ID] = {'total_discounts': 0, 'num_transactions': 0}

            if date < discount_date:
                before_discounts[product_ID]['total_discounts'] += discount
                before_discounts[product_ID]['num_transactions'] += 1
            else:
                after_discounts[product_ID]['total_discounts'] += discount
                after_discounts[product_ID]['num_transactions'] += 1

    total_before = sum(1 for product in before_discounts.values() if product['total_discounts'] == 0)
    total_after = sum(1 for product in after_discounts.values() if product['total_discounts'] == 0)

    print(f'Average transactions without discount before: {total_before / len(before_discounts):.2%}')
    print(f'Average transactions without discount after: {total_after / len(after_discounts):.2%}')

    for product_ID, product in products.items():
        product_name = product['name']
        avg_before = before_discounts[product_ID]['total_discounts'] / before_discounts[product_ID]['num_transactions'] if before_discounts[product_ID]['num_transactions'] > 0 else 0
        avg_after = after_discounts[product_ID]['total_discounts'] / after_discounts[product_ID]['num_transactions'] if after_discounts[product_ID]['num_transactions'] > 0 else 0

        print(f'{product_ID:>3} {product_name:>20} {avg_before:5.2%} - {avg_after:5.2%}')
    

def sales_per_weekday(sales, products, returns):
    # Dictionary to store total sales and transaction counts for each day of the week
    sales_by_day = {0: {'sales': 0, 'transactions': 0}, 1: {'sales': 0, 'transactions': 0},
                    2: {'sales': 0, 'transactions': 0}, 3: {'sales': 0, 'transactions': 0},
                    4: {'sales': 0, 'transactions': 0}, 5: {'sales': 0, 'transactions': 0},
                    6: {'sales': 0, 'transactions': 0}}

    # Calculate total sales and transactions for each day of the week
    for transaction_ID, sale_details in sales.items():
        date = datetime.strptime(sale_details['date'], '%Y-%m-%d')
        day_of_week = date.weekday()  # Get the day of the week (0 = Monday, 6 = Sunday)
        sales_by_day[day_of_week]['sales'] += products[sale_details['product_id']]['price'] * sale_details['quantity']
        sales_by_day[day_of_week]['transactions'] += 1

    # Subtract returned transactions
    for transaction_ID, return_details in returns.items():
        date = datetime.strptime(return_details['date'], '%Y-%m-%d')
        day_of_week = date.weekday()  # Get the day of the week (0 = Monday, 6 = Sunday)
        if transaction_ID in sales:
            sales_by_day[day_of_week]['transactions'] -= 1

    # Calculate average turnover per transaction for each day of the week
    for day in range(7):
        transactions = sales_by_day[day]['transactions']
        turnover = sales_by_day[day]['sales']
        if transactions > 0:
            avg_turnover = turnover / transactions
        else:
            avg_turnover = 0
        sales_by_day[day]['avg_turnover'] = avg_turnover

    return sales_by_day




# def plot_transactions_and_amounts_per_weekday(sales_by_day):
#     weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     transactions = [sales_by_day[day]['transactions'] for day in range(7)]
#     amounts = [sales_by_day[day]['sales'] for day in range(7)]

#     # Define bar colors (blue for weekdays, red for weekends)
#     bar_colors = ['tab:blue' if i < 5 else 'tab:red' for i in range(7)]

#     # Plot number of transactions per weekday
#     plt.figure(figsize=(10, 5))
#     plt.bar(weekdays, transactions, color=bar_colors)
#     plt.xlabel('Weekday')
#     plt.ylabel('Transactions')
#     plt.title('Number of Transactions per Weekday')
#     for i, value in enumerate(transactions):
#         plt.text(i, value, str(value), ha='center', va='bottom')
#     plt.show()

#     # Plot amounts per weekday
#     plt.figure(figsize=(10, 5))
#     plt.bar(weekdays, amounts, color=bar_colors)
#     plt.xlabel('Weekday')
#     plt.ylabel('Dollar amount')
#     plt.title('Amounts per Weekday')
#     for i, value in enumerate(amounts):
#         plt.text(i, value, '${:,.0f}'.format(value), ha='center', va='bottom')
#     plt.show()

def returned_products(products, sales, returns):
    returned_products = {}
    max_return_cost = 0
    max_return_day = None

    for transaction_ID, return_details in returns.items():
        # if transaction_ID is in returns, check for its presence in sales 
        if transaction_ID in sales:
            product_ID = sales[transaction_ID]['product_id']
            if product_ID in returned_products:
                returned_products[product_ID] += 1
            else:
                returned_products[product_ID] = 1

            # Calculate the shelving cost for the returned product
            price = products[product_ID]['price']
            shelving_cost = price * 0.1

            # Update the maximum return cost and day if necessary
            return_cost = shelving_cost * returned_products[product_ID]
            if return_cost > max_return_cost:
                max_return_cost = return_cost
                max_return_day = return_details['date']

    # Parse the date string into a date object
    date_object = datetime.strptime(max_return_day, "%Y-%m-%d")

    # Format the date into a readable string
    date_string = date_object.strftime("%A, %B %d, %Y")

    # Print the most expensive day in terms of returns
    print("Most Expensive Day in Terms of Returns:")
    print(f"{date_string:<20} Total Return Shelving(RS) Cost=$ {max_return_cost:,.2f}")

    # Print the list of items returned on that day
    print("\nProducts Returned that day:")
    print("PID         Product Name       NoI     RS Cost")
    for product_ID, count in returned_products.items():
        product_name = products[product_ID]['name']
        shelving_cost = products[product_ID]['price'] * 0.1
        return_cost = shelving_cost * count
        print(f"{product_ID:<3} {product_name:<20} {count:>3} $ {return_cost:10,.2f}")

def main():
    products = read_products('transactions_Products_January.csv')
    sales = read_sales('transactions_Sales_January.csv')
    returns = read_returns('transactions_Returns_January.csv')
    
    # Call the sales_per_weekday function and store the result in sales_by_day
    date_averages(products, sales, returns)
    sales_per_weekday(sales, products, returns)
    # plot_transactions_and_amounts_per_weekday(sales_by_day)
    
    returned_products(products, sales, returns)

if __name__ == '__main__':
    main()
