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
    sales = []
    with open(filename2, 'r') as file:
        next(file)  # Skip header
        for line in file:
            transaction_ID, date, product_ID, quantity, discount = line.strip().split(',')
            sales.append({'transaction_id': transaction_ID, 'date': date, 'product_id': product_ID, 'quantity': int(quantity),
                          'discount': float(discount)})
    return sales

def read_returns(filename3):
    returns = {}
    with open(filename3, 'r') as file:
        next(file)  # Skip header
        for line in file:
            transaction_ID, date = line.strip().split(',')
            returns[transaction_ID] = {'transaction_id': transaction_ID, 'date': date}
    return returns

def question1(products, sales, returns): 
    net_sales = {}
    for sale in sales:
        if sale['transaction_id'] not in returns:
            product_id = sale['product_id']
            net_sales[product_id] = net_sales.get(product_id, 0) + sale['quantity']

    # Sort products by net sales and get top 3
    top_products = list(net_sales.items())
    top_products.sort(key=lambda x: x[1], reverse=True)
    top_products = top_products[:3]

    # Print the result
    print("{:<20} {}".format("Product Name", "Units Sold"))
    print("-" * 30)
    for product_id, units_sold in top_products:
        product_name = products[product_id]['name']
        print("{:<20} {:>3}".format(product_name, units_sold))

def question2(products, sales, returns):
    # Calculate net sales amount (considering returns)
    net_sales_amount = {}
    for sale in sales:
        if sale['transaction_id'] not in returns:
            product_id = sale['product_id']
            price_per_unit = products[product_id]['price']
            total_amount = sale['quantity'] * price_per_unit
            net_sales_amount[product_id] = net_sales_amount.get(product_id, 0) + total_amount

    # Sort products by net sales amount and get top 3
    top_products_amount = list(net_sales_amount.items())
    top_products_amount.sort(key=lambda x: x[1], reverse=True)
    top_products_amount = top_products_amount[:3]

    # Print the result
    print("{:<20} {}".format("Product Name", "Amount"))
    print("-" * 30)
    for product_id, amount in top_products_amount:
        product_name = products[product_id]['name']
        formatted_amount = "${:,.2f}".format(amount)
        print("{:<20} {}".format(product_name, formatted_amount))

def question3(products, sales, returns):
    # Initialize dictionaries to store aggregated data
    total_units_sold = {}
    total_amount = {}
    total_discounted_amount = {}
    total_discount_given = {}

    # Calculate aggregated data for each product
    for sale in sales:
        if sale['transaction_id'] not in returns:
            product_id = sale['product_id']
            quantity = sale['quantity']
            price_per_unit = products[product_id]['price']
            discount = sale['discount']

            # Update total units sold
            total_units_sold[product_id] = total_units_sold.get(product_id, 0) + quantity

            # Update total amount obtained from the sale of that product
            total_amount[product_id] = total_amount.get(product_id, 0) + quantity * price_per_unit

            # Update total discounted amount for that product
            discounted_amount = quantity * price_per_unit * (1 - discount / 100)
            total_discounted_amount[product_id] = total_discounted_amount.get(product_id, 0) + discounted_amount

            # Update total discount given for that product
            total_discount_given[product_id] = total_discount_given.get(product_id, 0) + discount

    # Calculate average discount for each product
    average_discount = {}
    for product_id in total_discount_given:
        total_sales_count = total_units_sold.get(product_id, 0)
        if total_sales_count > 0:
            average_discount[product_id] = total_discount_given[product_id] / total_sales_count
        else:
            average_discount[product_id] = 0

    # Sort products by total discounted amount
    sorted_products = sorted(total_discounted_amount.items(), key=lambda x: x[1], reverse=True)

    # Print the framed table
    print("+---+--------------------+---+---------------+------+---------------+")
    print("|{:<3}|{:<20}|{:>3}|{:>15}|{:>6}|{:>15}|".format("ID", "Product Name", "Sold", "Total Amount", "Avg. Discount", "Discounted Amount"))
    print("+---+--------------------+---+---------------+------+---------------+")
    for product_id, discounted_amount in sorted_products:
        product_name = products[product_id]['name']
        units_sold = total_units_sold.get(product_id, 0)
        total_amount_formatted = "${:,.2f}".format(total_amount.get(product_id, 0))
        average_discount_formatted = "{:0<5.2f}%".format(average_discount.get(product_id, 0))
        discounted_amount_formatted = "${:,.2f}".format(discounted_amount)

        print("|{:<3}|{:<20}|{:>3}|{:>15}|{:>6}|{:>15}|".format(product_id, product_name, units_sold, total_amount_formatted, average_discount_formatted, discounted_amount_formatted))
    print("+---+--------------------+---+---------------+------+---------------+")

def main():
    products = read_products('transactions_Products.csv')
    sales = read_sales('transactions_Sales.csv')
    returns = read_returns('transactions_Returns.csv')
    question1(products, sales, returns)
    print()
    question2(products, sales, returns)
    print()
    question3(products, sales, returns)
if __name__ == '__main__':
    main()