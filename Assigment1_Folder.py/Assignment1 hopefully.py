from datetime import datetime

def read_files(file_paths):
    data = {}

    for file_path in file_paths:
        data[file_path] = []

        with open(file_path, 'r') as file:
            lines = file.readlines()
            headers = lines[0].strip().split(',')
            for line in lines[1:]:
                values = line.strip().split(',')
                entry = {headers[i].lower(): values[i].strip() for i in range(len(headers))}
                data[file_path].append(entry)

    return data

def totalSales(data):
    '''Getting the total sales while also accounting for returned items.'''
    sales = data["transactions_Sales.csv"]
    returns = data['transactions_Returns.csv']

    total_sales = {}

    for sale in sales:
        product = sale['product_id']
        quantity = int(sale['quantity'])
        if product not in total_sales:
            total_sales[product] = quantity
            
        else:
            total_sales[product] += quantity

    # Accounting for returns
    for returned in returns:
        transaction_id = returned['transaction_id']
        for sale in sales:
            if sale['transaction_id'] == transaction_id:
                product = sale['product_id']
                quantity = int(sale['quantity'])
                total_sales[product] -= quantity

    return total_sales.items()
def TopSales(data):
    sorted_products = sorted(totalSales(data), key=lambda x: x[1], reverse=True)[:3]
    product_data = data["transactions_Products.csv"]

    print("Top 3 products in sales:")
    for product_id, units_sold in sorted_products:
        product_index = int(product_id[1:]) - 1  # Convert product_id to integer index
        product_name = product_data[product_index]['product_name']
        print(f"{product_name:>20} {units_sold:,}")
    print("")
    
def totalProfit(data):
    profit_per_item = {}
    returns = data['transactions_Returns.csv']
    sales = data["transactions_Sales.csv"]
    product = data['transactions_Products.csv']

    for sale in sales:
        product_id = sale['product_id']
        quantity = int(sale['quantity']) 
        discount = float(sale['discount'])
        price = int(product[int(product_id[1:]) - 1]['price'])

        if product_id not in profit_per_item:
            profit_per_item[product_id] = (quantity*(int(price)-(int(price)*discount)))
            
        else:
            profit_per_item[product_id] += (quantity*(int(price)-(int(price)*discount)))

    for returned in returns:
        transaction_id = returned['transaction_id']
        for sale in sales:
            if sale['transaction_id'] == transaction_id:
                product_id = sale['product_id']
                quantity = int(sale['quantity'])
                profit_per_item[product_id] -= (quantity*(price-(price*discount)))

    return profit_per_item.items()

def mostProfit(data):
    product_data = data["transactions_Products.csv"]
    sortedProfits = sorted(totalProfit(data), key=lambda x: x[1], reverse=True)[:3]
    print("Top 3 largest in sales by dollar:")
    for product_id, money_made in sortedProfits:
        product_index = int(product_id[1:]) - 1
        product_name = product_data[product_index]['product_name']
        formated_money = '{:,.2f}'.format(money_made)
        print(f"{product_name:>20} ${formated_money:3}")
    print("")


def turnover(data):
    productSales = totalSales(data)
    totalDiscounts = {}
    sales = data["transactions_Sales.csv"]

    #finding the tota discount and calculating the average discount
    for sale in sales:
        discount = float(sale['discount'])
        product_id = sale['product_id']
        if product_id not in totalDiscounts:
            totalDiscounts[product_id]= discount
        
        else:
            totalDiscounts[product_id] += discount

    avgDiscounts = {}
    for product_id, sales_count in productSales:
        total_discount = totalDiscounts.get(product_id, 0)
        avg_discount = (total_discount / sales_count) * 100 if sales_count != 0 else 0
        avgDiscounts[product_id] = avg_discount

    return avgDiscounts

def formatTurnover(data):
    product = data['transactions_Products.csv']
    productProfits = dict(totalProfit(data))
    productSales = dict(totalSales(data))
    avgDiscount = turnover(data)
    print("Product turnover:")
    print("+---+--------------------+---+-----------+------+-----------+")
    sortedProducts = sorted(productSales.items(), key=lambda x: x[0], reverse=True)
    for productId, unitsSold in sortedProducts:
        product_index = int(productId[1:]) - 1
        productName = product[product_index]["product_name"]
        sales_amount = productProfits[productId]
        productDiscount = avgDiscount[productId]
        discountedProfit = sales_amount*(productDiscount/100)
        print(f"|{productId:<3}|{productName:<20}|{unitsSold:>3}|${sales_amount:9,.2f}|{productDiscount:5.2f}%|${discountedProfit:9,.2f}|")
        print("+---+--------------------+---+-----------+------+-----------+")


def weeklySales(data):
    sales = data["transactions_Sales.csv"]
    returns = data['transactions_Returns.csv']
    #creating a dictionary which each date of the week since calender is unable to be imported.
    total_transactions = {        
        'Monday': 0,
        'Tuesday': 0,
        'Wednesday': 0,
        'Thursday': 0,
        'Friday': 0,
        'Saturday': 0,
        'Sunday': 0}
    
    #sale transactions
    for sale in sales:
        transaction_date = datetime.strptime(sale['date'], '%Y-%m-%d')
        weekday = transaction_date.strftime('%A')
        total_transactions[weekday] += 1

    #return transactions
    for returned in returns:
        transaction_date = datetime.strptime(returned['date'], '%Y-%m-%d')
        weekday = transaction_date.strftime('%A')
        total_transactions[weekday] += 1
    return total_transactions.items()

def formatWeeklySales(data):
    print("Number of transactions per weekday:")
    for weekday, count in weeklySales(data):
        print(f"{weekday:>9}:{count:3}")

def returnedItems(data):
    totalReturns = {}
    returns = data['transactions_Returns.csv']
    sales = data["transactions_Sales.csv"]

    for returned in returns:
        for sale in sales:
            if sale['transaction_id'] == returned['transaction_id']:
                product_id = sale['product_id']
                quantity = int(sale['quantity'])
                if product_id not in totalReturns:
                    totalReturns[product_id] = quantity
                else:
                    totalReturns[product_id] += quantity
    return totalReturns.items()

def formatReturned(data):
    product = data['transactions_Products.csv']
    sorted_returns = sorted(returnedItems(data),key = lambda x:x[0],reverse= False)
    print("")
    print("all returns")
    for product_id, quantity_returned in sorted_returns:
        product_index = int(product_id[1:]) - 1
        product_name = product[product_index]['product_name']
        print(f"{product_id} {product_name:>20} {quantity_returned:3}")
    print("")


def record_product_performance(data):
    sorted_products = sorted(totalSales(data), key=lambda x: x[0], reverse=False)

    with open("transactions_units.txt", "w") as file:
        for product_id, total_units_sold in sorted_products:
            file.write(f"{product_id},{total_units_sold}\n")

def main():
    # Example usage:
    file_paths = ["transactions_Products.csv", "transactions_Sales.csv", "transactions_Returns.csv"]
    file_data = read_files(file_paths)

    TopSales(file_data)
    mostProfit(file_data)
    formatTurnover(file_data)
    formatWeeklySales(file_data)
    formatReturned(file_data)
    record_product_performance(file_data)
main()