def print_table_border():
    print("+---+--------------------+---+-----------+------+-----------+")

def calculate_product_stats(products, sales, returns):
    product_stats = {}
    for product_id, product_details in products.items():
        total_units_sold = 0
        total_sales_amount = 0
        total_discounts = 0
        total_discounted_amount = 0
        total_transactions = 0
        DISCOUNT_DIVISOR = 100
        
        for sale_id, sale_details in sales.items():
            if sale_details['product_id'] == product_id and sale_id not in returns:
                total_units_sold += sale_details['quantity']
                total_sales_amount += sale_details['quantity'] * product_details['price'] * (1 - sale_details['discount'] / DISCOUNT_DIVISOR)
                total_discounts += sale_details['discount']
                total_discounted_amount += product_details['price'] * sale_details['discount'] 
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
    
    for product_id, stat_details in sorted(product_stats.items(), key=lambda x: x[1]['total_discounted_amount'], reverse=True):
        product_name = stat_details['name']
        total_units_sold = stat_details['total_units_sold']
        total_sales_amount = stat_details['total_sales_amount']
        average_discount = stat_details['average_discount']
        total_discounted_amount = stat_details['total_discounted_amount']
        
        formatted_total_sales_amount = f'${total_sales_amount:>10,.2f}'
        formatted_average_discount = f'{average_discount:06.2f}%'
        formatted_total_discounted_amount = f'${total_discounted_amount:>10,.2f}'
        
        print_table_border()
        print(f"|{product_id:<3}|{product_name:<20}|{total_units_sold:>3}|{formatted_total_sales_amount}|{formatted_average_discount}|{formatted_total_discounted_amount}|")